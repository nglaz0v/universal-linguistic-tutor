import streamlit as st
import chromadb
import os
from pathlib import Path

# --- LlamaIndex & LangChain Imports ---
from llama_index.core import (
    VectorStoreIndex, 
    SimpleDirectoryReader, 
    Settings, 
    StorageContext,
    Document
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.langchain import LangChainLLM
from llama_index.embeddings.openai import OpenAIEmbedding
from langchain_openai import ChatOpenAI

# ==========================================
# 1. КОНФИГУРАЦИЯ И СИСТЕМНЫЙ ПРОМПТ
# ==========================================

# Убедись, что у тебя установлен API ключ OpenAI (например, через переменную окружения)
# os.environ["OPENAI_API_KEY"] = "sk-..." 
# Или используй st.secrets для Streamlit

SYSTEM_PROMPT = """# РОЛЬ И МИССИЯ
Ты — «Универсальный Лингвистический Тьютор» (Polyglot RAG). Твоя цель — помогать пользователю изучать языки, опираясь СТРОГО на предоставленную базу знаний. Ты общаешься с пользователем на русском языке, но обучаешь его целевому иностранному или вымышленному языку.

# АРХИТЕКТУРА И ИЗОЛЯЦИЯ КОНТЕКСТА (КРИТИЧЕСКИ ВАЖНО)
Твоя база знаний разделена на 4 независимых языковых домена:
1. Французский (реальный, романская группа)
2. Белорусский (реальный, славянская группа, особенности: аканне, дзеканне, тарашкевіца/наркамаўка)
3. Эсперанто (искусственный, абсолютно регулярный, без исключений)
4. Синдарин (вымышленный, эльфийский, строгие алгоритмические правила: мутации, i-аффония)

ПРАВИЛО ИЗОЛЯЦИИ: Прежде чем ответить, определи, какой язык имеет в виду пользователь. 
- Если извлеченный RAG-контекст относится к ДРУГОМУ языку — ИГНОРИРУЙ этот контекст. 
- Никогда не применяй правила одного языка к другому. 
- Если в контексте нет информации по запрошенному языку, честно скажи: "В предоставленных материалах по этому языку данное правило не детализировано".

# ПРИНЦИПЫ ОБУЧЕНИЯ И ФОРМАТ ОТВЕТА
1. Структурированность: Всегда используй Markdown. Выделяй жирным шрифтом ключевые слова.
2. Декомпозиция: Разбирай сложные слова на морфемы (особенно в Эсперанто и Синдарине).
3. Контекст чтения: Приводи примеры из литературного или лорного контекста.
4. Разбор ошибок: Хвали за попытку, указывай на ошибку, объясняй правило.

# ФОРМАТ ГЕНЕРАЦИИ УПРАЖНЕНИЙ
Если пользователь просит упражнение, сгенерируй РОВНО 5 заданий.
ВАЖНО: Сначала выдай ТОЛЬКО задания. Не пиши ответы сразу. Напиши: "Жду твои ответы! Напиши их, и я проверю, либо попроси 'дай ключи'".

# ЗАЩИТА ОТ ГАЛЛЮЦИНАЦИЙ
- ЭСПЕРАНТО: Нет исключений.
- СИНДАРИН: Не путай с Квенья. Не выдумывай слова.
- БЕЛОРУССКИЙ: Учитывай разницу наркомовки и тарашкевицы.
"""

# Настройки LlamaIndex
# Подключаем LangChain LLM в LlamaIndex (демонстрируем связку стеков)
lc_llm = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("API_BASE_URL"),
    model=os.getenv("LLM_MODEL_NAME"),
    temperature=0.1
)
Settings.llm = LangChainLLM(llm=lc_llm)
Settings.embed_model = OpenAIEmbedding(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base=os.getenv("API_BASE_URL"),
    model=os.getenv("EMBEDDING_MODEL_NAME"),
)

# ==========================================
# 2. ИНИЦИАЛИЗАЦИЯ БАЗЫ ЗНАНИЙ И RAG
# ==========================================

LANGUAGES = {
    "Французский": "french_kb",
    "Белорусский": "belarusian_kb",
    "Эсперанто": "esperanto_kb",
    "Синдарин": "sindarin_kb"
}

@st.cache_resource(show_spinner="Инициализация базы знаний и векторного хранилища...")
def initialize_rag():
    """Загружает документы, добавляет метаданные и создает индексы ChromaDB."""
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    indices = {}
    
    for lang_name, folder_name in LANGUAGES.items():
        folder_path = Path(folder_name)
        if not folder_path.exists():
            st.warning(f"Папка {folder_name} не найдена. Пропускаем.")
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
        
        # Построение индекса
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

st.set_page_config(page_title="Polyglot RAG Tutor", page_icon="📚", layout="wide")

# Инициализация
indices = initialize_rag()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("🌍 Polyglot RAG")
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
st.caption("Ассистент опирается строго на загруженную базу знаний (RAG)")

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
                
            # Запрос к LLM
            response = chat_engine.chat(
                prompt, 
                chat_history=chat_history
            )
            
            full_response = response.response
            message_placeholder.markdown(full_response)
            
    # Сохраняем ответ ассистента
    st.session_state.messages.append({"role": "assistant", "content": full_response})
