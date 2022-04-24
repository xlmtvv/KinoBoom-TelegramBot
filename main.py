from aiogram import executor
from create_bot import dp

from handlers import set_up_handlers

set_up_handlers.register_handlers(dp)
if __name__ == '__main__':
    executor.start_polling(dp)
