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
    del_adr = []
    count = 0
    for adr in list_addr:
        # time.sleep(0.5)
        try:
            latitude_longtitude = lon_lat_handler(Client, adr)
        except Exception as e:
            print(f"Exc for {adr} and count {count}")
            del_adr.append(adr)  # append for remove data
            print(e)
            break
        else:
            add_lon_lat = [latitude_longtitude[1], latitude_longtitude[0]]
            lon_lat.append(add_lon_lat)
        finally:
            count += 1
            print(count)
            # lon_lat.append(add_lon_lat)
    print(f" assertion len: {len(list_addr)} == {len(lon_lat)} + {len(del_adr)}")
    return lon_lat, del_adr


def drop_not_found_adr(df, del_adr):
    print("before drop", len(df["address"].isin(del_adr)))
    mask = df["address"].isin(del_adr) == False
    print(("after drop", len(df[mask])))
    return df[mask]


def save_data(data, columns, filename):
    """

    :param data:
    :param columns:
    :param filename:
    :return:
    """
    df = pd.DataFrame(data, columns=columns)
    df_common_fin = df.dropna(axis='index', how='any', subset=['longtitude'])
    print("info lon_lat df", df.info())
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
    new_df.to_csv(filename, index=False)


def main(c_abbr):
    """

    :param c_abbr:
    :return:
    """
    filename = f"{c_abbr}_addr_area_price.csv"
    list_addr, df = get_addr(f_name=filename)
    lon_lat, del_adr = create_list_lon_lat(list_addr)
    clear_df = drop_not_found_adr(df, del_adr)
    save_data(data=lon_lat, columns=["longtitude", "latitude"], filename=f"{c_abbr}_lon_lat.csv")
    add_data_to_df(clear_df, list_lon_lat=lon_lat, filename=f"{c_abbr}_addr_area_price_lon_lat.csv",
                   columns_name=["longtitude", "latitude"])


def insert_row(df, row_number, row_value, f_name):
    df.to_csv(f_name, index=True)
    df = pd.read_csv(f_name, sep=",")

    df1 = df[:row_number]
    df2 = df[row_number:]
    print(df1.loc[:])

    # df_result = pd.concat([df1, df2], sort=False)
    # print(df_result.shape())
    # print(df.index)
    # print(df.shape[0])
    # df.index = [*range(df.shape[0])]
    # df_result.to_csv(f_name, index=False)

if __name__ == "__main__":

    with open("apikey.txt", "r") as key_file:
        for line in key_file:
            key = line.strip()
    api_url = f"https://geocode-maps.yandex.ru/1.x?apikey={key}"
    setattr(Client, "API_URL", api_url)

    # city_abbr_exmpl = ["SPb", "MSK", "EKB"]
    city_abbr_exmpl = ["MSK"]
    # main("SPb")
    main("MSK")
    # main("EKB")
    for i in city_abbr_exmpl:

        df1 = pd.read_csv(f"{i}_lon_lat.csv", sep=",")
        print("len", len(df1))

        df2 = pd.read_csv(f"{i}_addr_area_price_lon_lat.csv", sep=",")
        print("len", len(df2))


    # insert_row(df, 0, [59.876549, 30.259202], f_name="SPb_lon_lat.csv")
    # df = pd.read_csv("SPb_lon_lat.csv", sep=",")
    # print(df.info())