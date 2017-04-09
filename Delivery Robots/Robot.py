robots_total = 0  #amount of robots

#Class representing the robot which  delivers packages
class Robot:
    #Initializes a "idle" robot given it a name and starting position
    def __init__(self, x = 0 , y = 0 , name = 'r' ):
        self.x = x #default robot x coordinate before and after completing a order
        self.y = y #default robot y coordinate before and after completing a order
        self.state = "idle" #current robot state

        #Package and destination information
        self.time = 0  #time until the current delivery is finished ( no delivery is active, time = 0 )

        #Name of the robot, the default name is: "r1","r2",...,"rN"
        global robots_total
        robots_total += 1
        if name == 'r':
            self.name = 'r' + str(robots_total)
        else:
            self.name = name

    #Assigns the robot to one order
    def process_order(self,order):
        self.state = "on_delivery"
        x = abs(self.x - order.product.x)
        y = abs(self.y - order.product.y)

        #Total amount of time needed to process the order
        #(x + y): time needed to go pick up the product
        #(x - order.pack.x) + (y - order.pack.y):
        # time needed to go from the product position to the packing station
        self.time = (x + y) + abs(x - order.pack.x) + abs(y - order.pack.y)

    #A informative string of the current workings of the robot
    def status(self):
        if self.state == "idle":
            return self.name + ", " + self.state + ", (" + str(self.x) + "," + str(self.y) + ")"
        else:
            return self.name + ", " + self.state + ", (" + str(self.x) + "," + str(self.y) + ") ," + str(self.time)

    def __lt__(self, other):
        return self.time < other.time

