'''
Created on 28 Mar 2018

@author: Emmet
'''

from math import pi, sin, cos, acos
import os.path
import csv

class Airport():
    ''' Stores Airport objects '''
    
    def __init__(self, airportCode, airportName, country, airportLat, airportLong):
        ''' Define what attributes we want the Airport instances to have '''
        self.airportCode = airportCode
        self.airportName = airportName
        self.country = country
        self.airportLat = airportLat
        self.airportLong = airportLong
           
    def getAirportCode(self):
        ''' Returns the code for the airport instance'''
        return self.airportCode
    
    def getAirportName(self):
        ''' Returns the name for the airport instance'''
        return self.airportName
    
    def getCountry(self):
        ''' Returns the country of the airport instance'''
        return self.country
               
    def getLatitude(self):
        ''' Returns the latitude for the airport instance '''
        return float(self.airportLat) 
    
    def getLongitude(self):
        ''' Returns the longitude for the airport instance '''
        return float(self.airportLong)


class AirportAtlas():
    ''' Holds info. on all of the airports '''
    
    def __init__(self):
        ''' AirportAtlas invokes the loadData method when called '''
        self.loadData("../airport.csv")

        
    def loadData(self, csvFile):
        ''' Reads the CSV file and creates instances of the class Airport. Key:Object pairs '''
        self.airports = {}
        with open(os.path.join("input", csvFile), "rt", encoding="utf8") as f:
            reader = csv.reader(f)
            for line in reader:
                self.airports[line[4]] = Airport(line[4], line[1], line[3], line[6], line[7])
                # airportCode = airportCode, airportName, countryName, latitude, longitude
        return self.airports

    
    def getAirport(self, code):
        ''' Takes a three letter code as input and returns the Airport object corresponding to the code '''
        Location = self.airports[code]
        return Location

     
    @staticmethod
    def greatCircleDistance(lat1, long1, lat2, long2):
        ''' Calculates the distance from one airport to another
        Return the answer as a float '''
          
        radius_earth = 6371
        theta1 = long1 * (2 * pi) / 360
        theta2 = long2 * (2 * pi) / 360
        phi1 = (90 - lat1) * (2 * pi) / 360
        phi2 = (90 - lat2) * (2 * pi) / 360
        distance = acos(sin(phi1) * sin(phi2) * cos(theta1 - theta2) + cos(phi1) * cos(phi2)) * radius_earth
        return distance

    
    def getDistanceBetweenAirports(self, code1, code2):
        ''' Takes in 2 airport codes and pulls out the latitude and longitude for each
        Passes these values to greatCircleDistance which uses them to return distance between the airports '''
        
        airport1 = self.getAirport(code1)
        airport2 = self.getAirport(code2)
        lat1 = airport1.getLatitude()
        long1 = airport1.getLongitude()
        lat2 = airport2.getLatitude()
        long2 = airport2.getLongitude()
        return self.greatCircleDistance(lat1, long1, lat2, long2)

    