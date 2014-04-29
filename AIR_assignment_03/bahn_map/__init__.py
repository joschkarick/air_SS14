'''
Created on 28.04.2014

@author: Joschka Rick
'''
from bahn_grid import *

from bahn_grid import Map, Station, SearchAlgorithm, get_random_map, execute_a_star

station1 = Station(1, 1)
station2 = Station(10, 10)
station1.neighbours = [station2]
station2.neighbours = [station1]

m1 = Map(100, 100, [station1, station2])
m2 = get_random_map(number_of_stations=100, width=100, height=100)
print execute_a_star(station1, station2)
print m1.find_nearest_station((6, 6))
print m2.navigate((2, 2), (9, 9))