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
    return soup.findAll("div", {"class": "item__line"})


def second_pars(inner_info, city, pattern = "\d+"):
    """

    :param inner_info:
    :param pattern:
    :param city:
    :return:
    """
    adddata = []
    for info in inner_info:
        address = info.findAll("span", {"class": "item-address__string"})
        if not len(address):
            continue

        price = info.findAll("span", {"class": "price"})
        area_m2 = info.findAll("a", {"class": "snippet-link"})
        cost_of_housing = int("".join(re.findall(pattern, price[0].text)))
        try:
            m2 = float(area_m2[0].text.split(",")[1][:-2].strip())
        except Exception as e:
            print(e)
        cost_m2 = round(cost_of_housing / m2)
        data = [f"{city}, {address[0].text.strip()}", cost_m2]
        adddata.append(data)
    return adddata


def search_data(routs,city,concat_name, limit_page, page, filename):
    while page < limit_page:
        time.sleep(10)
        url = f"https://www.avito.ru/{routs[city]}/kvartiry/prodam?cd={page}"  # url2
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

    routs = {"SPb": "sankt-peterburg", "MSK": "moskva", "EKB": "ekaterinburg"}
    columns = ["address", "price"]

    city_abr = "SPb"
    # rus_name = "Санкт-Петербург"
    filename = f"{city_abr}_address_price.csv"
    # create_colums(columns, filename=filename)
    # search_data(routs, limit_page=100, page=0, city=f"{city_abr}", concat_name=f"{rus_name}", filename=filename)
    df = pd.read_csv(filename, sep=",")
    print(len(df))
    print(df)

    city_abr = "MSK"
    # rus_name = "Москва"
    filename = f"{city_abr}_address_price.csv"
    # create_colums(columns, filename=filename)
    # search_data(routs, limit_page=100, page=0, city=f"{city_abr}", concat_name=f"{rus_name}", filename=filename)
    df = pd.read_csv(filename, sep=",")
    print(len(df))
    print(df)

    # city_abr = "EKB"
    # rus_name = "Екатеринбург"
    # filename = f"{city_abr}_address_price.csv"
    # create_colums(columns, filename=filename)
    # search_data(routs, limit_page=100, page=0, city=f"{city_abr}", concat_name=f"{rus_name}", filename=filename)
    # df = pd.read_csv(filename, sep=",")
    # print(len(df))
    # print(df)



