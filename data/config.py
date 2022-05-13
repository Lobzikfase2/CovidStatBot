from environs import Env

env = Env()
env.read_env()

# С помощью библиотеки Env, извлекаем приватную информацию
# из файла .env
BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("ip")
