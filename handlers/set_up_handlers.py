from sys import set_coroutine_origin_tracking_depth
from create_bot import bot, dp
from tmdbv3api import TMDb, Movie, Discover, TV
from aiogram import Dispatcher, types
from constants import message_start, message_help, message_info, popular_films
import aiogram.utils.markdown as fmt
from tmdbv3api import Discover
from parsing_kinopoisk import list_movies_txt
from config import TMDB_API

# setting tmdb
tmdb = TMDb()
tv = TV()
movie = Movie()
tmdb.api_key = TMDB_API
tmdb.language = 'ru'
tmdb.debug = True

# handler for /start
async def start_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["🆘help", '💡info']
    keyboard.add(*buttons)
    await message.reply(message_start, reply_markup=keyboard)



# handler for keyboard button help
async def keyboard_help_button(message: types.Message):
    await message.reply(message_help)


# handler for keyboard button info
async def keyboard_info_button(message: types.Message):
    await message.reply(
        f'''{fmt.hide_link('https://www.themoviedb.org')}{message_info}''')


# handler for /help
async def process_help_command(message: types.Message):
    await message.reply(message_help)


# handler for command info
async def process_info_command(message: types.Message):
    # link_to_tmdb = fmt.link('TMDb', 'https://www.themoviedb.org')
    await message.reply(
        f'''{fmt.hide_link('https://www.themoviedb.org')}{message_info}''')

# handler and parsing /top_series
async def top_series(message: types.Message):
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
async def top_movies(message: types.Message):
    await message.answer(list_movies_txt)

#handler and parsing for /now
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
async def popular_movies_serials(message: types.Message):
    await message.answer(popular_films)

#handler and parsing /soon
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

#  This is a function that searches for a movie or series by the title that the user will send to the chat
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
async def unknown_message(msg: types.Message):
    message_text = 'Я не понимаю тебя :(\nХочу тебе напомнить,что у меня есть команда /help'
    await bot.send_message(msg.from_user.id, message_text)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(keyboard_help_button, lambda message: message.text == "🆘help")
    dp.register_message_handler(keyboard_info_button, lambda message: message.text == "💡info")
    dp.register_message_handler(process_help_command, commands=['help'])
    dp.register_message_handler(process_info_command, commands=['info'])
    dp.register_message_handler(top_series, commands=['top_series'])
    dp.register_message_handler(top_movies, commands=['top_movies'])
    dp.register_message_handler(afisha_now, commands=['now'])
    dp.register_message_handler(popular_movies_serials, commands=['popular'])
    dp.register_message_handler(soon_release, commands=['soon'])
    dp.register_message_handler(search_films, content_types=types.ContentTypes.TEXT)
    dp.register_message_handler(unknown_message, content_types=types.ContentTypes.ANY)