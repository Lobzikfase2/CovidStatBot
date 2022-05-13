from aiogram import types


async def set_default_commands(dp):
    """
    Задаёт список команд, доступных в боте
    """
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Начать"),
            types.BotCommand("stats", "Статистика"),
            types.BotCommand("options", "Настройки"),
            types.BotCommand("help", "Cправка"),
        ]
    )
