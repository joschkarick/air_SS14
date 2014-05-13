__author__ = 'Joschka Rick, Fernando Morillo'


import math as m
import copy


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


Modes = enum('LINE_NUMBER', 'EUCLIDEAN_DISTANCE', 'CLOSEST_TO_DEADLINE')


def load_scenario(file_path):
    """
    Generates a scenario instance from the given file path.
    """
    f = open(file_path)

    x, y = f.readline().split(' ')
    x = float(x)
    y = float(y)
    start_pos = (x, y)

    packages = list()
    for line in f:
        x, y, deadline = line[:-1].split(' ')
        packages.append({'x': float(x), 'y': float(y), 'deadline': float(deadline)})

    return Scenario(start_pos, packages)


class Scenario(object):
    """
    This class represents one CSP delivery robot problem.
    """

    def __init__(self, start_pos, packages):
        self.start_pos = start_pos
        self.packages = packages

    def find_solution(self, mode=Modes.LINE_NUMBER):
        """
        This function executes a DFS search with backtracking to find a solution for the problem.
        """
        packages = copy.deepcopy(self.packages)

        # Initial node
        packages.insert(0, {'x': self.start_pos[0], 'y': self.start_pos[1], 'deadline': 0})

        # Init variable to count evaluation of constraint satisfactions
        self.evaluate_satisfaction = 0

        # Get the solution
        return self.expand_node(0, packages, 0, mode=mode), self.evaluate_satisfaction

    def expand_node(self, current_package_index, packages, exec_time, mode):
        """
        This function is call recursively to find the solution to the problem.
        current_package_index: The index in the list of packages which contains the next node.
        packages: A list with all remaining packages.
        exec_time: The current time which already passed.
        mode: The mode for sorting the successors.
        """
        current_package = packages.pop(current_package_index)

        # Sort the remaining packages according to the mode
        if mode == Modes.LINE_NUMBER:
            pass
        elif mode == Modes.EUCLIDEAN_DISTANCE:
            packages = sorted(packages, key=lambda p: get_euclidean_distance(current_package, p))
        elif mode == Modes.CLOSEST_TO_DEADLINE:
            packages = sorted(packages, key=lambda p: p['deadline'] - exec_time)
            pass

        # Check if goal reached
        if len(packages) == 0:
            # If yes, return the execution time and a list with the current package
            return exec_time, [current_package]

        # For each remaining package
        for i, package in enumerate(packages):

            # Get the new execution time for the package, based on the existing and the euclidean distance
            new_exec_time = exec_time + get_euclidean_distance(current_package, package)

            # Check the constraint satisfaction
            self.evaluate_satisfaction += 1
            if not package['deadline'] > new_exec_time:
                return None

            # Call recursively
            res = self.expand_node(i, copy.deepcopy(packages), new_exec_time, mode=mode)

            # If something was returned, the constraints were satisfied
            if res:
                # Append the current node to the list
                res_exec_time, res_backtrack = res
                res_backtrack.insert(0, current_package)
                return res_exec_time, res_backtrack

        return None

    pass


def get_euclidean_distance(a, b):
    return m.sqrt(pow(a['x'] - b['x'], 2) + pow(a['y'] - b['y'], 2))
