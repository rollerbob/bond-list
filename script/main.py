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
        'Нак. куп. доход',
        'Период купона',
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
    to_date = "08.05.2020"

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
    bond_list = pd.read_csv(csv_file, sep=';', encoding="cp1251")

    # перетаскиваю нужные мне данные в главный DataFrame
    df['Код облигации'] = bond_list['ISIN']
    df['Дата размещения'] = bond_list['Дата начала размещения']

    # DataFrame bond_list больше не нужен
    del bond_list

    # Формирую Series с кодами облигаций
    isins = df['Код облигации']

    # Заполняю остатки DataFrame используя запросы к бирже по коду облигации
    i = 0
    bar = ChargingBar('Сбор данных с сайта MOEX', max=len(isins), suffix='%(percent).1f%% | Осталось -  %(eta_td)s ')
    
    for isin in isins:
        r = get_data_ext(isin).json()
        
        columns = r.get('securities').get('columns')
        data = r.get('securities').get('data')
        
        if columns and data:
            data = data[0]
            df.loc[i, 'Наименование'] = data [columns.index('SECNAME')]
            df.loc[i, 'Дата погашения'] = data [columns.index('MATDATE')]
            df.loc[i, 'Уровень листинга'] = data[columns.index('LISTLEVEL')]
            df.loc[i, 'Номинал'] = data[columns.index('FACEVALUE')]
            df.loc[i, 'Стоимость'] = data[columns.index('PREVWAPRICE')]
            df.loc[i, 'Ном. доходность'] = data[columns.index('COUPONPERCENT')]
            df.loc[i, 'Нак. куп. доход'] = data[columns.index('ACCRUEDINT')]
            df.loc[i, 'Период купона'] = data[columns.index('COUPONPERIOD')]
            # df.loc[i, 'Фиксированный купон'] = data[columns.index('')]
            # df.loc[i, 'Амортизация'] = data[columns.index('')]

        marketdata = r.get('marketdata').get('columns')
        data = r.get('marketdata').get('data')

        if columns and data:
            data = data[0]
            df.loc[i, 'Доходность'] = data[marketdata.index('YIELD')]
            df.loc[i, 'Дюрация'] = data[marketdata.index('DURATION')]

        bar.next()
        i += 1

    bar.finish()
    
    # Сохраняю полученные данные в эксель
    df.to_excel(xlsx_file)
    print (df.head())


if __name__ == '__main__':
    main()
