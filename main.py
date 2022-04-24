from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as fmt

from tmdbv3api import TMDb, Movie, Discover, TV
from config import TMDB_API, TK
from parsing_kinopoisk import list_movies_txt
import asyncio

from constants import message_start, message_help, message_info

TOKEN = TK
bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)


# import all for TMDb
tmdb = TMDb()
tmdb.api_key = TMDB_API
tmdb.language = 'ru'
tmdb.debug = True
tv = TV()
movie = Movie()

# answer for /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["🆘help", '💡info']
    keyboard.add(*buttons)
    await message.reply(message_start, reply_markup=keyboard)



# Answer for keyboard help
@dp.message_handler(lambda message: message.text == "🆘help")
async def keyboard_help_button(message: types.Message):
    await message.reply(message_help)


# answer for keyboard about
@dp.message_handler(lambda message: message.text == "💡info")
async def keyboard_info_button(message: types.Message):
    await message.reply(
        f'''{fmt.hide_link('https://www.themoviedb.org')}{message_info}''')


# answer for /help
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(message_help)


# answer for keyboard about
@dp.message_handler(commands='info')
async def process_info_command(message: types.Message):
    # link_to_tmdb = fmt.link('TMDb', 'https://www.themoviedb.org')
    await message.reply(
        f'''{fmt.hide_link('https://www.themoviedb.org')}Данный бот сделан с целью помощи в выборе и поиске кино

Если у вас есть идеи для улучшения бота,пожелания или жалобы - обращайтесь к @mutaliyevv

/help - для помощи в навигации

This bot uses TMDb api''')

# Answer  for /popular
@dp.message_handler(commands=['top_serials'])
async def top_serials(message: types.Message):
    discover = Discover()
    serial = discover.discover_tv_shows({
        'sort_by': 'popularity.desc'
    })
    text_serials = '''🔝Популярные сериалы сейчас:\n\n'''
    for ser in serial:
        text_serials += '📺Название: ' + str(ser.name) + '\n📅 Дата выхода: ' + getattr(
            ser, 'first_air_date', 'n/a') + '\n' + '📌Ссылка: https://www.themoviedb.org/tv/' + str(ser.id) + '\n\n'
    await message.answer(text_serials)


# handler for top_movies
@dp.message_handler(commands=['top_movies'])
async def top_movies(message: types.Message):
    await message.answer(list_movies_txt)

#handler for now
@dp.message_handler(commands=['now'])
async def afisha_now(message: types.Message):
    from datetime import datetime, timedelta
    current_date = datetime.now().date()
    N_DAYS_AGO = 30
    n_days_ago = current_date - timedelta(days=N_DAYS_AGO)

    discover = Discover()
    afisha = discover.discover_movies({
        'primary_release_date.gte': n_days_ago,
        'primary_release_date.lte': current_date,
        'sort_by': 'vote_average.desc',
        'vote_count.gte': 70
    })
    text_for_afisha = '''🆕Афиша фильмов:\n\n'''
    for i in afisha:
        text_for_afisha += ('🎬Название: ' + i['title'] + '\n' + '📅Дата выхода: ' + i[
            'release_date'] + '\n' + '📌Ссылка: ' + 'https://www.themoviedb.org/movie/' + str(i['id']) + '\n\n')

    await message.answer(text_for_afisha)


# handler for popular
@dp.message_handler(commands=['popular'])
async def popular_movies_serials(message: types.Message):
    from constants import popular_films
    await message.answer(popular_films)

#handler for soon films
@dp.message_handler(commands=['soon'])
async def soon_release(message: types.Message):
    from datetime import datetime, timedelta
    current_date = datetime.now().date()
    n_days_frw = current_date + timedelta(days=150)

    discover = Discover()
    soonfilms = discover.discover_movies({
        'primary_release_date.gte': current_date,
        'primary_release_date.lte': n_days_frw,
    })
    text_for_soon = '''🔜Самые ожидаемые фильмы:\n\n'''
    for i in soonfilms[:12]:
        text_for_soon += ('🎬Название: ' + i['title'] + '\n' + '📅Дата выхода: ' + i[
            'release_date'] + '\n' + '📌Ссылка: ' + 'https://www.themoviedb.org/movie/' + str(i['id']) + '\n\n')
    await message.answer(text_for_soon)

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def search_films(msg: types.Message):
    tittle = msg.text
    if tittle[0] not in ('/<>@#$%^&*()_-={}[]\|:;.,`?'):
        search_movies = movie.search(tittle)
        search_shows = tv.search(tittle)
        text = '''⬇🔎Результаты поискa по фильмам: \n\n'''
        # Parsing flims
        for res in search_movies[:10]:
            text += '🎬Название: ' + str(res.title) + '\n📅 Дата выхода: ' + getattr(
                res, 'release_date', 'n/a') + '\n' + '📌Ссылка: https://www.themoviedb.org/movie/' + str(res.id) + '\n\n'
        text += '''⬇🔎Результаты поискa по сериалам: \n\n'''
        # Parsing serials
        for shows in search_shows[:10]:
            text += '📺Название: ' + str(shows.name) + '\n📅 Дата выхода: ' + getattr(
                shows, 'first_air_date', 'n/a') + '\n' + '📌Ссылка: https://www.themoviedb.org/tv/' + str(shows.id) + '\n\n'
        # Test films and serials are more than 0
        if len(search_shows)+len(search_movies) > 0 :
            await bot.send_message(msg.from_user.id, text)
        else:
            await bot.send_message(msg.from_user.id, '❌По данному запросу ничего не найдено')
    else:
        await bot.send_message(msg.from_user.id, '❌По данному запросу ничего не найдено')


# answer for unknown messages
@dp.message_handler(content_types=types.ContentTypes.ANY)
async def unknown_message(msg: types.Message):
    message_text = 'Я не понимаю тебя :(\nХочу тебе напомнить,что у меня есть команда /help'
    await bot.send_message(msg.from_user.id, message_text)


if __name__ == '__main__':
    executor.start_polling(dp)
