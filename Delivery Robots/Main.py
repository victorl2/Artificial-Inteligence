from copy import *
from Tests import *
from State import solution
import time

def uniform_cost_search(state):
    frontier = [] #list with all states to expand
    explored = [] #list with all state already expanded
    frontier.append(state)

    while frontier:
        state = frontier.pop(0)

        #is the current state the end ?
        if state.is_complete():
            return solution(state)

        #add element and keep list sorted
        explored.append(state)

        #ADD ALL POSSIBLE ACTIONS TO THE FRONTIER LIST

        #Action:Progress time x units
        if state.delivery:
            child = deepcopy(state)
            child.back = state
            child.progress_time()
            state_verification(child,explored,frontier)

        #Action: Alocate a robot to a order dont cost units time
        for i in range(0, len(state.idle)):
            for j in range(0, len(state.orders)):
                child = deepcopy(state)
                child.back = state

                #Alocate the idle robot 'i' to the order 'j'
                child.execute_order(child.idle[i],child.orders[j])
                state_verification(child,explored,frontier)


#MAIN EXECUTION
counter_start = time.time()
print("##### BEGIN TEST #####")
state = aline_test()
uniform_cost_search(state)
print("\nTime elapsed:" + str(time.time() - counter_start))