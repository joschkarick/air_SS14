"""
Created on 28.04.2014

@author: Joschka Rick
"""
from _mysql import connect
from operator import ne

from random import randint
from math import sqrt, floor


def enum(**enums):
    return type('Enum', (), enums)

SearchAlgorithm = enum(A_STAR=0)


def get_random_map(number_of_stations=3000, width=1000, height=1000):
    """
    This function generates a random map with the given parameters.
    The stations are evenly distributed over the hole map.
    Each station is connect to up to 10 completely random stations.
    Returns the new map instance.
    """
    m = Map(width=width, height=height)

    # While there are less than `number_of_stations` stations, proceed.
    while m.get_station_count() < number_of_stations:
        x = randint(0, width-1)
        y = randint(0, height-1)

        # Only add the station if the position is free in the map.
        if m.is_free((x, y)):
            station = Station(x, y)
            m.add_station(station)

    # Go through each station and connect it to 10 neighbours.
    stations = m.get_stations()
    for station in stations:
        for i in xrange(10):
            index = randint(0, len(stations)-1)

            # Add the station to each other
            station.neighbours.append(stations[index])
            stations[index].neighbours.append(station)
    m.draw_grid()
    return m
    pass


def execute_a_star(start_station, goal_station):
    """
    This functions executes the A* algorithm on the given stations.
    It returns the goal node, which has predecessors, leading to the
    start node.
    """

    # Create the start node with start_station and add it to the open list.
    start_node = Node(None,
                      start_station,
                      heuristic_cost=start_station.distance_to(goal_station))
    open_list = [start_node]
    closed_list = list()

    # While there are unexplored nodes, proceed.
    while open_list:

        # The list will always contain the nodes sorted by total costs f.
        current_node = open_list.pop(0)

        # If the cheapest node in the list contains the goal station, a solution was found.
        if current_node.station == goal_station:
            return current_node

        closed_list.append(current_node)

        # Expand the current node
        # Go through each neighbour
        for neighbour in current_node.station.neighbours:

            # For each neighbour station create a node.
            # The heuristic costs are the euclidean distance.
            heuristic_costs = floor(current_node.station.distance_to(goal_station))

            # The edge costs are at least as high as the heuristic costs. Thus the heuristic function is admissible.
            edge_costs = heuristic_costs + randint(1, int(heuristic_costs / 2))
            node = Node(current_node,
                        neighbour,
                        # Add the edge costs to the precedessors path costs.
                        path_cost=edge_costs+current_node.get_path_cost(),
                        heuristic_cost=heuristic_costs)

            # If the neighbour was already processed, skip it.
            if node in closed_list:
                continue

            # If the node is in the open list, check what to do with it.
            if node in open_list:
                for open_node in open_list:

                    # If the existing open node is cheaper, skip the neighbour.
                    if open_node < node:
                        continue
                    # If not, remove the node. The new node will be added outside of the loop.
                    else:
                        open_list.remove(open_node)
                        break

            # If come so far, add the node to the open list.
            open_list.append(node)
            pass

        # After processing all neighbours, sort the open list by the total costs of each node.
        open_list.sort(key=lambda n: n.get_total_cost())

    return None
    pass


def find_path(start_station, goal_station, algorithm=SearchAlgorithm.A_STAR):
    """
    This function executes a path search with the given parameters.
    Returns the goal node.
    """
    if algorithm == SearchAlgorithm.A_STAR:
        return execute_a_star(start_station, goal_station)
    pass


class Map(object):
    """
    This class represents a map with a given size and several stations.
    """

    def __init__(self, width, height, stations=[]):
        self.width = width
        self.height = height
        self.stations = stations

        # Create a map grid 2D matrix
        self.__grid = None

        # Fill the map grid with the existing stations
        self.fill_grid()
        pass

    def add_station(self, station):
        """This function adds a station to the list and refills the map grid."""
        self.stations.append(station)
        self.fill_grid()

    def fill_grid(self):
        """This function takes every station in the list and places it in the map grid."""
        self.__grid = [[None for y in xrange(self.height)] for x in xrange(self.width)]
        for station in self.stations:
            self.__grid[station.x][station.y] = station

    def get_stations(self):
        """This function returns all stations of this map."""
        return self.stations

    def draw_grid(self):
        """This function draws an ASCII-art map, representing the current state."""
        print ('\n'.join(''.join(' ' if cell is None else 's' for cell in row)
                         for row in self.__grid))
        pass

    def navigate(self, start_position=(0, 0), goal_position=(1, 1)):
        """
        This function executes all necessary functions to find the goal node.
        The goal node contains the full path.
        """

        # Find the nearest station to the start and goal position.
        start_station = self.find_nearest_station(start_position)
        goal_station = self.find_nearest_station(goal_position)

        # In case there are no stations, return None
        if not start_station:
            return None

        print "start_station found:", start_station
        print "goal_station found:", goal_station

        # Execute a path search with A_STAR
        return find_path(start_station, goal_station, algorithm=SearchAlgorithm.A_STAR)
        pass

    def is_free(self, position):
        """This functions returns True when the map is free at the given position, otherwise false."""
        if self.__grid[position[0]][position[1]]:
            return False
        return True
        pass

    def get_station_count(self):
        return len(self.stations)

    def find_nearest_station(self, start_pos):
        """This function uses BFS to find the nearest station to a given position."""
        discovered = list()
        queue = [start_pos]

        # While there are nodes to explore, resume.
        while queue:
            # Get the most early added node.
            current_node = queue.pop(0)

            # Get the object at the given position.
            station_found = self.__grid[current_node[0]][current_node[1]]

            # If the object at the given position is None, there is no station there.
            if station_found:
                return station_found

            # Check if the node was already discovered.
            if current_node not in discovered:
                discovered.append(current_node)

                # Get the neighbours positions
                new_nodes = self.expand_position_node(current_node)

                # If there are neighbours, append them to the queue.
                if new_nodes:
                    queue += new_nodes

        # If no solution was found up to here, there is no station.
        return None

    def expand_position_node(self, node):
        """This function expands a position to all sides, including diagonals."""

        expanded_nodes = list()

        # Go from the top left corner to the bottom right.
        for x in xrange(-1, 2):
            for y in xrange(-1, 2):
                new_node = (node[0] + x, node[1] + y)

                # If the node is within the map and is not the same as the node to expand, safe it.
                if (0 <= new_node[0] < self.width
                    and 0 <= new_node[1] < self.height
                    and not (new_node[0] == node[0]
                             and new_node[1] == node[1])):
                    expanded_nodes.append(new_node)
                    pass

        return expanded_nodes
    pass


class Station(object):
    """
    This class represents a station with a position and connections to other stations.
    """

    def __init__(self, x, y, neighbours=[]):
        self.neighbours = neighbours
        self.x = x
        self.y = y

    def distance_to(self, other_station):
        """This function returns the euclidean distance to the other station."""
        xd = self.x - other_station.x
        yd = self.y - other_station.y
        return sqrt((xd * xd) + (yd * yd))
        pass

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str("Station at (" + str(self.x) + "," + str(self.y) + ")")

    def __eq__(self, other_station):
        if self.x == other_station.x and self.y == other_station.y:
            return True
        return False

    def __ne__(self, other_station):
        return not self == other_station
    pass


def print_path(node):
    for path_node in node.get_path():
        print path_node


class Node(object):
    """
    This class represents a node in the bahn search graph.
    """

    def __init__(self, predecessor, station, path_cost=0, heuristic_cost=0):
        self.station = station
        self.predecessor = predecessor
        self.__heuristic_cost = heuristic_cost
        self.__path_cost = path_cost
        self.__total_cost = path_cost + heuristic_cost

    def set_costs(self, path_cost=None, heuristic_cost=None):
        """This function sets the costs of the node."""
        if path_cost:
            self.__path_cost = path_cost

        if heuristic_cost:
            self.__heuristic_cost = heuristic_cost

        self.__total_cost = self.__path_cost + self.__heuristic_cost
        pass

    def get_path(self):
        """This function recursively builds the path from up the root node."""
        if self.predecessor is None:
            l = list()
            l.append(self)
            return l
        else:
            predecessor_path = self.predecessor.get_path()
            predecessor_path.append(self)
            return predecessor_path

    def get_total_cost(self):
        return self.__total_cost

    def get_path_cost(self):
        return self.__path_cost

    def get_heuristic_cost(self):
        return self.__heuristic_cost

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str("Node ("
                   + str(self.__path_cost) + " ; "
                   + str(self.__heuristic_cost) + " ; "
                   + str(self.__total_cost) + ")\n\t-> "
                   + str(self.station))

    def __eq__(self, other_node):
        if self.station.x == other_node.station.x and self.station.y == other_node.station.y:
            return True
        return False

    def __ne__(self, other_node):
        return not self == other_node

    def __cmp__(self, other):
        if self.__path_cost > other.__path_cost:
            return 1
        elif self.__path_cost < other.__path_cost:
            return -1
        else:
            return 0
    pass