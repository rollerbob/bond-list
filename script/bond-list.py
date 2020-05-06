import os
import numpy as np
import pandas as pd
import requests
from dl import download_csv

# Файл с Мосбиржы со списком облигаций в XML
csv_file="res/bond_list.csv"
csv_file = os.path.join(os.path.dirname(__file__), os.pardir, csv_file)
csv_file = os.path.normpath(csv_file)

# Если файла нет, то скачаем его
if (os.path.isfile(csv_file) == False):
    csv = download_csv("01.05.2020")
    open(csv_file, "wt").write(csv)





base = pd.read_csv(csv_file, sep=';', encoding="cp1251" )
print (base[['Код бумаги']][:10])

