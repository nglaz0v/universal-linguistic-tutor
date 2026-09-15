import logging
from vkbottle.bot import Message, MessageEvent
from config import user_states, LANGUAGES
from keyboards import get_language_keyboard, get_reset_keyboard
from rag_engine import rag_engine

logger = logging.getLogger(__name__)

async def start(message: Message) -> None:
    """Обработчик команды /start"""
    user_id = message.from_id
    # Сбрасываем состояние при старте
    user_states[user_id] = None
    
    welcome_text = (
        "👋 Привет! Я — **Polyglot RAG Tutor**.\n\n"
        "Я помогу тебе изучить один из 4 языков, опираясь на строгие правила и базу знаний:\n"
        "• 🇫🇷 Французский\n"
        "• 🇧🇾 Белорусский\n"
        "• 🟢 Эсперанто\n"
        "• 🧝 Синдарин\n\n"
        "👇 **Выберите язык для начала обучения:**"
    )
    
    await message.answer(welcome_text, keyboard=get_language_keyboard())

async def handle_message(message: Message) -> None:
    """Обработка текстовых сообщений"""
    user_id = message.from_id
    text = message.text.strip()
    
    logger.info(f"Message from {user_id}: {text}")
    
    # Проверяем, выбрал ли пользователь язык
    selected_lang = user_states.get(user_id)
    if (not selected_lang) and (text in LANGUAGES.keys()):
        user_states[user_id] = text
        selected_lang = user_states[user_id]
    
    if not selected_lang:
        await message.answer(
            "⚠️ Сначала выберите язык обучения, нажав на кнопку ниже или написав /start",
            keyboard=get_language_keyboard()
        )
        return
        
    # Показываем индикатор набора текста (typing)
    await message.answer("⏳ Думаю и ищу информацию в базе знаний...")
    
    # Запрос к RAG
    response_text = await rag_engine.query(selected_lang, text)
    
    # VK имеет лимит на длину сообщения (4096 символов). 
    # Если ответ слишком длинный, обрезаем его (для MVP этого достаточно)
    if len(response_text) > 4000:
        response_text = response_text[:3900] + "\n\n... (ответ обрезан из-за лимита VK)"
        
    await message.answer(
        response_text, 
        keyboard=get_reset_keyboard()
    )

async def handle_callback(event: MessageEvent) -> None:
    """Обработка нажатий на инлайн-кнопки"""
    user_id = event.user_id
    payload = event.payload
    
    # В vkbottle payload приходит как строка, её нужно распарсить, 
    # но если мы передаем dict, vkbottle иногда делает это автоматически. 
    # На всякий случай проверяем тип.
    import json
    if isinstance(payload, str):
        payload = json.loads(payload)
        
    action = payload.get("action")
    
    if action == "select_lang":
        lang = payload.get("lang")
        user_states[user_id] = lang
        
        await event.edit_message(
            f"✅ Отлично! Вы выбрали: **{lang}**.\n\nТеперь просто напишите мне свой вопрос, попросите объяснить правило или сгенерировать упражнение!",
            keyboard=get_reset_keyboard()
        )
        
    elif action == "reset":
        user_states[user_id] = None
        await event.edit_message(
            "🔄 Возвращаемся в главное меню. Выберите язык:",
            keyboard=get_language_keyboard()
        )
        
    # Обязательно отвечаем на callback, чтобы убралась иконка загрузки в VK
    await event.show_snackbar("Действие выполнено")
