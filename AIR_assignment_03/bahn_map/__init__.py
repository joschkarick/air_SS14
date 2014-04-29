"""
Created on 28.04.2014

@author: Joschka Rick
"""
from bahn_grid import *

from bahn_grid import Map, Station, SearchAlgorithm, get_random_map, print_path

station1 = Station(1, 1)
station2 = Station(90, 90)
station1.neighbours = [station2]
station2.neighbours = [station1]

m2 = get_random_map(number_of_stations=50, width=100, height=100)
goal_station = m2.navigate((2, 2), (20, 20))
print print_path(goal_station)
