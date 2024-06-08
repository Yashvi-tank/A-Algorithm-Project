import math
from queue import PriorityQueue

class HashTable:
    # Initialize the hash table with a given size
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]

    # Generate a hash for the given key
    def _hash(self, key):
        return hash(key) % self.size

    # Add or update the key-value pair in the hash table
    def set(self, key, value):
        hashed_key = self._hash(key)
        for i, (k, v) in enumerate(self.table[hashed_key]):
            if k == key:
                self.table[hashed_key][i] = (key, value)
                return
        self.table[hashed_key].append((key, value))

    # Retrieve the value associated with the given key
    def get(self, key):
        hashed_key = self._hash(key)
        for k, v in self.table[hashed_key]:
            if k == key:
                return v
        return None

    # Check if the key exists in the hash table
    def __contains__(self, key):
        return self.get(key) is not None

class City:
    # Initialize the city with its name and coordinates
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = HashTable()

    # Add a neighboring city and the distance to it
    def add_neighbor(self, neighbor, distance):
        self.neighbors.set(neighbor, distance)

# Calculate the Euclidean distance between two cities
def euclidean_distance(city1, city2):
    return math.sqrt((city1.x - city2.x)**2 + (city1.y - city2.y)**2)

# A* algorithm to find the shortest path between start and goal cities
def a_star_algorithm(start, goal, cities):
    open_set = PriorityQueue()
    open_set.put((0, start))
    
    g_score = HashTable(len(cities))
    for city in cities:
        g_score.set(city, float('inf'))
    g_score.set(start, 0)
    
    f_score = HashTable(len(cities))
    for city in cities:
        f_score.set(city, float('inf'))
    f_score.set(start, euclidean_distance(start, goal))
    
    came_from = HashTable(len(cities))

    while not open_set.empty():
        _, current = open_set.get()
        
        if current == goal:
            return reconstruct_path(came_from, current, g_score)
        
        for bucket in current.neighbors.table:
            for neighbor, distance in bucket:
                tentative_g_score = g_score.get(current) + distance
                if tentative_g_score < g_score.get(neighbor):
                    came_from.set(neighbor, (current, distance))
                    g_score.set(neighbor, tentative_g_score)
                    f_score.set(neighbor, g_score.get(neighbor) + euclidean_distance(neighbor, goal))
                    open_set.put((f_score.get(neighbor), neighbor))
    
    return None

# Reconstruct the path from start to goal
def reconstruct_path(came_from, current, g_score):
    total_path = [(current, g_score.get(current))]
    
    while current in came_from:
        current, distance = came_from.get(current)
        total_path.append((current, g_score.get(current)))
    
    total_path.reverse()
    return total_path, g_score.get(total_path[-1][0])

# cities setup as nodes of graph
calais = City("Calais", -200, 1200)
caen = City("Caen", -600, 730)
paris = City("Paris", -190, 640)
nancy = City("Nancy", 510, 600)
rennes = City("Rennes", -910, 480)
brest = City("Brest", -1400, 560)
nantes = City("Nantes", -910, 220)
limoges = City("Limoges", -380, -190)
bordeaux = City("Bordeaux", -740, -470)
strasbourg = City("Strasbourg", 800, 600)
dijon = City("Dijon", 315, 220)
lyon = City("Lyon", 290, -215)
toulouse = City("Toulouse", -350, -830)
grenoble = City("Grenoble", 470, -370)
avignon = City("Avignon", 310, -730)
montpellier = City("Montpellier", 120, -830)
marseille = City("Marseille", 430, -910)
nice = City("Nice", 810, -790)

# Adding the neighbors for each city
calais.add_neighbor(caen, 450)
calais.add_neighbor(paris, 297)
calais.add_neighbor(nancy, 534)

caen.add_neighbor(paris, 241)
caen.add_neighbor(calais, 450)
caen.add_neighbor(rennes, 176)

paris.add_neighbor(calais, 297)
paris.add_neighbor(nancy, 297)
paris.add_neighbor(caen, 241)
paris.add_neighbor(rennes, 348)
paris.add_neighbor(limoges, 396)

nancy.add_neighbor(paris, 372)
nancy.add_neighbor(strasbourg, 145)
nancy.add_neighbor(dijon, 201)
nancy.add_neighbor(calais, 534)

strasbourg.add_neighbor(nancy, 145)
strasbourg.add_neighbor(dijon, 335)

dijon.add_neighbor(nancy, 201)
dijon.add_neighbor(strasbourg, 335)
dijon.add_neighbor(lyon, 192)

rennes.add_neighbor(caen, 176)
rennes.add_neighbor(nantes, 107)
rennes.add_neighbor(paris, 348)
rennes.add_neighbor(brest, 244)

limoges.add_neighbor(bordeaux, 329)
limoges.add_neighbor(nantes, 329)
limoges.add_neighbor(lyon, 389)
limoges.add_neighbor(paris, 396)
limoges.add_neighbor(toulouse, 313)

nantes.add_neighbor(rennes, 107)
nantes.add_neighbor(limoges, 329)
nantes.add_neighbor(bordeaux, 329)

bordeaux.add_neighbor(limoges, 220)
bordeaux.add_neighbor(toulouse, 259)
bordeaux.add_neighbor(nantes, 329)

toulouse.add_neighbor(bordeaux, 259)
toulouse.add_neighbor(limoges, 313)
toulouse.add_neighbor(montpellier, 240)

montpellier.add_neighbor(toulouse, 240)
montpellier.add_neighbor(avignon, 91)

lyon.add_neighbor(limoges, 389)
lyon.add_neighbor(dijon, 192)
lyon.add_neighbor(grenoble, 104)
lyon.add_neighbor(avignon, 216)

avignon.add_neighbor(lyon, 216)
avignon.add_neighbor(grenoble, 227)
avignon.add_neighbor(montpellier, 91)
avignon.add_neighbor(marseille, 99)

grenoble.add_neighbor(lyon, 104)
grenoble.add_neighbor(avignon, 227)

marseille.add_neighbor(avignon, 99)
marseille.add_neighbor(nice, 158)

nice.add_neighbor(marseille, 158)
brest.add_neighbor(rennes, 244)

# The list of all Cities
cities = [calais, caen, paris, nancy, rennes, brest, nantes, limoges, bordeaux,
          strasbourg, dijon, lyon, toulouse, grenoble, avignon, montpellier, marseille, nice]

# Run the algorithm
start_city = rennes  # Example start city
goal_city = lyon  # Example goal city
path, total_distance = a_star_algorithm(start_city, goal_city, cities)

# Print the result
if path:
    for city, dist in path:
        print(f"{city.name} : ({dist} km)")
    print(f"Total distance: {total_distance} km")
else:
    print("No path found")
