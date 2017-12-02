# Implementation of Google Maps

- Created an implementation similar to Google Maps to find best possible driving directions from a source city to destination given the datasets for cities and highways in USA.

# Running the Code:
  `python route.py start-city end-city routing-opt routing-algorithm`
  
It takes following command-line arguments:
  1. start-city: start location
  2. end-city: destination location
  3. routing-opt is one of:
      1. segments finds a route with the fewest number of “turns” (i.e. edges of the graph)
      2. distance finds a route with the shortest total distance
      3. time finds the fastest route, for a car that always travels at the speed limit
      4. scenic finds the route having the least possible distance spent on highways (which we define as roads with speed limits 55 mph or greater)

  4. routing-algorithm is one of:
      1. bfs uses breadth-first search
      2. dfs uses depth-first search
      3. ids uses iterative deepening search
      4. astar uses A* search, with a suitable heuristic function
