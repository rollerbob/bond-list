import os
import numpy as np
import pandas as pd
from progress.bar import ChargingBar
from dl import download_csv
from dl import get_data
from dl import get_data_ext

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
        'Фиксированный купон',
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

    # Расположение файла со списком облигаций
    csv_file = "res/bond_list.csv"
    csv_file = os.path.join(os.path.dirname(__file__), os.pardir, csv_file)
    csv_file = os.path.normpath(csv_file)

    # Расположение файла с итоговым экселем
    xlsx_file = "res/big_table.xlsx"
    xlsx_file = os.path.join(os.path.dirname(__file__), os.pardir, xlsx_file)
    xlsx_file = os.path.normpath(xlsx_file)

    # Проверяю есть ли сохранённый файл на диске в res/bond_list.csv
    # Если файла нет, то скачаем его
    if os.path.isfile(csv_file) == False:
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

    # Формирую Series с кодами облигаций
    isins = df['Код облигации']

    # Заполняю остатки DataFrame используя запросы к бирже по коду облигации
    i = 0
    bar = ChargingBar('Сбор данных с сайта MOEX', max=len(isins), suffix='%(percent).1f%% | Осталось -  %(eta_td)s ')
    
    for isin in isins:
        r = get_data(isin).json()
        data = r.get('description').get('data')
        for line in data:
            if line[0] == "LISTLEVEL":
                df.loc[i, 'Уровень листинга'] = line[2]

            if line[0] == "MATDATE":
                df.loc[i, 'Дата погашения'] = line [2]

            if line[0] == "FACEVALUE":
                df.loc[i, 'Номинал'] = line[2]

            if line[0] == "COUPONFREQUENCY":
                df.loc[i, 'Кол-во платежей в год'] = line[2]

            if line[0] == "COUPONPERCENT":
                df.loc[i, 'Ном. доходность'] = line[2]

        r = get_data_ext(isin).json()
        data = r.get('marketdata').get('data')
        if data:
            line = data[0]
            df.loc[i, 'Стоимость'] = line[47]
            df.loc[i, 'Доходность'] = line[16]
            df.loc[i, 'Дюрация'] = line[36]

        bar.next()
        i += 1

    bar.finish()
    
    # Сохраняю полученные данные в эксель
    df.to_excel(xlsx_file)


if __name__ == '__main__':
    main()