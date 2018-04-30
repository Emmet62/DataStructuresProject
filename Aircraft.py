'''
Created on 19 Apr 2018

@author: Emmet
'''

import os.path
import csv

class Aircraft:
    ''' Loads in the aircraft data and extracts relevant information'''
    
    def __init__(self, aircraftCode, measureSystem, aircraftMaxRange):
        self.aircraftCode = aircraftCode
        self.measureSystem = measureSystem
        self.aircraftMaxRange = aircraftMaxRange
        
    def getAircraftCode(self):
        return self.aircraftCode
    
    def getAircraftRange(self):
        ''' Returns the range of the aircraft, accounts for imperial system'''
        if self.measureSystem == 'metric':
            totalRange = float(self.aircraftMaxRange)
        else:
            aircraftMaxRange = float(self.aircraftMaxRange)
            totalRange = aircraftMaxRange*1.609344
            
        return totalRange
    
class AircraftAtlas:
    
    def __init__(self):
        self.loadData()
    
    def loadData(self):
        ''' This code was adapted from the practical'''
        self.aircrafts = {}
        csvFile = "./aircraft.csv"
        with open(os.path.join(csvFile), "rt") as f:
            reader = csv.reader(f)
            for line in reader:
                self.aircrafts[line[0]] = Aircraft(line[0], line[2], line[4])
                # aircraftCode = aircraftCode, system, range
        return self.aircrafts

                    