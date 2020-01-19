import itertools
import requests
from bs4 import BeautifulSoup as bs
from collections import Counter
import re
import pandas as pd
import time

def main(session, HEADERS, limit_articles=100, initial_page=0):
    """Функция, кторая вернет список всех найденных
    тегов по всем статьям.
    Вы можете назначить лимит статей (limit_articles), по которым хотите собрать теги,
    а также начальную страницу, с которой хотите начать поиск информации (initial_page.
    Опционально, вторым параметром, функция вернет словарь {название статьи : список ее тегов}"""

    head_article = {}
    tags_list = []
    count_articles = 0
    current_page = initial_page
    # list_for_len_articles = []
    while count_articles < limit_articles:
        resp = session.get(f"https://pikabu.ru/new/subs?of=v2&subs=1&_=1577034698730&page={current_page}",
                           headers=HEADERS)
        print("current page", current_page)
        current_page += 1

        if resp.status_code == 200:
            soup = bs(resp.content, "html.parser")
            artic_curr_page = soup.find_all("article", {"class": "story"})
            if not len(artic_curr_page):
                print(f"Exist articles on page {current_page - 1}")
                continue
            artic_curr_page.pop()  # последний элемент в списке - это рекламная информация на странице, выкидываем его

            for i, article in enumerate(artic_curr_page):
                count_articles += 1
                if count_articles == limit_articles:
                    break
                new_tags = [k.get("data-tag") for k in article.find_all("a", {"class": "tags__tag", "data-tag": True})]
                tags_list.append(new_tags)
                head_article[article.a.text] = new_tags

            print("count_articles", count_articles)
        else:
            print("Неудача, смотри код ошибки", resp.status_code)
            break
    return tags_list, head_article


def counter(tags_list):
    """Функция осуществялет подсчет слов, переданных в списке wordcouтt
    и сортирует в зависимости от частоты появления тега в статье
    в порядке убывания
    Возвращает отсортированный tulpe - (Название тега, сколько раз он встретился в статьях)
    """

    unpaced_tags_list = list(itertools.chain.from_iterable(tags_list))
    counter_words = Counter(unpaced_tags_list)
    count_words = {word: counter_words[word] for word in unpaced_tags_list}
    sort_count_words = sorted(count_words.items(), key=lambda x: x[1], reverse=True)

    return sort_count_words


def final_str_for_writing(sort_count_words, elements=None):
    """Функция берет количество первых N элементов и преобразует их
    для последующей записи в файл
    """
    note_str = ""
    if elements is None:
        elements = 11
    for index, elem in enumerate(sort_count_words, start=1):
        if index == elements:
            break
        note_str += f"({index}) {elem[0]} : {elem[1]}\n"
    return note_str


def create_colums(columns, filename):
    """

    :param columns:
    :param filename:
    :return:
    """
    df = pd.DataFrame(columns=columns)
    df.to_csv(filename, index=False)

def first_pars(resp):
    """

    :param resp:
    :return:
    """
    soup = bs(resp.content, "html.parser")
    return soup.findAll("div", {"class": "OffersSerpItem__info-inner"})


def second_pars(inner_info, city,pattern = "\d+"):
    """

    :param inner_info:
    :param pattern:
    :param city:
    :return:
    """
    adddata = []
    for info in inner_info:
        address = info.findAll("div", {"class": "OffersSerpItem__address"})
        price_m2 = info.findAll("div", {"class": "OffersSerpItem__price-detail"})  # цена снизу
        data = [f"{city}, {address[0].text}", int("".join(re.findall(pattern, price_m2[0].text)))]
        adddata.append(data)
    return adddata


def search_data(routs,city,concat_name, limit_page, page, filename):
    while page < limit_page:
        time.sleep(10)
        url = f"https://realty.yandex.ru/{routs[city]}/kupit/kvartira/?page={page}"  # url2
        page += 1
        print("cuurent page", page)
        session = requests.Session()
        resp = session.get(url, headers=HEADERS)
        if resp.status_code == 200:
            inner_info = first_pars(resp)
            app_data = second_pars(inner_info, city=concat_name)
        df2 = pd.DataFrame(app_data, columns=columns)
        df2.to_csv(filename, mode="a", header=False, index=False)

def save_data(data, columns, filename):
    """

    :param data:
    :param columns:
    :param filename:
    :return:
    """
    df2 = pd.DataFrame(data, columns=columns)
    df2.to_csv(filename, mode="a", header=False, index=False)

def read_pdframe(filename):
    df = pd.read_csv(filename, sep=",")
    return df

def geoYandex(data):
    for _, adr in enumerate(data):
        addr = adr


if __name__ == "__main__":

    COOKIE = ""
    with open("cookie.txt", "r") as cookie_file:
        for line in cookie_file:
            COOKIE += line.strip()

    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                  "*/*;q=0.8",
        "Cookie": f"{COOKIE}",
        "User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/'
                      '20100101 Firefox/71.0',
    }

    routs = {"SPb": "sankt-peterburg", "MSK": "moskva", "EKB":"ekaterinburg"}
    columns = ["address", "price"]

    city_abr = "SPb"
    rus_name = "Санкт-Петербург"
    filename = f"{city_abr}_address_price.csv"
    create_colums(columns, filename=filename)
    search_data(routs, limit_page=24, page=0, city=f"{city_abr}", concat_name=f"{rus_name}", filename=filename)
    df = pd.read_csv(filename, sep=",")
    print(len(df))
    geoYandex(df)

    city_abr = "MSK"
    rus_name = "Москва"
    filename = f"{city_abr}_address_price.csv"
    create_colums(columns, filename=filename)
    search_data(routs, limit_page=24, page=0, city=f"{city_abr}", concat_name=f"{rus_name}", filename=filename)
    df = pd.read_csv(filename, sep=",")
    print(len(df))

    city_abr = "EKB"
    rus_name = "Екатеринбург"
    filename = f"{city_abr}_address_price.csv"
    create_colums(columns, filename=filename)
    search_data(routs, limit_page=24, page=0, city=f"{city_abr}", concat_name=f"{rus_name}", filename=filename)
    df = pd.read_csv(filename, sep=",")
    print(len(df))



