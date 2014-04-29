'''
Created on 28.04.2014

@author: Joschka Rick
'''


from random import randint


def enum(**enums):
    return type('Enum', (), enums)

SearchAlgorithm = enum(A_STAR=0)


def get_random_map(number_of_stations=3000, width=1000, height=1000):
    for i in xrange(number_of_stations):
        station = Station()
        pass
    pass


class Map(object):
    
    def __init__(self, width, height, stations=[]):
        self.width = width
        self.height = height
        self.stations = stations
        pass

    def find_path(self, start_station, goal_station, algorithm=SearchAlgorithm.A_STAR):
        if algorithm == SearchAlgorithm.A_STAR:
            return self.execute_a_star(start_station, goal_station)
        pass
    
    def execute_a_star(self, start_station, goal_station):
        open_list = [start_station]
        closed_list = []
        while open_list:
            current_station = open_list.pop(0)
            
            if current_station == goal_station:
                return current_station
            
            closed_list.append(current_station)
            
            open_list.extend(self.expand_station(current_station))
        pass
    
    def expand_station(self, station):
        pass
    pass


class Station(object):

    def __init__(self, x, y, predecessor, successors=[], path_cost=0, heuristic_cost=0):
        self.predecessor = predecessor
        self.successor = successors
        self.x = x
        self.y = y
        self.__heuristic_cost = heuristic_cost
        self.__path_cost = path_cost
        self.__total_cost = path_cost + heuristic_cost
        
    def set_costs(self, path_cost=None, heuristic_cost=None):
        if path_cost:
            self.__path_cost = path_cost
            
        if heuristic_cost:
            self.__heuristic_cost = heuristic_cost
            
        self.__total_cost = self.__path_cost + self.__heuristic_cost
        pass
    
    def get_total_cost(self):
        return self.__total_cost
    
    def get_path_cost(self):
        return self.__path_cost
    
    def get_heuristic_cost(self):
        return self.__heuristic_cost

    def __eq__(self, other_station):
        if self.x == other_station.x and self.y == other_station.y:
            return True
        return False
    
    def __ne__(self, other_station):
        return not self == other_station
    pass
