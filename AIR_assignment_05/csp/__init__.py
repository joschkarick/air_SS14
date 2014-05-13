__author__ = 'Joschka Rick, Fernando Morillo'


import glob


from delivery_robot import load_scenario, Modes

"""
for file_name in glob.glob('scenarios/*'):
    print "Calculating solution for " + file_name
    scenario = load_scenario(file_name)

    print "\tUsing Modes.LINE_NUMBER:"
    result, evaluations = scenario.find_solution(Modes.LINE_NUMBER)
    if result:
        exec_time, exec_path = result
        print "\t\tExecution time:  " + str(exec_time)
        print "\t\tNumber of Evals: " + str(evaluations)

    print "\tUsing Modes.EUCLIDEAN_DISTANCE:"
    result, evaluations = scenario.find_solution(Modes.EUCLIDEAN_DISTANCE)
    if result:
        exec_time, exec_path = result
        print "\t\tExecution time:  " + str(exec_time)
        print "\t\tNumber of Evals: " + str(evaluations)

    print "\tUsing Modes.CLOSEST_TO_DEADLINE:"
    result, evaluations = scenario.find_solution(Modes.CLOSEST_TO_DEADLINE)
    if result:
        exec_time, exec_path = result
        print "\t\tExecution time:  " + str(exec_time)
        print "\t\tNumber of Evals: " + str(evaluations)
"""


print "\tName\t\t\tModus\t\t\t\tTime\t\t\t#Evals"
for file_name in glob.glob('scenarios/*'):
    print "\t" + file_name.split('\\')[1],
    scenario = load_scenario(file_name)

    print "\tLINE_NUMBER",
    result, evaluations = scenario.find_solution(Modes.LINE_NUMBER)
    if result:
        exec_time, exec_path = result
        print "\t\t" + str(exec_time),
        print "\t" + str(evaluations)
    else:
        print "\t\tNo solution found"

    print "\t-------------",
    print "\tEUCLIDEAN_DISTANCE",
    result, evaluations = scenario.find_solution(Modes.EUCLIDEAN_DISTANCE)
    if result:
        exec_time, exec_path = result
        print "\t" + str(exec_time),
        print "\t" + str(evaluations)
    else:
        print "\tNo solution found"

    print "\t-------------",
    print "\tCLOSEST_TO_DEADLINE",
    result, evaluations = scenario.find_solution(Modes.CLOSEST_TO_DEADLINE)
    if result:
        exec_time, exec_path = result
        print "" + str(exec_time),
        print "\t" + str(evaluations)
    else:
        print "No solution found"