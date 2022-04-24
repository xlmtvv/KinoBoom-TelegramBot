import requests
from bs4 import BeautifulSoup
from time import sleep
def parsing_top250():
    url = f"https://www.kinopoisk.en/lists/top250/?page=1&tab=all"
    r = requests.get(url)
    sleep(1)
    soup = BeautifulSoup(r.text, 'lxml')

    films = soup.findAll('div', class_='desktop-rating-selection-film-item')
    data = []
    for film in films[:14]:
        link = "https://www.kinopoisk.ru" + film.find('a', class_='selection-film-item-meta__link').get('href')
        russian_name = film.find('a', class_='selection-film-item-meta__link').find('p',
                                                                                    class_='selection-film-item-meta__name').text
        original_name = film.find('a', class_='selection-film-item-meta__link').find('p',
                                                                                     class_='selection-film-item-meta__original-name').text
        country = film.find('a', class_='selection-film-item-meta__link').find('span',
                                                                               class_='selection-film-item-meta__meta-additional-item').text
        film_type = film.find('a', class_='selection-film-item-meta__link').findAll('span',
                                                                                    class_='selection-film-item-meta__meta-additional-item')[
            1].text
        try:
            rate = film.find('span', class_='rating__value rating__value_positive').text
        except:
            rate = '-'
        data.append([link, russian_name, original_name, country, film_type, rate])
    list_movies = '''🔝Список лучших фильмов:\n\n'''
    for movie in data:
        list_movies += f'🎬Название: {movie[1]}\n📅Дата выхода: {movie[2][-4::1]}\n📃Жанр: {movie[4]}\n📌Ссылка: {movie[0]}\n\n'
    return list_movies

# I parsed a kinopoisk and transferred the data to a constant for convenience

list_movies_txt = '''🔝Список лучших фильмов за все время:

🎬Название: Зеленая миля
📅Дата выхода: 1999
📃Жанр: драма, криминал
📌Ссылка: https://www.kinopoisk.ru/film/435/

🎬Название: Побег из Шоушенка
📅Дата выхода: 1994
📃Жанр: драма
📌Ссылка: https://www.kinopoisk.ru/film/326/

🎬Название: Властелин колец: Возвращение короля
📅Дата выхода: 2003
📃Жанр: фэнтези, приключения
📌Ссылка: https://www.kinopoisk.ru/film/3498/

🎬Название: Властелин колец: Две крепости
📅Дата выхода: 2002
📃Жанр: фэнтези, приключения
📌Ссылка: https://www.kinopoisk.ru/film/312/

🎬Название: Властелин колец: Братство Кольца
📅Дата выхода: 2001
📃Жанр: фэнтези, приключения
📌Ссылка: https://www.kinopoisk.ru/film/328/

🎬Название: Форрест Гамп
📅Дата выхода: 1994
📃Жанр: драма, комедия
📌Ссылка: https://www.kinopoisk.ru/film/448/

🎬Название: Король Лев
📅Дата выхода: 1994
📃Жанр: мультфильм, мюзикл
📌Ссылка: https://www.kinopoisk.ru/film/2360/

🎬Название: Интерстеллар
📅Дата выхода: 2014
📃Жанр: фантастика, драма
📌Ссылка: https://www.kinopoisk.ru/film/258687/

🎬Название: Тайна Коко
📅Дата выхода: 2017
📃Жанр: мультфильм, фэнтези
📌Ссылка: https://www.kinopoisk.ru/film/679486/

🎬Название: 1+1
📅Дата выхода: 2011
📃Жанр: драма, комедия
📌Ссылка: https://www.kinopoisk.ru/film/535341/

🎬Название: Криминальное чтиво
📅Дата выхода: 1994
📃Жанр: криминал, драма
📌Ссылка: https://www.kinopoisk.ru/film/342/

🎬Название: Список Шиндлера
📅Дата выхода: 1993
📃Жанр: драма, биография
📌Ссылка: https://www.kinopoisk.ru/film/329/

🎬Название: Начало
📅Дата выхода: 2010
📃Жанр: фантастика, боевик
📌Ссылка: https://www.kinopoisk.ru/film/447301/
'''