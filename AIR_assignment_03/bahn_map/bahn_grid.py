"""
Created on 28.04.2014

@author: Joschka Rick
"""
from _mysql import connect
from operator import ne

from random import randint
from graph import Node
from math import sqrt, floor


def enum(**enums):
    return type('Enum', (), enums)

SearchAlgorithm = enum(A_STAR=0)


def get_random_map(number_of_stations=3000, width=1000, height=1000):
    m = Map(width=width, height=height)
    while m.get_station_count() < number_of_stations:
        x = randint(0, width-1)
        y = randint(0, height-1)

        if m.is_free((x, y)):
            station = Station(x, y)
            m.add_station(station)

    stations = m.get_stations()
    for station in stations:
        for i in xrange(10):
            index = randint(0, len(stations)-1)
            station.neighbours.append(stations[index])

    m.draw_grid()
    return m
    pass


def execute_a_star(start_station, goal_station):
    start_node = Node(None,
                      start_station,
                      heuristic_cost=start_station.distance_to(goal_station))
    open_list = [start_node]
    closed_list = list()

    while open_list:
        current_node = open_list.pop(0)

        if current_node.station == goal_station:
            return current_node

        closed_list.append(current_node)

        for neighbour in current_node.station.neighbours:
            heuristic_costs = floor(current_node.station.distance_to(neighbour))
            edge_costs = heuristic_costs + randint(0, int(heuristic_costs / 2))
            node = Node(current_node,
                        neighbour,
                        path_cost=edge_costs+current_node.get_path_cost(),
                        heuristic_cost=heuristic_costs)

            if node in closed_list:
                continue

            if node in open_list:
                for open_node in open_list:
                    if open_node < node:
                        continue
                    else:
                        open_list.remove(open_node)

            open_list.append(node)
            pass
        open_list.sort(key=lambda n: n.get_total_cost())

    return None
    pass


def find_path(start_station, goal_station, algorithm=SearchAlgorithm.A_STAR):
    if algorithm == SearchAlgorithm.A_STAR:
        return execute_a_star(start_station, goal_station)
    pass


class Map(object):
    
    def __init__(self, width, height, stations=[]):
        self.width = width
        self.height = height
        self.stations = stations
        self.__grid = [[]]
        self.fill_grid()
        pass

    def add_station(self, station):
        self.stations.append(station)
        self.fill_grid()

    def fill_grid(self):
        self.__grid = [[None for y in xrange(self.height)] for x in xrange(self.width)]
        for station in self.stations:
            self.__grid[station.x][station.y] = station

    def get_stations(self):
        return self.stations

    def draw_grid(self):
        print ('-' for i in xrange(len(self.__grid[0])))
        print ('\n'.join(''.join(' ' if cell is None else 's' for cell in row)
                         for row in self.__grid))
        pass

    def navigate(self, start_position=(0, 0), goal_position=(1, 1)):
        start_station = self.find_nearest_station(start_position)
        goal_station = self.find_nearest_station(goal_position)
        if not start_station:
            return None

        print "start_station found:", start_station
        print "goal_station found:", goal_station

        return find_path(start_station, goal_station)
        pass

    def is_free(self, position):
        if self.__grid[position[0]][position[1]]:
            return False
        return True
        pass

    def get_station_count(self):
        return len(self.stations)

    def find_nearest_station(self, start_pos):
        discovered = list()
        start_node = start_pos
        queue = [start_node]

        while queue:
            current_node = queue.pop(0)

            station_found = self.__grid[current_node[0]][current_node[1]]

            if station_found:
                return station_found

            if current_node not in discovered:
                discovered.append(current_node)

                new_nodes = self.expand_position_node(current_node)

                if new_nodes:
                    queue += new_nodes

        return None

    def expand_position_node(self, node):
        expanded_nodes = list()
        for x in xrange(-1, 2):
            for y in xrange(-1, 2):
                new_node = (node[0] + x, node[1] + y)
                if (0 <= new_node[0] < self.width
                    and 0 <= new_node[1] < self.height
                    and not (new_node[0] == node[0]
                             and new_node[1] == node[1])):
                    expanded_nodes.append(new_node)
                    pass

        return expanded_nodes
    pass


class Station(object):

    def __init__(self, x, y, neighbours=[]):
        self.neighbours = neighbours
        self.x = x
        self.y = y

    def distance_to(self, other_station):
        xd = self.x - other_station.x
        yd = self.y - other_station.y
        return sqrt((xd * xd) + (yd * yd))
        pass

    def __str__(self):
        return str("Station at (" + str(self.x) + "," + str(self.y) + ")")

    def __eq__(self, other_station):
        if self.x == other_station.x and self.y == other_station.y:
            return True
        return False

    def __ne__(self, other_station):
        return not self == other_station
    pass
