'''
Created on 20 Apr 2018

@author: Emmet
'''

import os
import csv
import itertools

''' Import the classes'''
from Aircraft import AircraftAtlas
from Airport import AirportAtlas
from Currency import CurrenciesAtlas


''' Create the three dictionaries needed'''
aircraftDict = AircraftAtlas()
airportDict = AirportAtlas()
currencyDict = CurrenciesAtlas()

def main():
    ''' The main function for the analysis of the each route
    Reads the testroutes file and works through each route one at a time
    For each route, every possible pathway is evaluated. Always starts and ends at the first airport 
    Goes through each possible flight path and checks if each flight is feasible i.e. that the plane has the range to make the distance between stops
    If all flights in a flight path are feasible the total cost for all flights in this flight path is calculated
    The cheapest costing flight path is saved as the optimal flight path for the route
    A new file called bestroutes is created that has the optimal flight path and total cost for each route'''
    
    routeCatalog = {} # create an empty dictionary to store the optimal route and cost for each test route
    count = 0 # used for the key in the dictionary
    
    with open(os.path.join("./testroutes.csv"), "rt", encoding="utf8") as f: # open the testroutes file
        reader = csv.reader(f)
        for line in reader: # read each line one at a time
            
            airportStops = line # create a new variable to hold the info from the testroutes file
            airports = airportStops[:5] # create a variable to store the original route
            origin = airportStops[0] # origin is the first airport - will also be the last stop
            plane = airportStops[5] # denotes the model of plane used in the flight
            stops = set(airportStops[1:5]) # these are the 4 stops in between - compute every possible permutation of orders to fly in and evaluate each one (4! = 24)

            possible = 'Infeasible' # initialise route to be infeasible
            cheapestCost = 0 # initialise the cheapest cost for the route to 0
            optimalRoute = "" # start by saying no optimal route exists
            
            for combo in itertools.permutations(stops, 4): # computes the 4 stops in every possible order - 24 permutations in total
                feasibility = True # initialise feasibility to True
                
                comboCost = calculateCost(origin, combo[0], combo[1], combo[2], combo[3], plane) # call the calculateCost function to determine cost of this route                
                if comboCost == 0: # comboCost of 0 means the route wasn't feasible because of the plane not being able to cover the distance
                    feasibility = False
                
                if feasibility and cheapestCost == 0: # the first feasible route will satisfy this condition and become the optimal route
                    possible = 'Feasible'
                    cheapestCost = comboCost
                    optimalRoute = list([origin, combo[0], combo[1], combo[2], combo[3], origin])
                
                elif feasibility and comboCost < cheapestCost: # any subsequent feasible routes that are cheaper will become the new optimal route
                    cheapestCost = comboCost
                    optimalRoute = list([origin, combo[0], combo[1], combo[2], combo[3], origin])
                
            count += 1 # increment the key

            routeCatalog[count] = [plane, airports, optimalRoute, possible, cheapestCost] # add aircraft, airports, optimal route, feasiblilty and cost
            
            ''' Print the information for each route'''
            print("*********************************************************")
            print("Original Flight Plan:", airports)
            print("Aircraft Model:", plane)
            print("Optimal Route:", optimalRoute)
            print("Fuel Cost for Optimal Route:", cheapestCost)
            print("*********************************************************")
            print()
    
        
        with open('bestroutes.csv', 'w', newline='') as csvfile:
            fieldnames = ['Aircraft', 'Airports', 'Optimal Route', 'Feasibility', 'Fuel Cost'] # create the headers for the optimal routes file
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
            writer.writeheader()
            
            for i in range (1, count+1):
                ''' Iterate through each key/value pair in the routeCatalog dictionary
                Write the details for each route to a new row'''
                
                aircraftData = routeCatalog[i][0]
                airportsData = ", ".join(routeCatalog[i][1])
                routeData = ", ".join(routeCatalog[i][2])
                feasData = routeCatalog[i][3]
                costData = routeCatalog[i][4]
                
                writer.writerow({'Aircraft': aircraftData, 'Airports': airportsData, 'Optimal Route': routeData, 'Feasibility': feasData, 'Fuel Cost': costData})    
        

def calculateCost(begin, port1, port2, port3, port4, plane):
    ''' Takes in a route and calculates the total cost
    Breaks out of the loop if the plane can not travel the distance required
    Returns the total cost of the route - will be 0 if the distance is too great'''
    
    totalCost = 0
    planeRange = aircraftDict.aircrafts[plane].getAircraftRange() # uses a method from aircrafts class to determine plane's max distance
    array = list([begin, port1, port2, port3, port4, begin]) # create and array holding the flight path - start and end at first station
    for i in range (0, len(array)-1):
        distance = float(airportDict.getDistanceBetweenAirports(array[i], array[i+1])) # use a method from airportAtlas to get distance between airports
        if distance > planeRange: # check if the distance between the two airports exceeds the plane's range
            totalCost = 0
            return totalCost
        else:
            exchange = float(getCurrencyRate(array[i])) # call getCurrencyRate function to get the exchange rate for the country the airport is in
            cost = distance*exchange # compute the cost by multiplying distance by FX rate
            totalCost += cost # calculate the total cost of all routes in the flight path
    
    return totalCost # return the total cost of the flight path back to the main function
     
        
def getCurrencyRate(code):
    ''' Takes in an airport code as the argument
    Uses this to retrieve the country name from the airport dictionary
    Country name can be used to get currency to rate from the currencies dictionary'''
    name = airportDict.airports[code].getCountry() # use a method from airports class to get the country name
    currencyTo = currencyDict.currencies[name].getCurrencyTo() # use country name to look up currencyTo rate from merged currencies file
    return currencyTo # return the currencyTo rate to the calculateCost function


if __name__ == '__main__':
    main()
