import streamlit as st
import chromadb
import os
from pathlib import Path
import requests

# --- LlamaIndex Imports ---
from llama_index.core import (
    VectorStoreIndex, 
    SimpleDirectoryReader, 
    Settings, 
    StorageContext,
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.langchain import LangChainLLM
from llama_index.embeddings.openai import OpenAIEmbedding
from langchain_openai import ChatOpenAI
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# ==========================================
# 1. КОНФИГУРАЦИЯ И СИСТЕМНЫЙ ПРОМПТ
# ==========================================

SYSTEM_PROMPT = """# РОЛЬ И МИССИЯ
Ты — «Универсальный Лингвистический Тьютор» (Polyglot RAG). Твоя цель — помогать пользователю изучать языки, опираясь СТРОГО на предоставленную базу знаний. Ты общаешься с пользователем на русском языке.

# АРХИТЕКТУРА И ИЗОЛЯЦИЯ КОНТЕКСТА (КРИТИЧЕСКИ ВАЖНО)
Твоя база знаний разделена на 4 независимых языковых домена:
1. Французский
2. Белорусский (аканне, дзеканне, тарашкевіца/наркамаўка)
3. Эсперанто (абсолютно регулярный, без исключений)
4. Синдарин (эльфийский, мутации, i-аффония)

ПРАВИЛО ИЗОЛЯЦИИ: Определи язык пользователя. Если извлеченный RAG-контекст относится к ДРУГОМУ языку — ИГНОРИРУЙ его. Никогда не применяй правила одного языка к другому. Если информации нет, честно скажи: "В предоставленных материалах по этому языку данное правило не детализировано".

# ПРИНЦИПЫ ОБУЧЕНИЯ
1. Структурированность: Используй Markdown. Выделяй жирным ключевые слова и окончания.
2. Декомпозиция: Разбирай сложные слова на морфемы (корень, префикс, суффикс), особенно в Эсперанто и Синдарине.
3. Контекст чтения: Приводи примеры из литературы, новостей или лора.
4. Разбор ошибок: Похвали за попытку, укажи на ошибку, объясни правило.

# ФОРМАТ ГЕНЕРАЦИИ УПРАЖНЕНИЙ
Если просят упражнение, сгенерируй РОВНО 5 заданий. 
ВАЖНО: Сначала выдай ТОЛЬКО задания. Не пиши ответы сразу. Напиши: "Жду твои ответы! Напиши их, и я проверю, либо попроси 'дай ключи'".

# ЗАЩИТА ОТ ГАЛЛЮЦИНАЦИЙ
- ЭСПЕРАНТО: Нет исключений.
- СИНДАРИН: Не путай с Квенья. Не выдумывай слова.
- БЕЛОРУССКИЙ: Учитывай разницу наркомовки и тарашкевицы.
"""

# Настройки локальных моделей
LLM_MODEL = "qwen3.5:2b"       # Отлично следует инструкциям и знает русский
EMBED_MODEL = "nomic-embed-text" # Стандарт де-факто для локального RAG

# Настройка LlamaIndex на использование Ollama
try:
    # Проверяем, запущена ли Ollama
    requests.get("http://localhost:11434", timeout=2)
    
    Settings.llm = Ollama(
        model=LLM_MODEL, 
        request_timeout=120.0, # Увеличиваем таймаут для локальных моделей (особенно на CPU)
        temperature=0.1
    )
    Settings.embed_model = OllamaEmbedding(model_name=EMBED_MODEL)
    
except requests.exceptions.ConnectionError:
    st.error("❌ Не удалось подключиться к Ollama. Убедитесь, что Ollama запущена (ollama serve) и модели скачаны.")
    st.stop()

# ==========================================
# 2. ИНИЦИАЛИЗАЦИЯ БАЗЫ ЗНАНИЙ И RAG
# ==========================================

LANGUAGES = {
    "Французский": "french_kb",
    "Белорусский": "belarusian_kb",
    "Эсперанто": "esperanto_kb",
    "Синдарин": "sindarin_kb"
}

@st.cache_resource(show_spinner="🔄 Инициализация локальной базы знаний и векторного хранилища... (это может занять минуту)")
def initialize_rag():
    """Загружает документы, добавляет метаданные и создает индексы ChromaDB."""
    chroma_client = chromadb.PersistentClient(path="./chroma_db_local")
    indices = {}
    
    for lang_name, folder_name in LANGUAGES.items():
        folder_path = Path(folder_name)
        if not folder_path.exists():
            st.warning(f"⚠️ Папка {folder_name} не найдена. Пропускаем.")
            continue
            
        # Загрузка документов
        reader = SimpleDirectoryReader(input_dir=str(folder_path))
        docs = reader.load_data()
        
        # КРИТИЧЕСКИ ВАЖНО: Добавляем метаданные для изоляции контекста
        for doc in docs:
            doc.metadata["language"] = lang_name
            
        # Создание коллекции в ChromaDB для каждого языка отдельно
        collection_name = LANGUAGES[lang_name]
        chroma_collection = chroma_client.get_or_create_collection(collection_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        # Построение индекса с использованием локальных эмбеддингов
        index = VectorStoreIndex.from_documents(
            docs, 
            storage_context=storage_context, 
            show_progress=True
        )
        indices[lang_name] = index
        
    return indices

# ==========================================
# 3. STREAMLIT UI
# ==========================================

st.set_page_config(page_title="Polyglot RAG Tutor (Local)", page_icon="🦙", layout="wide")

# Инициализация
indices = initialize_rag()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("🦙 Polyglot RAG (Local)")
    st.markdown(f"**LLM:** `{LLM_MODEL}`\n**Embeddings:** `{EMBED_MODEL}`")
    st.divider()
    
    st.markdown("Выберите язык для изучения:")
    selected_lang = st.selectbox("Целевой язык:", list(LANGUAGES.keys()))
    
    st.divider()
    st.markdown("### 💡 Подсказки для демо:")
    st.markdown("- **Эсперанто:** 'Разбери слово malkomprenebla'")
    st.markdown("- **Синдарин:** 'Как будет \"орки\" во мн.ч. и почему?'")
    st.markdown("- **Белорусский:** 'Чем отличается тарашкевица от наркомовки?'")
    st.markdown("- **Французский:** 'Дай упражнение на Passé Composé'")
    
    if st.button("🗑️ Очистить историю чата"):
        st.session_state.messages = []
        st.rerun()

# Main Chat Area
st.title(f"🎓 Тьютор: {selected_lang}")
st.caption("Работает полностью локально через Ollama. Данные не покидают ваш компьютер.")

# Отображение истории чата
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Поле ввода
if prompt := st.chat_input(f"Спросите про {selected_lang}..."):
    # Добавляем запрос пользователя в историю
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Генерация ответа с использованием RAG
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        if selected_lang not in indices:
            full_response = f"⚠️ База знаний для языка '{selected_lang}' не загружена. Проверьте наличие папки {LANGUAGES.get(selected_lang, 'unknown')}."
            message_placeholder.markdown(full_response)
        else:
            # Получаем индекс для выбранного языка
            index = indices[selected_lang]
            
            # Создаем Chat Engine с нашим кастомным системным промптом
            chat_engine = index.as_chat_engine(
                chat_mode="context",
                system_prompt=SYSTEM_PROMPT,
                verbose=False # Поставь True, если хочешь видеть в консоли, какие чанки взял RAG
            )
            
            # Формируем контекст из истории для LLM
            chat_history = []
            for msg in st.session_state.messages[:-1]: # Все кроме текущего
                chat_history.append({"role": msg["role"], "content": msg["content"]})
                
            # Асинхронный или синхронный запрос к локальной LLM
            # Используем streamer для красивого посимвольного вывода в Streamlit
            response = chat_engine.stream_chat(prompt, chat_history=chat_history)
            
            # Посимвольный вывод (streaming)
            for chunk in response.response_gen:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)

    # Сохраняем ответ ассистента
    st.session_state.messages.append({"role": "assistant", "content": full_response})
