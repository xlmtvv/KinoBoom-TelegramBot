from aiogram import Bot, Dispatcher
from config import TK as TOKEN

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)