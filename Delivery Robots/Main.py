from copy import *
from Tests import *
from State import solution
import multiprocessing
import time

def uniform_cost_search(State):
    start = time.time()
    content = ("# UNIFORM COST SEARCH\n")
    content += search(State,False)
    end=str(time.time() - start)

    content+=("\n" + "*" * 60 + "\n")
    content +=(">Uniform cost search execution time: ")
    content +=(end.replace(end[4:], "")+"s\n")
    content +=("*" * 60 + "\n")
    print(content)


def a_star(State):
    start = time.time()
    content = ("####  A* SEARCH  #####\n")
    content += search(State,True)
    end = str(time.time() - start)

    content += ("\n" + "*" * 60 + "\n")
    content += (">A* search execution time: ")
    content += (end.replace(end[4:], "") + "s\n")
    content += ("*" * 60 + "\n")
    print(content)


def search(state , heuristic ):
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
            child.progress_time(heuristic)
            state_verification(child,explored,frontier)

        #Action: Alocate a robot to a order dont cost units time
        for i in range(0, len(state.idle)):
            for j in range(0, len(state.orders)):
                child = deepcopy(state)
                child.back = state

                #Alocate the idle robot 'i' to the order 'j'
                child.execute_order(child.idle[i],child.orders[j])
                state_verification(child,explored,frontier)

    return ""


if __name__ == "__main__":
    print("*" * 60)
    print("INITIAL STATE CONFIGURATION:")
    print("*" * 60)
    # MAIN EXECUTION
    state = generate_case()
    print(state.status())
    print("*" * 60)

    print("\n### OPTIONS ###")
    print("(1) Run both A* search and uniform cost search")
    print("(2) Run uniform cost search")
    print("(3) Run A* search")
    try:
        choice = int(input("Which option do you want?"))
        if(choice > 3 or choice < 1):
            print("\nInvalid input option, closing application.")
            exit(1)
    except ValueError:
        print("\nInvalid input option, closing application.")
        exit(1)

    print("*"*60)


    # UNIFORM COST SEARCH
    p1 = multiprocessing.Process(target=a_star, args=(state,))
    p2 = multiprocessing.Process(target=uniform_cost_search,args=(state,))


    #Starting each process
    if(choice == 1 or choice == 3):
        p1.start()
    if(choice == 1 or choice ==2):
        p2.start()

    print(">Executing search\n")

    #Wait the each process finish execution
    if (choice == 1 or choice == 3):
        p1.join()
    if (choice == 1 or choice == 2):
        p2.join()












