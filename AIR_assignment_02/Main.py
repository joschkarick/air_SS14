#!/usr/bin/env
'''
Created on Apr 15, 2014

@author: Joschka Rick
'''

from CleaningRobot import Robot, SearchAlgorithm
import timeit

# Create a robot with the first map and UNIFORM search algorithm
cr1 = Robot("maps/map1.txt", SearchAlgorithm.UNIFORM)
cr1.start_cleaning()

# Calculate 10 complete cleanings and print the average time
# print timeit.timeit('cr1.start_cleaning(); cr1.set_map(occupancy_map1)',
#                     'from __main__ import cr1, occupancy_map1',
#                     number=10)

cr2 = Robot("maps/map1.txt", SearchAlgorithm.DFS)
cr2.start_cleaning()

print "Finished."

#np.set_printoptions(threshold=np.nan)
