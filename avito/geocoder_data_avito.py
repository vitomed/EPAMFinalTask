import pandas as pd
from yandex_geocoder import Client
from yandex_geocoder.exceptions import YandexGeocoderAddressNotFound


def get_addr(file_name):
    """
    Get list of values from address column

    :param file_name: file that we open for reading
    :return: address list, data frame
    """
    d_frame = pd.read_csv(file_name, sep=",")
    addr = d_frame["address"]

    return addr, d_frame


def lon_lat_handler(client, addr):
    """
    Sends a get request in whose body the home address

    :param client: yandex geocoder Client
    :param addr: home address
    :return: latitude and longitude
    """
    try:
        answer = client.coordinates(addr)
    except YandexGeocoderAddressNotFound:
        answer = (None, None)

    return answer


def create_list_lon_lat(addresses, client):
    """
    Create list of longitude and latitude
    data

    :param addresses: addres list
    :param client: yandex geocoder Client
    :return: list of longitude and latitude
    """
    add_lon_lat = []
    count = 0
    for adr in addresses:
        latitude_longtitude = lon_lat_handler(client, adr)
        lon_lat = [latitude_longtitude[1], latitude_longtitude[0]]
        add_lon_lat.append(lon_lat)
        count += 1
        print(count)

    return add_lon_lat


def save_lon_lat_as_df(data, columns, file_name):
    """
    converts a list of latitudes and longitudes
    to a data frame and saves

    :param data: list of longitude and latitude
    :param columns: columns name
    :param file_name: file name
    """
    d_frame = pd.DataFrame(data, columns=columns)
    d_frame.to_csv(file_name, index=False)


def add_new_columns(d_frame, list_lon_lat, columns_name):
    """
    Connects two data frames

    :param d_frame: main data frame
    :param list_lon_lat: list of longitude and latitude
    :param columns_name:
    :return: frame in which all nan values will be removed
    """
    add_d_frame = pd.DataFrame(list_lon_lat, columns=columns_name)
    new_d_frame = pd.concat([d_frame, add_d_frame], sort=False, axis=1)
    d_frame_common_fin = new_d_frame.dropna(axis='index', how='any', subset=['longtitude'])

    return d_frame_common_fin


def main(c_abbr):
    """
    :param c_abbr: abbreviation of city
    """
    f_name = f"{c_abbr}/{c_abbr}_addr_area_price.csv"

    list_addr, main_d_frame = get_addr(file_name=f_name)

    lon_lat = create_list_lon_lat(addresses=list_addr, client=Client)

    save_lon_lat_as_df(data=lon_lat, columns=["longtitude", "latitude"],
                       file_name=f"{c_abbr}/{c_abbr}_lon_lat.csv")

    df_full = add_new_columns(d_frame=main_d_frame, list_lon_lat=lon_lat,
                              columns_name=["longtitude", "latitude"])

    df_full.to_csv(
        f"{c_abbr}/{c_abbr}_addr_area_price_lon_lat.csv",
        index=False)


if __name__ == "__main__":

    with open("apikey.txt", "r") as key_file:
        for line in key_file:
            key = line.strip()
    API_URL = f"https://geocode-maps.yandex.ru/1.x?apikey={key}"
    setattr(Client, "API_URL", API_URL)

    city_abbr_exmpl = ["SPb", "MSK", "EKB"]
    # main("SPb")
    # main("MSK")
    # main("EKB")
