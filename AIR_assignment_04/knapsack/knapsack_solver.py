__author__ = 'Fernando Morillo, Joschka Rick'


import copy
from random import randint


def find_local_min(file_path):
    """
    This function loads objects from the specified text file and finds the local maximum,
    starting with a randomly filled knapsack.
    """
    print "\n\n--------------------------------------------------------------------------------"
    print "Finding solution for", file_path

    # Open file at given path
    f = open(file_path, 'r')

    # Read the first line
    first_line = f.readline()

    # Remove linebreak at the end
    first_line = first_line[:-1]

    # Cast to float, in case it's a float as string, and to int
    weight_limit = int(float(first_line))

    # Load each line as a dictionary with index, weight and profit
    objects = []
    for line in f:
        i = line.split(' ')
        objects.append({'index': int(i[0]), 'weight': int(i[1]), 'profit': int(i[2][:-1])})

    # Sort the list by efficiency profit/weight
    sorted_objects = sorted(objects, key=lambda o: (o['profit'] / o['weight']), reverse=True)

    # Create an initial solution
    knapsack = get_initial_solution(weight_limit, objects)
    knapsack_old = Knapsack(0, profit=-1)

    print "Initial knapsacks... \t\t\t", knapsack

    # While the new neighbour is better than the old one
    while knapsack.profit > knapsack_old.profit:

        # Safe the old knapsack to compare profits
        knapsack_old = copy.deepcopy(knapsack)

        # Remove objects from the knapsack until there is enough space for at least one new object
        resume_popping = True
        while resume_popping:
            deleted_o = knapsack.pop()
            print "\tRemoved:\t", deleted_o

            # Add the fitting object with the highest efficiency until the knapsack is full
            while add_best_fit(knapsack, sorted_objects, deleted_o):
                resume_popping = False

        print "\nNew neighbouring solution... \t", knapsack

    # If the while loop broke, knapsack_old contains the local maximum
    return knapsack_old


def add_best_fit(k, sorted_objects, deleted_o):
    """
    This function finds the fitting object with the highest efficiency for k.
    """

    # Be sure to not exceed the objects count
    index = 0
    while index < len(sorted_objects):
        current_o = sorted_objects[index]

        # Don't add the just deleted item
        if current_o == deleted_o:
            index += 1
            continue

        # Don't add objects twice
        if current_o in k.objects:
            index += 1
            continue

        # Don't add if the weight would be too high
        if (current_o['weight'] + k.weight) >= k.weight_limit:
            index += 1
            continue

        print "\tAdded:\t\t", current_o

        # If not terminated yet, add the object to the knapsack
        k.add_object(current_o)

        return current_o

    return None


def get_initial_solution(weight_limit, objects):
    """
    This function creates an initial randomly filled knapsack.
    """
    k = Knapsack(weight_limit)

    # Get a random start position
    start_pos = randint(0, len(objects)-1)
    index = start_pos

    # Fill from start position until knapsack is full
    while k.add_object(objects[index]):
        index = (index + 1) % len(objects)

        # If we circle, break!
        if index == start_pos:
            break

    return k


class Knapsack(object):
    """
    This class represents a knapsack with a limited weight, a weight, a profit and all containing objects.
    This class is used as a solution for the local search problem.
    """

    def __init__(self, weight_limit, weight=0, profit=0):
        self.weight_limit = weight_limit
        self.weight = weight
        self.profit = profit
        self.objects = []

    def add_object(self, added_o):
        """
        This function adds an object to the knapsack, if possible.
        """

        # If weight would be too high, return False
        if (self.weight + added_o['weight']) > self.weight_limit:
            return False

        # Sum up the weight and profit
        self.weight += added_o['weight']
        self.profit += added_o['profit']

        self.objects.append(added_o)
        return True

    def pop(self):
        """
        This function removes the first item of the objects list of the knapsack
        and reduces the weight and profit accordingly.
        """

        if len(self.objects) == 0:
            return None

        deleted_o = self.objects.pop(0)

        # Reduce weight and profit
        self.weight -= deleted_o['weight']
        self.profit -= deleted_o['profit']
        return deleted_o

    def to_string(self):
        """
        This function prints the current state of the knapsack, including all objects.
        """
        print "\nSolution... \t\t\t\t\t", str(self)
        print "\n\tIndex:\tWeight:\tProfit:"
        for o in self.objects:
            print "\t" + str(o['index']) + "\t\t" + str(o['weight']) + "\t\t" + str(o['profit'])

    def __str__(self):
        """
        This function prints the current state of the knapsack.
        """
        return "[profit: " + str(self.profit)\
               + ", weight: " + str(self.weight)\
               + ", objects_count: " + str(len(self.objects))\
               + "]"
