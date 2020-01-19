import pandas as pd
a = ('30.289664', '50.958778')
b = ('40.1233', '60.958778')
c = ('50.289664', '70.958778')
d = ("30.153695", "59.795501")
e = ("30.473046", "59.919694")
list = [a, b, c, d, e]


def lon_lat(adr_list):
    lon_lat = []
    for elem in adr_list:
        add = [elem[0], elem[1]]
        lon_lat.append(add)
    print(lon_lat)
    return lon_lat


def save_data(data_lon_lat, columns, filename):
    df = pd.DataFrame(data_lon_lat, columns=columns)
    df.to_csv(filename, index=False)


lon_lat = lon_lat(list)
save_data(lon_lat, columns=["add3", "add4"], filename="new.csv")

df = pd.read_csv("old.csv", sep=",")


def add_data_df(df, list_lon_lat, filename, columns_name):
    add_df = pd.DataFrame(list_lon_lat, columns=columns_name)
    new_df = pd.concat([df, add_df], sort=False, axis=1)
    new_df.to_csv(filename, index=False)


add_data_df(df, lon_lat, filename="old.csv", columns_name=["add3", "add6"])

df = pd.read_csv("test_lon_lat.csv", sep=",")
print(df)