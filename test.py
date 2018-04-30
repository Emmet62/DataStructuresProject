'''
Created on 22 Apr 2018

@author: Emmet
'''

from Aircraft import *
from Airport import *
from Currency import *
from main import getCurrencyRate, calculateCost

''' Create the three test dictionaries needed'''
testAircraftDict = AircraftAtlas()
testAirportDict = AirportAtlas()
testCurrencyDict = CurrenciesAtlas()

def test_aircraftDict():
    ''' Test that the aircraft dictionary has been created'''
    assert testAircraftDict != None

def test_airportDict():
    ''' Test that the airport dictionary has been created'''
    assert testAirportDict != None

def test_currencyDict():
    ''' Test that the currency dictionary has been created'''
    assert testCurrencyDict != None

def test_getAircraftRange():
    ''' Test that the aircraft range method works'''
    testPlaneRange = testAircraftDict.aircrafts['A330'].getAircraftRange()
    assert testPlaneRange == 13430
    
def test_getDistanceBetweenAirports():
    ''' Test that the correct great circle distance is returned'''
    testDistance = testAirportDict.getDistanceBetweenAirports('LHR', 'JFK')
    assert round(testDistance) == 5539

def test_getCurrencyRate():
    ''' Test that the correct FX rate is used to convert the cost'''
    testCurrencyRate = getCurrencyRate('GIG')
    assert testCurrencyRate == '0.2932'
    
def test_calculateCost():
    ''' Test that the correct cost for a flight path is calculated'''
    testCost = calculateCost('LOV', 'VKO', 'VCS', 'BBO', 'BHI', '747')
    assert round(testCost, 4) == 1658.6244
    
def test_codeToName():
    ''' Test that entering an airport code returns name of the country that the airport is in'''
    testName = testAirportDict.airports['DUB'].getCountry()
    assert testName == 'Ireland'

