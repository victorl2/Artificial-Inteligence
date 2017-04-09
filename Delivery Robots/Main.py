from copy import *
from Tests import *
from State import solution
import time


#AÇÕES POSSIVEIS
#Associar cada "robô" a uma "ordem"
#Avançar no tempo e finalizar uma ou mais ordens
#Um novo estado deverá ser associado a nova ação executada


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


#Check if the state was already seen previously and adjust the explored or frontier list
def state_verification(state,explored,frontier):
    #Check if the state was ALREADY explored
    if state in explored:
        return False
    #Check to see if the child is on the list TO BE explored
    elif state in frontier:
        # If we have a occurence we check to compare the cost and keep the lowest
        for i in range(0, len(frontier)):
            if frontier[i] == state and frontier[i].time > state.time:
                frontier[i] = state
                return False
    else:
        insort(frontier, state)


counter_start = time.time()
print("##### BEGIN TESTE #####")
state = aline_test()
uniform_cost_search(state)
print("\nTime elapsed:" + str(time.time() - counter_start))