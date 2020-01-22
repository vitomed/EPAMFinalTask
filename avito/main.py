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


def saver(data, columns, f_name):

    df = pd.DataFrame(data, columns=columns)
    df = df.drop_duplicates("address")
    df.to_csv(f_name, mode="a", header=False, index=False)


def drop_addr_copy(df, column_name):
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
    df.drop_duplicates(column_name, inplace=True)
    return df


def search_data(routs, city, concat_name, page):
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
        return add_data


def main(routs, columns, c_abr, r_name, curr_page, f_page):
    """

    :param routs:
    :param columns:
    :param c_abr:
    :param r_name:
    :param curr_page:
    :param f_page:
    :return:
    """
    f_name = f"{c_abr}/{c_abr}_addr_area_price.csv"
    create_colums(columns, f_name=f_name)
    while curr_page < f_page:
        data_list = search_data(routs, page=curr_page, city=f"{c_abr}", concat_name=f"{r_name}")
        saver(data_list, columns, f_name)
        print("page", curr_page)
        curr_page += 1

    df = pd.read_csv(f_name, sep=",")
    updated_df = drop_addr_copy(df, column_name="address")
    updated_df.to_csv(f"{c_abr}/{c_abr}_updated_df.csv", index=False)

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

    city_routs = {"SPb": "sankt-peterburg", "MSK": "moskva", "EKB": "ekaterinburg"}

    columns = ["address", "area", "price"]

    main(routs=city_routs, columns=columns, c_abr="SPb", r_name="Санкт-Петербург", curr_page=1, f_page=100)
    # main(routs=routs, columns=columns, c_abr="MSK", r_name="Москва", s_page=1, f_page=100)
    # main(routs=routs, columns=columns, c_abr="EKB", r_name="Екатеринбург", s_page=1, f_page=100)


