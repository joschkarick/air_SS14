#!/usr/bin/env python
'''
            print "unset dirty"
Created on 28.04.2014

@author: Joschka Rick
'''

from map import Map, Station, SearchAlgorithm, get_random_map

station1 = Station(1, 1, None, path_cost=10, heuristic_cost=7)
station2 = Station(1, 1, None, path_cost=7, heuristic_cost=10)

print("1:", station1 == station2)
print("2:", station1 > station2)
print("3:", station1 < station2)
print("4:", station1 >= station2)
print("5:", station1 <= station2)
print("")
