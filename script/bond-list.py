import os
import numpy as np
import pandas as pd

# Файл с Мосбиржы со списком облигаций в XML
csv_file="res/bond_list.csv"

cwd = os.path.dirname(__file__)
csv_file = os.path.join(cwd, os.pardir, csv_file)
csv_file = os.path.normpath(csv_file)

base = pd.read_csv(csv_file, sep=';', encoding="cp1251" )
print (base[['Код бумаги']][:10])
