import datapackage
import pandas as pd
import re
import numpy as np
from json import JSONEncoder, dumps
import math


class Country: 

    def __init__(self, name, currency, iso_code) -> None:
        self.name: str = name
        self.currency : str = currency
        self.iso_code : int = iso_code

class CountryEncoder(JSONEncoder): 
    def default(self, obj):
        return obj.__dict__   


data_url = 'https://datahub.io/core/currency-codes/datapackage.json'

# to load Data Package into storage
package = datapackage.Package(data_url)

# to store all the Country Objects
currencies = []

# to load only tabular data
resources = package.resources
for resource in resources:
    if resource.name == "codes-all_csv":
        indexes = []
        data = pd.read_csv(resource.descriptor['path'])

        for ind in data.index:
            # remove old currencies
            if type(data['WithdrawalDate'][ind]) == str or re.match("^ZZ", data['Entity'][ind]):
                indexes.append(ind)
        data.drop(indexes, inplace=True)
        # clear all the unwanted data
        data.drop(columns= ["NumericCode", "MinorUnit", "WithdrawalDate"], inplace=True)

        # clear all duplicated currencies
        data.drop_duplicates(subset=['Currency'], inplace=True)

        # clear all rows with NaN
        data.dropna(inplace=True)
        
        for ind in data.index: 
            currencies.append(Country(name = data['Entity'][ind], currency = data['Currency'][ind], iso_code= data['AlphabeticCode'][ind]))




json_string = dumps(currencies, cls=CountryEncoder)

# method to return based on query 
def get_search_results(name: str): 
    upper_name = name.upper()
    return list(filter(lambda x: upper_name in x.name.upper(), currencies))

    # method to return based on query 
def get_search_results_iso(iso: str): 
    upper_iso = iso.upper()
    return list(filter(lambda x: upper_iso in str(x.iso_code).upper(), currencies))

def total_search_results(query: str):
    first_list = get_search_results(name = query)
    second_list = get_search_results_iso(iso = query)
    first_list.extend(second_list)

    return dumps(first_list, cls = CountryEncoder)

# method to return all currencies regardless of country
def get_all_currencies():
    only_currency_list = list(map(lambda x: x.currency, currencies))
    return only_currency_list

# method to return specific currencies from synchrounous input 
def get_specific_currency(query: str): 
    upper_query = query.upper()
    return list(filter(lambda x: upper_query in x.upper(), get_all_currencies()))
