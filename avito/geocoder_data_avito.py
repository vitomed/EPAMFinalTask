import pandas as pd
import time
from yandex_geocoder import Client
from yandex_geocoder.exceptions import YandexGeocoderAddressNotFound


def get_addr(f_name):
    """

    :param f_name:
    :return:
    """
    df = pd.read_csv(f_name, sep=",")
    addr = df["address"]
    return addr, df


def lon_lat_handler(client, addr):
    """

    :param client:
    :param addr:
    :return:
    """
    try:
        answer = client.coordinates(addr)
    except YandexGeocoderAddressNotFound:
        answer = (None, None)
    return answer


def create_list_lon_lat(list_addr, client):
    add_lon_lat = []
    count = 0
    for adr in list_addr:
        latitude_longtitude = lon_lat_handler(client, adr)
        lon_lat = [latitude_longtitude[1], latitude_longtitude[0]]
        add_lon_lat.append(lon_lat)
        count += 1
        print(count)
    return add_lon_lat


def save_lon_lat_as_df(data, columns, filename):
    """

    :param data:
    :param columns:
    :param filename:
    :return:
    """
    df = pd.DataFrame(data, columns=columns)
    print("info lon_lat df", df.info())
    df.to_csv(filename, index=False)


def add_new_columns(df, list_lon_lat, columns_name):
    add_df = pd.DataFrame(list_lon_lat, columns=columns_name)
    # print(add_df)
    new_df = pd.concat([df, add_df], sort=False, axis=1)
    # print(new_df)
    df_common_fin = new_df.dropna(axis='index', how='any', subset=['longtitude'])
    print(df_common_fin)
    return df_common_fin
    # print("add", df_common_fin.info())
    # df_common_fin.to_csv(filename, index=False)


def main(c_abbr):
    """

    :param c_abbr:
    :return:
    """
    filename = f"{c_abbr}/{c_abbr}_addr_area_price.csv"

    list_addr, df_main = get_addr(f_name=filename)

    lon_lat = create_list_lon_lat(list_addr, Client)

    save_lon_lat_as_df(data=lon_lat, columns=["longtitude", "latitude"], filename=f"{c_abbr}/{c_abbr}_lon_lat.csv")

    df_full = add_new_columns(df_main, list_lon_lat=lon_lat, columns_name=["longtitude", "latitude"])

    df_full.to_csv(f"{c_abbr}/{c_abbr}_addr_area_price_lon_lat.csv", index=False)


if __name__ == "__main__":

    with open("apikey.txt", "r") as key_file:
        for line in key_file:
            key = line.strip()
    api_url = f"https://geocode-maps.yandex.ru/1.x?apikey={key}"
    setattr(Client, "API_URL", api_url)

    # city_abbr_exmpl = ["SPb", "MSK", "EKB"]
    city_abbr_exmpl = ["EKB"]
    # main("SPb")
    # main("MSK")
    main("EKB")
    for i in city_abbr_exmpl:

        df1 = pd.read_csv(f"{i}/{i}_lon_lat.csv", sep=",")
        print("len", len(df1))

        df2 = pd.read_csv(f"{i}/{i}_addr_area_price_lon_lat.csv", sep=",")
        print("len", len(df2))


    # insert_row(df, 0, [59.876549, 30.259202], f_name="SPb_lon_lat.csv")
    # df = pd.read_csv("SPb_lon_lat.csv", sep=",")
    # print(df.info())