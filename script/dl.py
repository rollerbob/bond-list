#!/usr/bin/env python

import requests

URI = 'https://www.moex.com/ru/markets/stock/privilegeindividuals.aspx'

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,be;q=0.6",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "referer": URI,
}

def build_body(date, idx="0", change="", sort_by="", search=""):
    return {
        "__EVENTTARGET": "ctl00$PageContent$ctrlPrivilege$DownCSV",
        "__EVENTARGUMENT": "", 
        "__VIEWSTATE": "",
        "__EVENTVALIDATION": "/wEdABCvVXD1oYELeveMr0vHCmYPwaDSaUlVxBvR8swwp5V2bkCrzVsnCXEftxh8yu5XrI1wsOBwYZCjQDcRnEDHN/oVT8KU5+z2UsdG3ULNV4+dsCzk2G+Z3EJfyjp1rhAoEp84DZs/wSUfyvtEF83piNDc+/PivpJxB7iJpU3++tL1/oNvurASTA64JjG/UDcxYwsNirEaq0XvNcxGTLQrUOVNbQd6BXdjKzUgM6fhlk13Kighytrs7iWDvRido/VpD31dDWT41Pph6cnCUUhoab/9LSx3pPZlZJaAE2o5gPcXP0BWD1vP/wqkkPMp0nZeRXPqwbIccLdsbMTH014a4s0LoKLELXuIKxhOyEQBrhpqi1bfa/9dDsMxo9LUHBt8cL4=",
        "ctl00$PageContent$ctrlPrivilege$hidden_sort_column": str(sort_by),
        "ctl00$PageContent$ctrlPrivilege$hidden_current_page_index": str(idx),
        "ctl00$PageContent$ctrlPrivilege$hidden_current_page_index_change": str(change),
        "ctl00$PageContent$ctrlPrivilege$hidden_direction_desc": "",
        "ctl00$PageContent$ctrlPrivilege$beginDate": str(date),
        "ctl00$PageContent$ctrlPrivilege$txtSearch": str(search),
    }

def download_csv(to_date):
    response = requests.post(URI, headers=headers, data=build_body(to_date))
    return str(response.content, "cp1251")

