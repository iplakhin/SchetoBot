import asyncio
from aiogram import Bot, Dispatcher
from config.config import Config, load_config
from handlers import handlers
from keyboard.set_mainmenu import set_main_menu


async def main() -> None:
    config: Config = load_config()
    bot: Bot = Bot(token=config.tgbot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher()

    await set_main_menu(bot)
    dp.include_router(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
