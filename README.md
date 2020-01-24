## HeatMap цен на жилье по городам: Санкт-Петербург, Москва, Екатеринбург


В корне проекта необходимо создать два файла ``` cookie.txt и apikey.txt``` со следующей информацией:

В cookie.txt содержится ваш cookie

В apikey.txt ключ от Yandex API https://developer.tech.yandex.ru/services (JavaScript API и HTTP Геокодер)

Файлы должны запускаться следующим образом:

```

1) parser.py - парсер данных 
2) geocoder_data_avito.py - API Client Yandex Geocoder

```

Если нет необходимости парсить сайт, воспользуйтесь уже готовым набором данных:

```
SPb_addr_area_price_lon_lat.csv, MSK_addr_area_price_lon_lat.csv, EKB_addr_area_price_lon_lat.csv - 

данные с адресами, площадью, стоимостью, а также географическими координатами домов в трех городах
```
Для визуализации вышепреречисленных файлов, используйте готовые jupyter notebooks: ```SPb_visualisation.ipynb, MSK_visualisation.ipynb, EKB_visualisation.ipynb```

В папках ```SPb, MSK, EKB ```, находится файл ```heatmap.html```, в котором изображена тепловая карта цен на недвижимость соответствующий городов (NOTE! Маркеры кликабельны, чтобы увидеть информацию о конкретном доме - нажмите на маркер)

P.S.

В директории ```exportsh``` собраны данные в виде полигонов о каждом районе соответствующего города (файл .shp)

Ссылка на источники данных: https://www.openstreetmap.org, https://www.avito.ru
