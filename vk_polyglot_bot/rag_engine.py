import os
import logging
from pathlib import Path
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.langchain import LangChainLLM
from llama_index.embeddings.openai import OpenAIEmbedding
from langchain_openai import ChatOpenAI
from config import LANGUAGES, SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class RAGEngine:
    def __init__(self):
        logger.info("🔄 Инициализация RAG движка...")
        
        # Настройка LLM (используем GPT-4o или GPT-3.5-turbo для скорости/экономики)
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
        
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db_vk")
        self.indices = {}
        
        for lang_name, folder_name in LANGUAGES.items():
            folder_path = Path(folder_name)
            if not folder_path.exists():
                logger.warning(f"⚠️ Папка {folder_name} не найдена. Пропускаем.")
                continue
                
            logger.info(f"📚 Загрузка документов для: {lang_name}")
            reader = SimpleDirectoryReader(input_dir=str(folder_path))
            docs = reader.load_data()
            
            # Добавляем метаданные для изоляции
            for doc in docs:
                doc.metadata["language"] = lang_name
                
            collection_name = LANGUAGES[lang_name]
            chroma_collection = self.chroma_client.get_or_create_collection(collection_name)
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            
            self.indices[lang_name] = VectorStoreIndex.from_documents(
                docs, storage_context=storage_context, show_progress=False
            )
            
        logger.info("✅ RAG движок успешно инициализирован!")

    async def query(self, language: str, prompt: str) -> str:
        """Выполняет запрос к RAG для конкретного языка."""
        if language not in self.indices:
            return "❌ Ошибка: База знаний для этого языка не загружена."
            
        index = self.indices[language]
        
        # Создаем chat engine с системным промптом
        chat_engine = index.as_chat_engine(
            chat_mode="context",
            system_prompt=SYSTEM_PROMPT,
            verbose=False
        )
        
        try:
            # Используем асинхронный вызов для совместимости с vkbottle
            response = await chat_engine.achat(prompt)
            return response.response
        except Exception as e:
            logger.error(f"Ошибка при запросе к LLM: {e}")
            return "⚠️ Произошла ошибка при обработке запроса. Попробуйте позже."

# Глобальный экземпляр (синглтон)
rag_engine = RAGEngine()
