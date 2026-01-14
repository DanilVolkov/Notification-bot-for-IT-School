import logging

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs

from app.bot.handlers.start_session import start_session_router
from config.config import Config
from app.bot.dialogs.main_menu.dialogs import main_menu_dialog
# from app.bot.dialogs.unknown_users.dialogs import unknown_user_dialog

logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main(config: Config) -> None:
    logger.info("Starting bot...")
    # # Инициализируем хранилище
    # storage = RedisStorage(
    #     redis=Redis(
    #         host=config.redis.host,
    #         port=config.redis.port,
    #         db=config.redis.db,
    #         password=config.redis.password,
    #         username=config.redis.username,
    #     )
    # )

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    #dp = Dispatcher(storage=storage)
    dp = Dispatcher()

    # Создаём пул соединений с Postgres
    # db_pool: psycopg_pool.AsyncConnectionPool = await get_pg_pool(
    #     db_name=config.db.name,
    #     host=config.db.host,
    #     port=config.db.port,
    #     user=config.db.user,
    #     password=config.db.password,
    # )

    # Подключаем роутеры в нужном порядке
    logger.info("Including routers...")
    dp.include_routers(start_session_router, main_menu_dialog)

    # Подключаем миддлвари в нужном порядке
    logger.info("Including middlewares...")
    # dp.update.middleware(DataBaseMiddleware())
    # dp.update.middleware(ShadowBanMiddleware())
    # dp.update.middleware(ActivityCounterMiddleware())
    # dp.update.middleware(LangSettingsMiddleware())
    # dp.update.middleware(TranslatorMiddleware())

    # Запускаем поллинг
    setup_dialogs(dp)
    await dp.start_polling(bot)
    # try:
    #     await dp.start_polling(
    #         bot, db_pool=db_pool,
    #         translations=translations,
    #         locales=locales,
    #         admin_ids=config.bot.admin_ids
    #     )
    # except Exception as e:
    #     logger.exception(e)
    # finally:
    #     # Закрываем пул соединений
    #     await db_pool.close()
    #     logger.info("Connection to Postgres closed")