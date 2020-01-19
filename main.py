import itertools
import requests
from bs4 import BeautifulSoup as bs
from collections import Counter
import re
import pandas as pd
import time


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
    """

    :param routs:
    :param city:
    :param concat_name:
    :param limit_page:
    :param page:
    :param filename:
    :return:
    """
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
            print(app_data)
        df2 = pd.DataFrame(app_data, columns=columns)
        df2.to_csv(filename, mode="a", header=False, index=False)


def save_data(data, columns, filename):
    """

    :param data:
    :param columns:
    :param filename:
    :return:
    """
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(filename, mode="a", header=False, index=False)


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

    # city_abr = "SPb"
    # rus_name = "Санкт-Петербург"
    # filename = f"{city_abr}_address_price.csv"
    # # create_colums(columns, filename=filename)
    # # search_data(routs, limit_page=24, page=0, city=f"{city_abr}", concat_name=f"{rus_name}", filename=filename)
    # df = pd.read_csv(filename, sep=",")
    # print(len(df))
    # geoYandex(df)

    # city_abr = "MSK"
    # rus_name = "Москва"
    # filename = f"{city_abr}_address_price.csv"
    # create_colums(columns, filename=filename)
    # search_data(routs, limit_page=24, page=0, city=f"{city_abr}", concat_name=f"{rus_name}", filename=filename)
    # df = pd.read_csv(filename, sep=",")
    # print(len(df))
    #
    # city_abr = "EKB"
    # rus_name = "Екатеринбург"
    # filename = f"{city_abr}_address_price.csv"
    # create_colums(columns, filename=filename)
    # search_data(routs, limit_page=24, page=0, city=f"{city_abr}", concat_name=f"{rus_name}", filename=filename)
    # df = pd.read_csv(filename, sep=",")
    # print(len(df))

