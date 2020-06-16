import requests

moex_all_securities = 'https://www.moex.com/ru/listing/securities-list-csv.aspx?type=2'

def get_all_secs():
    c = requests.get(moex_all_securities)
    return c.content