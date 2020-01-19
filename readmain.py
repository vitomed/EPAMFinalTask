import pandas as pd


filename = "SPb_address_price.csv"

df2 = pd.read_csv(filename, sep=",")
addr = df2["address"][10]

def geoYandex():
    pass



