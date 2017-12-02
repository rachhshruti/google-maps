import sys
import time
from math import *

'''
Description: The code is used to find a path between the start city and end city 
depending on the routing option and routing algorithm given as command-line arguments.
@author Shruti Rachh
'''

# Reads the start-city, end-city, routing-option and routing-algorithm passed as command-line arguments
startCity=sys.argv[1]
endCity=sys.argv[2]
routingOpt=sys.argv[3]
routingAlgo=sys.argv[4]
maxSpeed=0
maxDist=0

'''
Computes the path to the end city by exploring the neighbors of 
each of the cities starting with the start city and computing the cost 
(distance,time,scenic,segment) for each of them
Input:
	currCity- city whose neighbors are being explored
	dist- dictionary containing all the computations (distance,time,segment,scenic,path) 
		  of the visited cities
	visitedCities- stores the list of visited cities whose cost has been computed.
	mapData- dictionary containing the list of cities along with the information about their 
			 neighboring cities
	geoInfo- dictionary containing information about the latitudes and longitudes of the cities.
			 This parameter is only used for astar routing algorithm for computing the heuristic
			 function.
Output:
	dictionary containing the computed (distance,time,scenic,segment,path) for each of the visited
	cities and list of visited cities.
''' 
def getPath(currCity,dist,visitedCities,mapData):
	for neighbor in mapData[currCity]:
		city=neighbor.keys()[0]
		d=neighbor.values()[0]
		currData=compute(currCity,city,d,dist)
		if currData:
			if city == endCity:
				dist[city]=currData
				return dist
			elif city not in dist.keys():
				dist[city]=currData
				visitedCities.append(city)
			elif int(d[0])+dist[currCity][routingOpt]<dist[city][routingOpt]:
				dist[city]=currData
	return visitedCities,dist

'''
Runs BFS algorithm to find a path between start city and end city, if any. It may or may not
return an optimal solution depending on the given routing option
Input:
	mapData- dictionary containing the list of cities along with the information about their 
			 neighboring cities
Output:
	dictionary containing the computed (distance,time,scenic,segment,path) for the end-city
'''
def bfs(mapData):
	visitedCities=[startCity]
	dist={}
	dist[startCity]={"distance":0,"time":0,"segment":0,"scenic":0,"path":startCity}
	#maxFringe=0
	while len(visitedCities)>0:
		currCity=visitedCities.pop(0)
		getPath(currCity,dist,visitedCities,mapData)		
		if endCity in dist.keys():
			break
	if endCity not in dist.keys():
		return {}
	return dist[endCity]		

'''
Runs DFS algorithm to find a path between start city and end city, if any. It may or may not
return an optimal solution depending on the given routing option
Input:
	mapData- dictionary containing the list of cities along with the information about their 
			 neighboring cities
Output:
	dictionary containing the computed (distance,time,scenic,segment,path) for the end-city
'''
def dfs(mapData,k=sys.maxint):
	visitedCities=[startCity]
	dist={}
	dist[startCity]={"distance":0,"time":0,"segment":0,"scenic":0,"path":startCity}
	while len(visitedCities)>0:
		currCity=visitedCities.pop()
		if dist[currCity]["segment"]<k:
			getPath(currCity,dist,visitedCities,mapData)
		if endCity in dist.keys():
			break
	if endCity not in dist.keys():
		return {}
	else:
		return dist[endCity]

'''
Runs IDS algorithm to find a path between start city and end city, if any. It may or may not
return an optimal solution depending on the given routing option
Input:
	mapData- dictionary containing the list of cities along with the information about their 
			 neighboring cities
Output:
	dictionary containing the computed (distance,time,scenic,segment,path) for the end-city
'''
def ids(mapData):
	k=1
	path={}
	while 1:
		path=dfs(mapData,k)
		if path or k==10000:
			break
		k=k+1
	return path

'''
Builds a graph storing the distances of adjacent cities in a dictionary	
considering that all roads are bi-directional by reading from 
road-segments.txt file.
Output:
	The dictionary of the form:
		{"city":[{"neighbor1":[dist1,speed_limit,name_of_highway]},..]}
'''
def buildMap():
	mapData={}
	with open('road-segments.txt','rb') as file:
		for routes in file:
			record=routes.split(" ")
			if record[0] not in mapData.keys():
				mapData[record[0]]=[{record[1]:[record[2],record[3],record[4]]}]
			else:
				mapData[record[0]].append({record[1]:[record[2],record[3],record[4]]})

			if record[1] not in mapData.keys():
				mapData[record[1]]=[{record[0]:[record[2],record[3],record[4]]}]
			else:
				mapData[record[1]].append({record[0]:[record[2],record[3],record[4]]})
	return mapData

'''
Finds a route between start-city and end-city depending on the given routing
algorithm.
Input:
	mapData- dictionary containing the list of cities along with the information about their 
			 neighboring cities	
Output:
	dictionary containing the computed (distance,time,scenic,segment,path) for the end-city		
'''
def findRoute(mapData):
	if routingAlgo=="bfs":
		return bfs(mapData)
	elif routingAlgo=="dfs":
		return dfs(mapData)

# Runs the code
if routingOpt not in ["distance","time","scenic","segment"]:
	print "Invalid routing option!\nIt must be one of the [distance,time,scenic,segment]"
elif routingAlgo not in ["bfs","dfs","ids","astar"]:
	print "Invalid routing algorithm!\nIt must be one of the [bfs,dfs,ids,astar]"
else:
	mapData=buildMap()
	if startCity not in mapData.keys() or endCity not in mapData.keys():
		print "Please check whether the start city and/or end city is correct."
	elif startCity==endCity:
		print "You are already at your destination."
	else:
		path=findRoute(mapData)
