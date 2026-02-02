from app.bot.consts import labels_texts

NOT_DATETIME_COLUMN = (
    f'⚠️ Таблица должна содержать колонку "{labels_texts.COLUMN_DATETIME_NAME}"'
)
INCORRECT_DATETIME_FORMAT = 'Неверный формат даты или времени'
INCORRECT_DATETIME_MOMENT = 'Время должно быть больше, чем настоящий момент'
