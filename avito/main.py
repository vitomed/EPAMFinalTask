import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import time


def create_colums(columns, f_name):
    """

    :param columns:
    :param filename:
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
        area = info.findAll("a", {"class": "snippet-link"})
        cost_of_housing = int("".join(re.findall(pattern, price[0].text)))
        try:
            area_m2 = float(area[0].text.split(",")[1][:-2].strip())
        except Exception as e:
            print(e)
        cost_m2 = round(cost_of_housing / area_m2)
        data = [f"{city}, {address[0].text.strip()}", area_m2, cost_m2]
        print(data)
        adddata.append(data)
    return adddata


def update_df(data, columns, f_name):
    """
    Если есть необходимость оставить только уникальные адреса,
    то воспользуйтесь этой функцией. Она удалит все повторения
    встречающиеся в столбце address и оставит только уникальные
    значения
    :param data:
    :param columns:
    :param filename:
    :return:
    """
    df = pd.DataFrame(data, columns=columns)
    # df = df.drop_duplicates("address")
    df.drop_duplicates("address", inplace=True)
    return df


def search_data(routs, city, concat_name, limit_page, page, save_f_name):
    while page < limit_page:
        # time.sleep(10)
        url = f"https://www.avito.ru/{routs[city]}/kvartiry/prodam/monolitnyy_dom?s=104&p={page}"
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
            single_addr_df = update_df(add_data, columns=columns, f_name=save_f_name)

            return single_addr_df



def main(routs, columns, c_abr, r_name, s_page, f_page):
    f_name = f"{c_abr}_addr_area_price.csv"
    create_colums(columns, f_name=f_name)
    single_addr_df = search_data(routs, limit_page=f_page, page=s_page, city=f"{c_abr}",
                                 concat_name=f"{r_name}", save_f_name=f_name)
    single_addr_df.to_csv()
    df = pd.read_csv(f_name, sep=",")
    # print("size df", len(df))
    # print("size unique addr", len(df.address.unique()))
    # print("size unique price", len(df.price.unique()))
    print(max(df.price), min(df.price))  # SPb 756144 40331, MSK 2837394 50000, 300000 12885


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

    columns = ["address", "area", "price"]

    main(routs=routs, columns=columns, c_abr="SPb", r_name="Санкт-Петербург", s_page=1, f_page=100)
    main(routs=routs, columns=columns, c_abr="MSK", r_name="Москва", s_page=1, f_page=100)
    main(routs=routs, columns=columns, c_abr="EKB", r_name="Екатеринбург", s_page=1, f_page=100)


