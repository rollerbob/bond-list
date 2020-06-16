import os
import numpy as np
import pandas as pd
import requests
from progress.bar import ChargingBar
import download

# Расположение файла со списком ценных бумаг, допущенных к торгам.
csv_file = "res/all_securities.csv"
csv_file = os.path.join(os.path.dirname(__file__), os.pardir, csv_file)
csv_file = os.path.normpath(csv_file)

bond_csv = "res/temp.csv"
bond_csv = os.path.join(os.path.dirname(__file__), os.pardir, bond_csv)
bond_csv = os.path.normpath(bond_csv)

# Проверяю есть ли сохранённый файл на диске в res/all_securities.csv
# Если файла нет, то скачаем его
if os.path.isfile(csv_file) == False:
    print ("Скачиваю список ценных бумаг с сервера MOEX.")
    all_secs = download.get_all_secs()
    print ("Сохраняю список на диск.")
    open(csv_file, "wb").write(all_secs)
    
else:
    print ("Открываю список облигаций с диска.")

# создаю DataFrame с этими данными
all_secs_df = pd.read_csv(csv_file, sep=';', verbose=True, encoding="CP1251")

# Теперь нужно сделать два списка. Список акций и список облигаций
bonds = all_secs_df[all_secs_df['SUPERTYPE'] == 'Облигации']
bonds = bonds[['ISIN', 'INSTRUMENT_TYPE']].dropna().to_csv(bond_csv)




