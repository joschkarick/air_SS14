"""
Created on 28.04.2014

@author: Joschka Rick
"""


class Node(object):
    def __init__(self, predecessor, station, path_cost=0, heuristic_cost=0):
        self.station = station
        self.predecessor = predecessor
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


