from vkbottle.tools import Keyboard, KeyboardButtonColor, Text

def get_language_keyboard() -> Keyboard:
    """Клавиатура для выбора языка"""
    kb = Keyboard(one_time=False, inline=True)
    
    languages = ["🇫🇷 Французский", "🇧🇾 Белорусский", "🟢 Эсперанто", "🧝 Синдарин"]
    
    for lang in languages:
        kb.add(
            Text(
                label=lang,
                payload={"action": "select_lang", "lang": lang}
            )
        )
        # Добавляем перенос строки после каждой кнопки для красоты
        kb.row()
        
    return kb

def get_reset_keyboard() -> Keyboard:
    """Кнопка для возврата в главное меню"""
    kb = Keyboard(one_time=False, inline=True)
    kb.add(
        Text(
            label="🔄 Сменить язык / Главное меню",
            payload={"action": "reset"}
        )
    )
    return kb
