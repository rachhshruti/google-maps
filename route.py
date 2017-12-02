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
Computes all the routing options (distance,time,segment,scenic) and path for a city 
based on the computations of its parent city and returns a dictionary.
Input:
	currCity- name of the city that is currently being explored.
	adjCity- one of the neighboring city of currCity
	d- list of [dist,speed_limit,highway] of adjCity
	dist- dictionary containing all the computations (distance,time,segment,scenic,path) 
		  of the visited cities
Output:
	a dictionary containing the computation for adjCity 
'''
def compute(currCity,adjCity,d,dist):
	currPath=dist[currCity]["path"]+"\n"+adjCity
	currTime=0
	distOnHighway=dist[currCity]["scenic"]
	if d[0]!="" and d[1]!="" and d[0]!="0" and d[1]!="0":
		currTime=round((float(d[0])/float(d[1]))*60,2)
		if int(d[1])>=55:
			distOnHighway+=int(d[0])
	else:
		return {}
	return {"distance":int(d[0])+dist[currCity]["distance"],"time":currTime+dist[currCity]["time"],"segment":dist[currCity]["segment"]+1,"scenic":distOnHighway,"path":currPath}	

'''
Reads the information about the latitudes and longitudes of the cities
from city-gps.txt file and stores it in the dictionary.
Output:
	a dictionary with key as the city and value as the list of [latitude,longitude] 
'''
def getGeoInfo():
	geoInfo={}
	with open('city-gps.txt','rb') as file:
		for cityInfo in file:
			record=cityInfo.split(" ")
			geoInfo[record[0]]=[record[1],record[2]]
	return geoInfo

'''
Reads the information about the latitudes and longitudes of the cities
from city-gps.txt file and stores it in the dictionary.
Output:
	a dictionary with key as the city and value as the list of [latitude,longitude] 
'''
def getBestNode(visitedCities,endCity,dist,routingOpt):
	minCost=sys.maxint
	bestCity=""
	for city in visitedCities:
		if minCost>dist[city]["heuristic"]:
			minCost=dist[city]["heuristic"]
			bestCity=city
	return bestCity

'''
This function is called when there are no geographical co-ordinates for a city.
It finds whether the neighbors of the city has geographical co-ordinates, if yes
it returns that neighbor.
Input:
	city- name of the city whose latitude and longitude is not known 
	geoInfo- dictionary containing information about the latitudes and longitudes of the cities 
	mapData- dictionary containing the list of cities along with the information about their 
			 neighboring cities
Output:
	a dictionary with key as the neigbor city and value as the list of [distance,speed_limit,highway]
	retrieved from mapData dictionary whose geographical co-ordinates are
	present in the geoInfo dictionary,if no such neighbor found, it returns empty dict 
'''
def findNeighbor(city,geoInfo,mapData):
	for neighbor in mapData[city]:
		if neighbor.keys()[0] in geoInfo.keys():
			return neighbor
	return {}

'''
Calculates the heuristic function depending on whether the geographical co-ordinates are present
or not. If not present, it checks if its parent or any of the neighboring cities contains the
geographical co-ordinates. If none present, then it assigns max int value to heuristic function.
Input:
	currCity- parent city of the city whose heuristic function is currently being computed
	adjCity- city whose heuristic is to be computed
	geoInfo- dictionary containing information about the latitudes and longitudes of the cities 
	mapData- dictionary containing the list of cities along with the information about their 
			 neighboring cities
	dist- dictionary containing all the computations (distance,time,segment,scenic,path) 
		  of the visited cities
Output:
	heuristic function value
''' 
def getHeuristic(currCity,adjCity,geoInfo,mapData,dist):
	if adjCity in geoInfo.keys():
		h=computeHeuristic(geoInfo[adjCity],geoInfo[endCity])
	elif currCity in geoInfo.keys():
		h=computeHeuristic(geoInfo[currCity],geoInfo[endCity])-(dist[adjCity][routingOpt]-dist[currCity][routingOpt])
	else: 
		n=findNeighbor(adjCity,geoInfo,mapData)
		if n:
			nData=compute(adjCity,n.keys()[0],n.values()[0],dist)
			h=computeHeuristic(geoInfo[n.keys()[0]],geoInfo[endCity])+(nData[routingOpt]-dist[adjCity][routingOpt])		
		else:
			h=sys.maxint
	if routingOpt=="time":
		h=h/float(maxSpeed)
	elif routingOpt=="segment":
		h=int(h/float(maxDist))
	elif routingOpt=="scenic":
		h=h/2
	return h

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
def getPath(currCity,dist,visitedCities,mapData,geoInfo={}):
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
			if geoInfo and city in dist.keys():
				h=getHeuristic(currCity,city,geoInfo,mapData,dist)
				dist[city]["heuristic"]=h+dist[city][routingOpt]
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
Runs A* algorithm to find a path between start city and end city, if any based on some heuristic
function. It may or may not return an optimal solution depending on the given routing option.
Input:
	mapData- dictionary containing the list of cities along with the information about their 
			 neighboring cities
Output:
	dictionary containing the computed (distance,time,scenic,segment,path) for the end-city
'''
def astar(mapData):
	visitedCities=[startCity]
	dist={}
	dist[startCity]={"distance":0,"time":0,"segment":0,"scenic":0,"path":startCity,"heuristic":0}
	geoInfo=getGeoInfo()
	while len(visitedCities)>0:
		currCity=getBestNode(visitedCities,endCity,dist,routingOpt)
		visitedCities.remove(currCity)
		getPath(currCity,dist,visitedCities,mapData,geoInfo)
		if endCity in dist.keys():
			break
	if endCity not in dist.keys():
		return {}
	return dist[endCity]

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

			# max speed and max distance is computed to calculate time and segment heuristic in case of astar
			global maxSpeed,maxDist
			if maxSpeed<record[3]:
				maxSpeed=record[3]
			if maxDist<record[2]:
				maxDist=record[2]
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
	elif routingAlgo=="ids":
		return ids(mapData)
	elif routingAlgo=="astar":
		return astar(mapData)

'''
Prints the path containing the list of intermediate cities along with their distances and time
assuming that the speed limits are being followed
Input:
	route- list of intermediate cities
	mapData- dictionary containing the list of cities along with the information about their 
			 neighboring cities			
'''
def printPath(route,mapData):
	totalTime=0
	cities=""
	for i in range(0,len(route)-1):
		cities=cities+route[i]+" "
		for j in mapData[route[i]]:
			if route[i+1] == j.keys()[0]:
				val=j.values()[0]
				time=round((float(val[0])/float(val[1]))*60,2)
				print "Go to ",route[i+1]," on ",val[2].strip()," highway for ",val[0]," miles.\nEstimated time is: ",str(time)," mins."
	return cities+route[i+1]

'''
Formats the output in human-readable format giving the list of directions consisting of 
intermediate cities, times, distances and then prints a machine readable format as specified.
Input:
	path- dictionary containing the computed (distance,time,scenic,segment,path) for the end-city
	mapData- dictionary containing the list of cities along with the information about their 
			 neighboring cities			
'''
def formatOutput(path,mapData):
	route=path["path"].split("\n")
	cities=printPath(route,mapData)
	print "Your destination has been reached."
	totTime=path["time"]
	if(totTime>=60):
		totHours=int(totTime)/60
		totMins=totTime%60
		print "The total time is: ",totHours," hour ",totMins," mins."
	else:
		print "The total time is: ",totTime," mins."
	print "Total number of turns (segments): ",path["segment"]
	print "Distance spent on highways: ",path["scenic"]
	print "The total distance is: ",path["distance"]," miles."
	print str(path["distance"])+" "+str(round(float(path["time"])/60,4))+" "+cities

# Runs the code
#start=time.time()
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
		if path:
			formatOutput(path,mapData)
		else:
			print "No path found between start city ", startCity," and end city ",endCity
#end=time.time()
#print "time to run the algorithm: ",round((end-start),3)
