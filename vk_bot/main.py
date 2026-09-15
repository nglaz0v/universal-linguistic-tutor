import sys
import os
import logging
from dotenv import load_dotenv

from vkbottle import Bot, GroupEventType
from vkbottle.bot import BotLabeler, Message, MessageEvent

# Добавляем текущую директорию в путь, чтобы импорты работали
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Загрузка переменных окружения
load_dotenv()

from handlers import start, handle_message, handle_callback
# Импортируем rag_engine здесь, чтобы он инициализировался при запуске main.py
import rag_engine 

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Создаем лейблер
labeler = BotLabeler()

@labeler.message(text=["/start", "Старт", "Начать"])
async def start_handler(message: Message) -> None:
    """Обрабатывает команду /start"""
    await start(message)

@labeler.message()
async def message_handler(message: Message) -> None:
    """Обрабатывает все текстовые сообщения"""
    await handle_message(message)

@labeler.raw_event(GroupEventType.MESSAGE_EVENT, MessageEvent)
async def callback_handler(event: MessageEvent) -> None:
    """Обрабатывает callback-события от кнопок"""
    await handle_callback(event)

def main() -> None:
    """Запуск бота."""
    token = os.getenv('VK_GROUP_TOKEN')
    if not token:
        print("❌ Токен не установлен. Установите: export VK_GROUP_TOKEN='ваш_токен'")
        return

    # Проверяем наличие ключа OpenAI
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY не установлен в .env файле!")
        return

    bot = Bot(token=token, labeler=labeler)
    
    print("🤖 VK бот Polyglot RAG Tutor запущен...")
    print("📱 Используйте /start для начала работы")
    print("⏹️  Для остановки нажмите Ctrl+C")

    bot.run_forever()

if __name__ == "__main__":
    main()
