from bisect import *
import threading

weight = 2 #weight added to the heuristic function
#A representation of the state of the world.
#Multiple robots delivering packages simultaneously
class State:
    def __init__(self, state = None):
        self.back = state #father state ( state that originated this one )
        self.cost = 0
        self.time = 0 #total amount of time passed
        self.idle = [] #List of all idle robots
        self.delivery = [] #List of all robots on delivery
        self.products = [] #List of all avaliable products
        self.orders = [] #List containing all not atended orders
        self.packs = [] #List of all available packaging stations


    #Send the request for a robot complete a given order ( only the request, not the action )
    def execute_order(self ,robot ,order):
        for co in self.orders:
            if co == order:
                self.orders.remove(co)
                break
        else:
            raise ValueError("The \"order\" provided is not in the orders list")

        robot.process_order(order)
        t1 = threading.Thread(target=insort, args =(self.delivery,robot,))
        t2 = threading.Thread(target=self.idle.remove,args=(robot,))

        t1.start()
        t2.start()

        t1.join()
        t2.join()


    #Progress though time x units, where x is the time required to finish the fastest
    #delivery currently being performed by a robot
    #h_active: True = calculate cost with heuristic , False = no heuristic (cost = time) ]
    def progress_time(self,h_active):

        passed = 0
        if self.delivery:

            robot = self.delivery.pop(0) #pick up the robot doing the fastest delivery
            passed = robot.time #time needed to perform the fastest delivery
            self.time+= passed #add the time of the action on the total time counter

            #calculate the cost for the current state
            if h_active:
                self.cost = self.time + self.heuristic()
            else:
                self.cost = self.time

            robot.state="idle"
            robot.time = 0
            self.idle.append(robot)

            #correct the time needed for all other robots
            v = 0
            while (v < len(self.delivery)):
                r = self.delivery[v]
                r.time -= passed
                if r.time <= 0:
                    r.state = "idle"
                    self.delivery.pop(v)
                    self.idle.append(r)
                else:
                    v+=1
        return passed

    #Check if this is the END state ( no more orders and all robots are idle )
    def is_complete(self):
        if (self.orders or self.delivery):
            return False
        return True

    def status(self):
        idles = ""
        deliver = ""
        ord = ""
        result = ""
        for i in range(0,len(self.idle)):
            idles += "[ "+ self.idle[i].status() + "]; "

        for i in range(0,len(self.delivery)):
            deliver += "[ "+self.delivery[i].status() + "]; "


        for i in range(0,len(self.orders)):
            ord += "[ "+ self.orders[i].status() + "]; "

        result+=("TIME: " + str(self.time) + "\n")
        if idles:
            result +=("IDLE:" + idles + "\n")
        else:
            result +=("IDLE: 'is empty'\n")
        if deliver:
            result +=("ON_DELIVERY:" + deliver + "\n")
        else:
            result +=("ON_DELIVERY: 'is empty'\n")
        if ord:
            result +=("ORDERS:" +ord + "\n")
        else:
            result +=("ORDERS: 'is empty'" +"\n")
        return result


    #Defining equality betwen the objects of this type ( we can use state == state2 )
    def __eq__(self, other):
        if self.cost != other.cost:
            return False

        high = [len(self.orders) , len(self.idle) , len(self.delivery) ]
        maximum = max(high)

        if len(self.orders) != len(other.orders):
            return False
        if len(self.idle) != len(other.idle):
            return False
        if len(self.delivery) != len(other.delivery):
            return False

        for i in range(0,maximum):
            if(high[0] > i):
                if self.orders[i] != other.orders[i]:
                    return False
            elif(high[1] > i):
                if self.idle[i] != other.idle[i]:
                    return False
            elif(high[2] > i):
                if(self.delivery[i]!= other.delivery[i]):
                    return False
        return True

    #Implementing the operator "<" for the state object
    def __lt__(self,other):
        if self.cost < other.cost:
            return True
        return False

    #Implementing the operator "<=" for the state object
    def __le__(self, other):
        if self.__eq__(self,other) or self.cost < other.cost:
            return True
        return False

    #Implementing the operator ">=" for the state object
    def __ge__(self, other):
        if self.__eq__(self,other) or self.cost > other.cost:
            return True
        return False

    #Implementing the operator ">" for the state object
    def __gt__(self, other):
        if self.cost > other.cost:
            return True
        return False

    #Heuristic function
    def heuristic(self):
        return len(self.orders) * 3

#Check if the current state is the solution
def solution(state):
    if state is None:
        return ""
    father = state.back
    return solution(father) + str("######################\n" + state.status())


#Check if the state was already seen previously and adjust the explored or frontier list
def state_verification(state,explored,frontier):
    #Check if the state was ALREADY explored
    if state in explored:
        return False
    #Check to see if the child is on the list TO BE explored
    elif state in frontier:
        # If we have a occurence we check to compare the cost and keep the lowest
        for i in range(0, len(frontier)):
            if frontier[i] == state and frontier[i].cost > state.cost:
                frontier[i] = state
                return False
    else:
        insort(frontier, state)

