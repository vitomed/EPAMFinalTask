import pandas as pd
a = ('30.289664', '50.958778')
b = ('40.1233', '60.958778')
c = ('50.289664', '70.958778')
d = ("30.153695", "59.795501")
e = ("30.473046", "59.919694")
list = [a, b, c, d, e]


# cleaning(clean_df)


def get_addr(f_name):
    df = pd.read_csv(f_name, sep=",")
    addr = df["address"]
    return addr, df


def lon_lat_handler(client, addr):

    try:
        answer = client.coordinates(addr)
    except YandexGeocoderAddressNotFound:
        answer = (None, None)
    return answer


def create_list_lon_lat(list_addr, client):
    add_lon_lat = []
    count = 0
    for adr in list_addr[:5]:
        latitude_longtitude = lon_lat_handler(client, adr)
        lon_lat = [latitude_longtitude[1], latitude_longtitude[0]]
        add_lon_lat.append(lon_lat)
        count += 1
        print(count)
    return add_lon_lat


def save_lon_lat_df(data, columns, filename):
    df = pd.DataFrame(data, columns=columns)
    print("info lon_lat df", df.info())
    df.to_csv(filename, index=False)


def add_data_to_df(df, list_lon_lat, filename, columns_name):
    add_df = pd.DataFrame(list_lon_lat, columns=columns_name)
    # print(add_df)
    new_df = pd.concat([df, add_df], sort=False, axis=1)
    # print(new_df)
    df_common_fin = new_df.dropna(axis='index', how='any', subset=['longtitude'])
    # print(df_common_fin)
    print("add", df_common_fin.info())
    # df_common_fin.to_csv(filename, index=False)


with open("apikey.txt", "r") as key_file:
    for line in key_file:
        key = line.strip()

# api_url = f"https://geocode-maps.yandex.ru/1.x?apikey={key}"
# setattr(Client, "API_URL", api_url)

# addr, df = get_addr("avito/MSK_addr_area_price.csv")
# l1 = create_list_lon_lat(addr, Client)
# print(l1)

# save_lon_lat_df(l1, ["longtitude", "latitude"], filename="test_lon_lat.csv")

# add_data_to_df(df, l1, "test_addr_area_pr_lon_lat.csv", ["longtitude", "latitude"])

"Москва, Рублёвское ш., 70к5"


df_lon_lat = pd.read_csv("test_lon_lat.csv", sep=",")
df = pd.read_csv("avito/MSK_addr_area_price.csv", sep=",")
add_data_to_df(df, list(zip(df_lon_lat.longtitude.values, df_lon_lat.latitude.values)),
               "test_addr_area_pr_lon_lat.csv", ["longtitude", "latitude"])

