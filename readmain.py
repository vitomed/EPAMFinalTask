import pandas as pd


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


def add_data_df(df, list_lon_lat, filename, columns_name):
    add_df = pd.DataFrame(list_lon_lat, columns=columns_name)
    new_df = pd.concat([df, add_df], sort=False, axis=1)
    new_df.to_csv(filename, index=False)

import numpy as np

def drop_not_found_adr(df, del_adr):
    mask = df["address"].isin(del_adr) == False
    return df[mask]








df = pd.read_csv("test.csv", sep=",")
del_addres = ["Санкт-Петербург, Дивенская ул., 5"]
drop_not_found_adr(df, del_addres)