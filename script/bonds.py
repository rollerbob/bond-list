import os
import numpy as np
import pandas as pd
import requests
from progress.bar import ChargingBar
import download

print ()

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

print ()

# создаю DataFrame с этими данными
all_secs_df = pd.read_csv(csv_file, sep=';', verbose=False, encoding="CP1251")
# На какое число составлен список 
to_date = all_secs_df.loc[0,'DATESTAMP']
to_date = to_date[:10]

# Теперь нужно сделать два списка. Список акций и список облигаций

# Начинаю обрабатывать список облигаций.
# Для начала вычленяю из общего списка все облигации
# мне достаточно датафрейма с ISIN и типом облигации
bonds = all_secs_df[all_secs_df['SUPERTYPE'] == 'Облигации']
bonds = bonds[['ISIN', 'INSTRUMENT_TYPE']].dropna()
print ("Количество облигаций торгуемых на дату", to_date, ":", bonds.shape[0])

# Теперь разберусь с полученными данными
# Сколько всего облигаций каждого типа в полученном датафрейме
unique_bonds_types = bonds.INSTRUMENT_TYPE.value_counts()

# Cколько всего таких типов
unique_bonds_type_amount = len(unique_bonds_types)
print ("Количество типов облигаций:", unique_bonds_type_amount)
print ("Типы облигаций:")
print (unique_bonds_types)

# Теперь по каждому типу могу собрать данные и сохранить
for bond_type in unique_bonds_types.index:
    # создаю датафрейм для текущего типа облигаций
    df = pd.DataFrame(columns=[
        'ISIN облигации',
        'Наименование',
        'Отрасль',
        'Дата размещения',
        'Дата погашения',
        'Уровень листинга',
        'Номинал',
        'Стоимость',
        'Ном. доходность',
        'Доходность',
        'Нак. куп. доход',
        'Период купона',
        'Фиксированный купон',
        'Амортизация',
        'Дюрация'
    ])
    # Формирую серию ISIN текущего типа облигаций
    isins = bonds[bonds['INSTRUMENT_TYPE'] == bond_type]
    isins = isins['ISIN']
    
    for isin in isins:


# bonds.to_csv(bond_csv)




