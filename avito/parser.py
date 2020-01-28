import re
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs


def create_colums(columns, file_name):
    """
    An empty table is created with the column name,
    which are transferred to variable columns and
    stored in a file named file_name

    :param columns: columns name
    :param filename: file name
    """
    d_frame = pd.DataFrame(columns=columns)
    d_frame.to_csv(file_name, index=False)


def search_ads(resp):
    """
    Search advertisement for apartments for sale

    :param resp: pice of HTML page
    :return: list advertisement
    """
    soup = bs(resp.content, "html.parser")
    return soup.findAll("div", {"class": "item__line"})


def parsing_ads(advertisements, city):
    """
    In each ad it is looking for an address,
    cost of housing, area of an apartment

    :param advertisements: list of found ads on the page
    :param pattern: price search template
    :param city: joins in order to determine the coordinates
    :return: list with information about each home
    """
    apart_info = []
    pattern = "\d+"

    for ads in advertisements:
        address = ads.findAll("span", {"class": "item-address__string"})

        if not address:
            continue

        price = ads.findAll("span", {"class": "price"})
        area = ads.findAll("a", {"class": "snippet-link"})
        cost_of_housing = int("".join(re.findall(pattern, price[0].text)))
        try:
            area_m2 = float(area[0].text.split(",")[1][:-2].strip())
        except Exception as exp:
            print(exp)
        else:
            cost_m2 = round(cost_of_housing / area_m2)
            house_chars = [f"{city}, {address[0].text.strip()}", area_m2, cost_m2]
            apart_info.append(house_chars)
    return apart_info


def writer_apart_info(data_aparts, columns, file_name):
    """
    Writes new data on apartments to the data apartsbase

    :param data_aparts: list of apatments info
    :param columns: columns on data frame
    :param file_name: name file for saving data frame
    """
    d_frame = pd.DataFrame(data_aparts, columns=columns)
    d_frame.to_csv(file_name, mode="a", header=False, index=False)


def drop_addr_copy(d_frame, column_name):
    """
    If you need to save only unique addresses,
    then use this function. She will remove all repetitions.
    occurring in the address column and will leave unique
    values

    :param d_frame: investigated data frame
    :param column_name: column name to check
    :return: updated data frame
    """
    d_frame.drop_duplicates(column_name, inplace=True)
    return d_frame


def search_data(routs, city_key, concat_name, page):
    """
    Finding home sales data on every page

    :param routs: dictionary with urls
    :param city_key: key to select the desired URL
    :param concat_name: city name
    :param page: investigated page
    :return: set of information parameters about apartments
    """
    url = f"https://www.avito.ru/{routs[city_key]}/kvartiry/prodam/monolitnyy_dom?s=104&p={page}"
    session = requests.Session()
    resp = session.get(url, headers=HEADERS)
    try:
        assert resp.status_code == 200, f"NOTE! {resp.status_code}"
    except Exception as exp:
        print(exp)
    else:
        ads = search_ads(resp=resp)
        list_appart_info = parsing_ads(advertisements=ads, city=concat_name)
        return list_appart_info


def main(routs, columns, c_abr, r_name, curr_page, f_page):
    """
    :param routs: dictionary with urls
    :param columns: columns on data frame
    :param c_abr: city abbreviation
    :param r_name: russian name of the city
    :param curr_page: start page for searching
    :param f_page: finish page
    """
    f_name = f"{c_abr}/{c_abr}_addr_area_price.csv"
    create_colums(columns=columns, file_name=f_name)

    while curr_page < f_page:
        print("page", curr_page)
        data_list = search_data(routs, page=curr_page, city_key=f"{c_abr}", concat_name=f"{r_name}")
        writer_apart_info(data_aparts=data_list, columns=columns, file_name=f_name)
        curr_page += 1

    # created_df = pd.read_csv(f_name, sep=",")
    # updated_df = drop_addr_copy(created_df, column_name="address")
    # updated_df.to_csv(f"{c_abr}/{c_abr}_updated_df.csv", index=False)


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

    CITY_ROUTS = {"SPb": "sankt-peterburg", "MSK": "moskva", "EKB": "ekaterinburg"}
    FRAME_COLUMNS = ["address", "area", "price"]


    main(routs=CITY_ROUTS, columns=FRAME_COLUMNS, c_abr="SPb",
         r_name="Санкт-Петербург", curr_page=1, f_page=100)
    # main(routs=CITY_ROUTS, columns=FRAME_COLUMNS, c_abr="MSK",
    #      r_name="Москва", curr_page=1, f_page=100)
    # main(routs=CITY_ROUTS, columns=FRAME_COLUMNS, c_abr="EKB",
    #      r_name="Екатеринбург", curr_page=1, f_page=100)
