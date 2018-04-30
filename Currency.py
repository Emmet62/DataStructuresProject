'''
Created on 28 Mar 2018

@author: Emmet
'''
import os
import csv
import pandas as pd

class Currencies():
    '''Create a class that can store information relating to currencies'''

    def __init__(self, currencyCode, currencyName, currencyTo, currencyFrom, countryName):
        self.currencyCode = currencyCode
        self.currencyName = currencyName
        self.currencyTo = currencyTo
        self.currencyFrom = currencyFrom
        self.countyName = countryName
        
    def getCurrencyCode(self):
        ''' Returns the currency code'''
        return self.currencyCode
        
    def getCurrencyName(self):
        ''' Returns the currency name'''
        return self.currencyName 
    
    def getCurrencyTo(self):
        ''' Returns the currency to rate '''
        return self.currencyTo
    
    def getCurrencyFrom(self):
        ''' Returns the currency from rate '''
        return self.currencyFrom
        
    def getCountryName(self):
        ''' Returns the country name'''
        return self.countyName

class CurrenciesAtlas():
    
    currencies = {}
    
    def __init__(self):
        ''' Call the merge files method'''
        self.mergeFiles()
        
    def mergeFiles(self):    
        ''' Reads in the 2 currency files and merges them on the currency_alphabetic_code'''
        rates =pd.read_csv("./currencyrates.csv")
        currency = pd.read_csv("./countrycurrency.csv")
        rates.columns = ['currencyName', 'currency_alphabetic_code', 'currencyTo', 'currencyFrom']
        merged = pd.merge(currency, rates, on='currency_alphabetic_code')
        merged.dropna()
        merged.to_csv("./merged.csv")
        self.loadData("./merged.csv")
        
    def loadData(self, file):
        ''' Create a dictionary using the new merged file'''
        with open(os.path.join(file), "rt", encoding="utf8") as f:
            reader = csv.reader(f)
            for line in reader:
                self.currencies[line[1]] = Currencies(line[1], line[15], line[22], line[23], line[21])
                # countryName = countryName, currencyCode, currencyTo, currencyFrom, currencyName
        return self.currencies

