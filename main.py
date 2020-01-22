import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import time


def create_colums(columns, f_name):
    """

    :param columns:
    :param f_name:
    :return:
    """
    df = pd.DataFrame(columns=columns)
    df.to_csv(f_name, index=False)


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


def search_data(routs,city,concat_name, limit_page, page, save_f_name):
    """

    :param routs:
    :param city:
    :param concat_name:
    :param limit_page:
    :param page:
    :param f_name:
    :return:
    """
    while page < limit_page:
        time.sleep(10)
        url = f"https://realty.yandex.ru/{routs[city]}/kupit/kvartira/?page={page}"
        page += 1
        print("cuurent page", page)
        session = requests.Session()
        resp = session.get(url, headers=HEADERS)
        try:
            assert resp.status_code == 200, f"NOTE! {resp.status_code}"
        except Exception as e:
            print(e)
        else:
            inner_info = first_pars(resp)
            add_data = second_pars(inner_info, city=concat_name)
            update_df(add_data, columns=columns, f_name=save_f_name)


def update_df(data, columns, f_name):
    """

    :param data:
    :param columns:
    :param filename:
    :return:
    """
    df = pd.DataFrame(data, columns=columns)
    df = df.drop_duplicates("address")
    df.to_csv(f_name, mode="a", header=False, index=False)


def clear_df(f_name):
    df = pd.read_csv(f_name, sep=",")
    clear_df = df.drop_duplicates("address")
    clear_df.to_csv(f_name, index=False)


def main(routs, columns, c_abr, r_name, s_page, f_page):
    f_name = f"{c_abr}_address_price.csv"
    create_colums(columns, f_name=f_name)
    search_data(routs, limit_page=f_page, page=s_page, city=f"{c_abr}", concat_name=f"{r_name}", save_f_name=f_name)
    clear_df(f_name)
    df = pd.read_csv(f_name, sep=",")
    print(len(df))
    print(len(df.address.unique()))
    print(len(df.price.unique()))


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

    main(routs=routs, columns=columns, c_abr="SPb", r_name="Санкт-Петербург", s_page=0, f_page=1)
    # main(routs=routs, columns=columns, c_abr="EKB", r_name="Екатеринбург", s_page=1, f_page=3)
    # main(routs=routs, columns=columns, c_abr="MSK", r_name="Москва", s_page=0, f_page=2)


