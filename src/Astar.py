import heapq
import pathPlanner as p

class PriorityQueue:
	def __init__(self):
		self.elements = []

	def empty(self):
		return len(self.elements) == 0

	def put(self, item, priority):
		heapq.heappush(self.elements, (priority, item))

	def get(self):
		return heapq.heappop(self.elements)[1]

class Grid:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.walls = []

	def inbound(self, id):
		(x, y) = id
		return 0 <= x < self.width and 0 <= y < self.height

	def passable(self, id):
		return id not in self.walls

	def neighbors(self, id):
		(x, y) = id
		results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
		if (x + y) % 2 == 0: results.reverse() 
		results = filter(self.inbound, results)
		results = filter(self.passable, results)
		return results

class GridWeights(Grid):
	def __init__(self, width, height):
		super().__init__(width, height)
		self.weights = {}

	def cost(self, fromnode, tonode):
		return self.weights.get(tonode, 1)


def dist_to_goal(a, b): #Simple distance heruristic
	(x1, y1) = a
	(x2, y2) = b
	return abs(x1 - x2) + abs(y1 - y2)

def a_star(graph, start, goal):
	frontier = PriorityQueue()
	frontier.put(start, 0) #Push start to the priority queue
	camefrom = {}
	costsofar = {}
	camefrom[start] = None
	costsofar[start] = 0

	while not frontier.empty(): #If the grid is not empty
		current = frontier.get() #Pop the current element 

		if (current == goal): 
			break

		for nextthing in graph.neighbors(current): #Looks at neighbors of the current cell 
			newcost = costsofar[current] + graph.cost(current, nextthing) #Looks at costs of moving to other cells

			if nextthing not in costsofar or newcost < costsofar[nextthing]: #Update
				costsofar[nextthing] = newcost
				priority = newcost + dist_to_goal(goal, nextthing)
				frontier.put(nextthing, priority)
				camefrom[nextthing] = current

	return camefrom, costsofar

def path(camefrom, start, goal): #Translates camefrom list into an actual path
	current = goal 
	path = []
	while current != start:
		path.append(current)
		currnet = came_from[current]
	path.append(start)
	path.reverse()
	return path

def main():
	p.world_map = WorldMap()
	p.world_map.set_feature((1,.15),(1,0.25), OBSTACLE)
	p.world_map.set_feature((1.5,0.8),(1.7,1), GOAL)
	p.world_map.inflate()
	p.world_map.print_obs_map()

	path(a_star(p.world_map, (0,0), (5,5)), (0,0), (5,5))
if __name__ == "__main__":
	main()
	exit(0)