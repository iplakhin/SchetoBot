import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config.config import Config, load_config
from handlers import handlers
from keyboard.set_mainmenu import set_main_menu
from middleware.middleware import RegistrationCheck, PermissionCheck


async def main() -> None:
    config: Config = load_config()
    bot: Bot = Bot(token=config.tgbot.token, parse_mode="HTML")
    storage: MemoryStorage = MemoryStorage()
    dp: Dispatcher = Dispatcher(storage=storage)

    await set_main_menu(bot)
    dp.include_router(handlers.router)
    dp.update.outer_middleware(PermissionCheck())
    #dp.callback_query.middleware(RegistrationCheck)
    #dp.message.middleware(PermissionCheck)
    #dp.callback_query.middleware(PermissionCheck)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
