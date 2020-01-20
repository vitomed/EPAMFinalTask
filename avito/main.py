import requests
from bs4 import BeautifulSoup as bs
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
        print(data)
        adddata.append(data)
    return adddata


def search_data(routs, city, concat_name, limit_page, page, filename):
    while page < limit_page:
        # time.sleep(10)
        url = f"https://www.avito.ru/{routs[city]}/kvartiry/prodam?s=104&p={page}"
        page += 1
        print("cuurent page", page)
        session = requests.Session()
        resp = session.get(url, headers=HEADERS)
        if resp.status_code == 200:
            inner_info = first_pars(resp)
            app_data = second_pars(inner_info, city=concat_name)
        df = pd.DataFrame(app_data, columns=columns)
        df.to_csv(filename, mode="a", header=False, index=False)


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

    def main(routs, columns, c_abr, r_name, s_page, f_page):
        f_name = f"{c_abr}_address_price.csv"
        create_colums(columns, filename=f_name)
        search_data(routs, limit_page=f_page, page=s_page, city=f"{c_abr}", concat_name=f"{r_name}", filename=f_name)
        df = pd.read_csv(f_name, sep=",")
        print(len(df))
        print(len(df.address.unique()))
        print(len(df.price.unique()))

    # main(routs=routs, columns=columns, c_abr="SPb", r_name="Санкт-Петербург", s_page=1, f_page=5)
    # main(routs=routs, columns=columns, c_abr="EKB", r_name="Екатеринбург", s_page=1, f_page=3)
    main(routs=routs, columns=columns, c_abr="MSK", r_name="Москва", s_page=1, f_page=3)


