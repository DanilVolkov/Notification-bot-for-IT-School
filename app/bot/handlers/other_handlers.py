import logging
from datetime import datetime
from typing import Any

import pandas as pd
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput
from pandas import DataFrame

from app.bot.consts import errors_descriptions, labels_texts

logger = logging.getLogger(__name__)


async def no_text(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
):
    await message.answer(labels_texts.NO_TEXT)


def set_red_question(text):
    return f'{text}❓'


def datetime_check(text: Any) -> str:
    try:
        planned_datetime = datetime.strptime(text, '%d.%m.%Y %H:%M')
    except:  # noqa
        raise ValueError(errors_descriptions.INCORRECT_DATETIME_FORMAT)  # noqa
    if planned_datetime <= datetime.now():
        raise ValueError(errors_descriptions.INCORRECT_DATETIME_MOMENT)
    return text


async def error_datetime(
    message: Message,
    widget: ManagedTextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    logger.debug(f'Ошибка при добавлении даты и времени: {error}')
    if errors_descriptions.INCORRECT_DATETIME_FORMAT in str(error):
        await message.answer(labels_texts.ERROR_TYPE_DATETIME)
    else:
        await message.answer(labels_texts.ERROR_DATETIME)


def check_correct_table(file_path: str) -> tuple[bool, str, DataFrame]:
    try:
        df: DataFrame = pd.read_excel(file_path)
        df.fillna('', inplace=True)

        if labels_texts.COLUMN_DATETIME_NAME not in df.columns:
            return False, errors_descriptions.NOT_DATETIME_COLUMN, df

        invalid_dates = []
        for idx, date in enumerate(df[labels_texts.COLUMN_DATETIME_NAME]):
            # убираем секунды
            date_str = (
                str(date)[:-3] if str(date).count(':') == 2 else str(date)
            )

            # пытаемся менять формат даты, если он неверный
            try:
                excel_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                date_str = excel_date.strftime('%d.%m.%Y %H:%M')
            except:  # noqa
                pass

            if date_str:
                try:
                    datetime_check(date_str)
                except ValueError as ex:
                    error_description = (
                        errors_descriptions.INCORRECT_DATETIME_FORMAT
                    )
                    if errors_descriptions.INCORRECT_DATETIME_MOMENT in str(
                        ex
                    ):
                        error_description = (
                            errors_descriptions.INCORRECT_DATETIME_MOMENT
                        )

                    invalid_dates.append(
                        f'➡️ Строка {idx + 2}: {date_str} - {error_description}'
                    )

        if invalid_dates:
            err_msg = '⚠️ Некорректные даты:\n' + '\n'.join(invalid_dates)
            return False, err_msg, df

        return True, '', df

    except Exception as ex:
        logger.error(f'Ошибка чтения таблицы: {ex}')
        return False, labels_texts.ERROR_WORK_EXCEL, pd.DataFrame()


def check_user_fio(user_fio: str) -> str:
    fio = user_fio.strip().split()
    if len(fio) == 3 and all(map(lambda s: s.isalpha(), fio)):
        return user_fio
    raise ValueError
