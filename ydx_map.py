from yandex_geocoder import Client
import pandas as pd
import time


def lon_lat_handler(client, addr):
    """

    :param client:
    :param addr:
    :return:
    """
    answer = client.coordinates(addr)
    return answer


def get_addr(f_name):
    """

    :param f_name:
    :return:
    """
    df = pd.read_csv(f_name, sep=",")
    addr = df["address"]
    return addr, df


def create_list_lon_lat(list_addr):
    """

    :param list_addr:
    :return: lon, lat
    """
    lon_lat = []
    for adr in list_addr:
        time.sleep(5)
        longlat_latlong = lon_lat_handler(Client, adr)
        add_lon_lat = [longlat_latlong[0], longlat_latlong[1]]
        lon_lat.append(add_lon_lat)

    return lon_lat


def save_data(data_lon_lat, columns, filename):
    """

    :param data:
    :param columns:
    :param filename:
    :return:
    """
    df = pd.DataFrame(data_lon_lat, columns=columns)
    print("save", df)
    df.to_csv(filename, index=False)


def add_data_to_df(df, list_lon_lat, filename, columns_name):
    """

    :param df:
    :param list_lon_lat:
    :param filename:
    :param columns_name:
    :return:
    """
    add_df = pd.DataFrame(list_lon_lat, columns=columns_name)
    new_df = pd.concat([df, add_df], sort=False, axis=1)
    print(new_df)
    new_df.to_csv(filename, index=False)


if __name__ == "__main__":

    with open("apikey.txt", "r") as key_file:
        for line in key_file:
            key = line.strip()
    api_url = f"https://geocode-maps.yandex.ru/1.x?apikey={key}"
    setattr(Client, "API_URL", api_url)

    filename = "SPb_address_price.csv"
    list_addr, df = get_addr(f_name=filename)
    lon_lat = create_list_lon_lat(list_addr)
    save_data(lon_lat, columns=["longitude", "latitude"], filename="Spb_lon_lat.scv")
    add_data_to_df(df, list_lon_lat=lon_lat, filename="SPb_addr_pr_lon_lat.csv", columns_name=["longitude", "latitude"])

