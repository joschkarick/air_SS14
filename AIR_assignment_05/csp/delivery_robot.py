__author__ = 'Joschka Rick, Fernando Morillo'


import math as m
import copy


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


Modes = enum('LINE_NUMBER', 'EUCLIDEAN_DISTANCE', 'CLOSEST_TO_DEADLINE')


def load_scenario(file_path):
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

    def __init__(self, start_pos, packages):
        self.start_pos = start_pos
        self.packages = packages

    def find_solution(self, mode=Modes.LINE_NUMBER):
        packages = copy.deepcopy(self.packages)
        packages.insert(0, {'x': self.start_pos[0], 'y': self.start_pos[1], 'deadline': 0})
        self.evaluate_satisfaction = 0
        return self.expand_node(0, packages, 0, mode=mode), self.evaluate_satisfaction

    def expand_node(self, current_package_index, packages, exec_time, mode):
        current_package = packages.pop(current_package_index)

        if mode == Modes.LINE_NUMBER:
            pass
        elif mode == Modes.EUCLIDEAN_DISTANCE:
            packages = sorted(packages, key=lambda p: get_euclidean_distance(current_package, p))
        elif mode == Modes.CLOSEST_TO_DEADLINE:
            packages = sorted(packages, key=lambda p: p['deadline'] - exec_time)
            pass

        # Check if goal reached
        if len(packages) == 0:
            return exec_time, [current_package]

        for i, package in enumerate(packages):
            new_exec_time = exec_time + get_euclidean_distance(current_package, package)

            if not package['deadline'] > new_exec_time:
                self.evaluate_satisfaction += 1
                return None

            res = self.expand_node(i, copy.deepcopy(packages), new_exec_time, mode=mode)

            if res:
                res_exec_time, res_backtrack = res
                res_backtrack.insert(0, current_package)
                return res_exec_time, res_backtrack

        return None

    pass


def get_euclidean_distance(a, b):
    return m.sqrt(pow(a['x'] - b['x'], 2) + pow(a['y'] - b['y'], 2))
