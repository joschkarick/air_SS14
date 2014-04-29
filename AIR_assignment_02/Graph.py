#!/usr/bin/env python

'''
Created on Apr 15, 2014

@author: Joschka Rick
'''

from Map import MapState


class Node(object):

    def __init__(self, indizes, map_state=0, neighbours=[], costs=0):
        object.__init__(self)
        self.indizes = indizes
        self.neighbours = neighbours
        self.map_state = map_state
        self.costs = costs
    pass

    def add_neighbour(self, neighbour):
        self.__neighbours.append(neighbour)
        pass

    def __cmp__(self, other):
        if ((self.indizes[0] == other.indizes[0])
            and (self.indizes[1] == other.indizes[1])):
            return 0
        else:
            if (self.costs > other.costs):
                return 1
        return -1

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "x=" + str(self.indizes[0] + 1) \
            + " y=" + str(self.indizes[1]) \
            + " dirty=" + str(self.map_state)
        pass
    pass


class Graph(object):

    def __init__(self, start_node=None):
        self.__start_node = start_node
        pass
    pass
