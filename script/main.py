import os
import numpy as np
import pandas as pd
import json
from dl import download_csv
from dl import get_data

def main():
    
    # Сначала создаю DataFrame c нужными колонками
    df = pd.DataFrame(columns=[
        'Код облигации',
        'Наименование',
        'Отрасль',
        'Дата размещения',
        'Дата погашения',
        'Уровень листинга',
        'Номинал',
        'Стоимость',
        'Ном. доходность',
        'Доходность',
        'Кол-во платежей в год',
        'Фиксиированный купон',
        'Амортизация',
        'Дюрация'
    ])
    
    # Теперь беру список обращающихся рублевых облигаций российских организаций,
    # процентные (купонные) доходы по которым не облагаются налогом на доходы 
    # физических лиц в пределах установленных лимитов.
    # Список берётся с
    # https://www.moex.com/ru/markets/stock/privilegeindividuals.aspx

    # На какую дату нужно проверить список
    to_date = "06.05.2020"

    # Расположение файла
    csv_file="res/bond_list.csv"
    csv_file = os.path.join(os.path.dirname(__file__), os.pardir, csv_file)
    csv_file = os.path.normpath(csv_file)

    # Проверяю есть ли сохранённый файл на диске в res/bond_list.csv
    # Если файла нет, то скачаем его
    if (os.path.isfile(csv_file) == False):
        print ("Скачиваю список облигаций с сервера MOEX.")
        csv = download_csv(to_date)
        print ("Сохраняю список облигаций на диск.")
        open(csv_file, "wt").write(csv)
    else:
        print ("Открываю список облигаций с диска.")
        csv = open(csv_file, "r")

    # создаю DataFrame с этими данными
    bond_list = pd.read_csv(csv, sep=';', encoding="cp1251")

    # перетаскиваю нужные мне данные в главный DataFrame
    df['Код облигации'] = bond_list['ISIN']
    df['Наименование'] = bond_list['Наименование']
    df['Дата размещения'] = bond_list['Дата начала размещения']


    # DataFrame bond_list больше не нужен
    del bond_list

    # Создаю конфиг для аутентификации на сайте мосбиржи
    # my_config = Config("gd.triebkraft@gmail.com", "32Go7bi")
    
    
    

    # Формирую Series с кодами облигаций
    isins = df['Код облигации']

    # Заполняю остатки DataFrame используя запросы к бирже по коду облигации
    i = 0
    
    for isin in isins:
        r = get_data(isin).json()
        data = r.get('description').get('data')
        for line in data:
            if line[0] == "LISTLEVEL":
                df.loc[i, 'Уровень листинга'] = line[2]
        print (i)
        i += 1

    print (df.head())
    
    # for isin in isins:
    #     df.loc[i, 'Отрасль'] = isin
    #     i += 1
        


if __name__ == '__main__':
    main()