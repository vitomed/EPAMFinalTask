HeatMap цен на жилье по городам: Санкт-Петербург, Москва, Екатеринбург
======================================================================

## Подготовка к работе

### API key и cookie

В корне проекта необходимо создать два файла ``` cookie.txt и apikey.txt``` со следующей информацией:

В cookie.txt содержится ваш cookie

В apikey.txt ключ от Yandex API https://developer.tech.yandex.ru/services (JavaScript API и HTTP Геокодер)

### Installation requirements

Для работы с ```storage.py и geocoder_data_avito.py``` список зависимостей собран в requirements.txt

* Install Python dependency packages from requirements.txt

Для работы с ```.ipnd``` в jupyter notebooks, установите в рабочее окружение conda: 

[geopandas](http://geopandas.org/install.html)

[matplotlib](https://matplotlib.org/users/installing.html)

## Работа с проектом

### Данные для анализа отсутствуют

Файлы должны запускаться следующим образом:

* parser.py - парсер данных 
* geocoder_data_avito.py - API Client Yandex Geocoder

### Данные для анализа есть

Если нет необходимости парсить сайт, воспользуйтесь уже готовым набором данных:

```SPb_addr_area_price_lon_lat.csv, MSK_addr_area_price_lon_lat.csv, EKB_addr_area_price_lon_lat.csv ``` 

данные с адресами, площадью, стоимостью, а также географическими координатами домов для трех городов

### Визуализация результатов

Для визуализации вышепреречисленных файлов, используйте готовые jupyter notebooks: ```SPb_visualisation.ipynb, MSK_visualisation.ipynb, EKB_visualisation.ipynb```

В папках ```SPb, MSK, EKB ```, находится файл ```heatmap.html```, в котором изображена тепловая карта цен на недвижимость соответствующих городов

(NOTE! Маркеры кликабельны, чтобы увидеть информацию о конкретном доме - нажмите на маркер)



#### P.S.

В директории ```exportsh``` собраны данные в виде полигонов о каждом районе соответствующего города (файл .shp)

Ссылка на источники данных: 

[Геоданные](https://www.openstreetmap.org)
