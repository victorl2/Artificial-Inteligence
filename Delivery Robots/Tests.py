from State import *
from random import randint
from Product import *
from Order import *
from Robot import *
from Package import *
from bisect import *

def generate_case():
    state = State()

    #Generating ROBOTS
    for i in range(0, randint(2, 4)):
        robot = Robot(randint(0, 10), randint(0, 10))
        if (randint(0, 10) < 4):
            robot.state = "on_delivery"
            robot.time = randint(3, 22)
            insort(state.delivery, robot)
        else:
            state.idle.append(robot)

    total_prods = randint(1, 4)

    #GENERATING PRODUCTS
    for i in range(0, total_prods):
        prod = Product(randint(0, 10), randint(0, 10))
        state.products.append(prod)

    total_packs = randint(1, 4)

    #GENERATING PACKING STATIONS
    for i in range(0, total_packs):
        pack = Pack(randint(0, 10), randint(0, 10))
        state.packs.append(pack)

    #GENERATING ORDERS
    for i in range(1, 5):
        product = state.products[randint(0, total_prods - 1)]
        packing = state.packs[randint(0, total_packs - 1)]
        order = Order(product, packing)
        state.orders.append(order)
    return state

def basic_test():
    state = State()

    prod1 = Product(5,5)
    prod2 = Product(10,10)
    state.products.append(prod1)
    state.products.append(prod2)

    robot1 = Robot(0,0)

    robot2 = Robot(1,1)
    robot2.state = "on_delivery"
    robot2.time = 12

    state.idle.append(robot1)
    state.delivery.append(robot2)

    pack = Pack(3,3)
    state.packs.append(pack)

    order1 = Order(prod1,pack)
    order2 = Order(prod2,pack)

    state.orders.append(order1)
    state.orders.append(order2)


    return state

def aline_test():
    state = State()
    r1 = Robot(20,14)
    r2 = Robot(20,20)
    r3 = Robot(20,0)

    r1.time = 14
    r2.time = 8
    r3.time = 8

    r1.state = "on_delivery"
    r2.state = "on_delivery"
    r3.state = "on_delivery"

    insort(state.delivery,r1)
    insort(state.delivery,r2)
    insort(state.delivery,r3)

    pack1 = Pack(20,0)
    pack2 = Pack(20,10)
    pack3 = Pack(20,20)

    state.packs.append(pack1)
    state.packs.append(pack2)
    state.packs.append(pack3)

    prod1 = Product(0,0)
    prod2 = Product(0,10)
    prod3 = Product(0,20)

    state.products.append(prod1)
    state.products.append(prod2)
    state.products.append(prod3)

    ord1 = Order(prod1,pack1)
    ord2 = Order(prod2,pack2)
    ord3 = Order(prod3,pack3)

    state.orders.append(ord1)
    state.orders.append(ord2)
    state.orders.append(ord3)
    return state

def test2():
    state = State()
    r1 = Robot(20,14)
    r2 = Robot(20,20)
    r3 = Robot(20,0)

    r1.time = 14
    r2.time = 8
    r3.time = 8

    r1.state = "on_delivery"
    r2.state = "on_delivery"
    r3.state = "on_delivery"

    insort(state.delivery,r1)
    insort(state.delivery,r2)
    insort(state.delivery,r3)

    pack1 = Pack(20,0)
    pack2 = Pack(20,10)
    pack3 = Pack(20,20)

    state.packs.append(pack1)
    state.packs.append(pack2)
    state.packs.append(pack3)

    prod1 = Product(0,0)
    prod2 = Product(0,10)
    prod3 = Product(0,20)

    state.products.append(prod1)
    state.products.append(prod2)
    state.products.append(prod3)

    ord1 = Order(prod1,pack1)
    ord2 = Order(prod1,pack2)
    ord3 = Order(prod1,pack3)
    ord4 = Order(prod2, pack1)
    ord5 = Order(prod2, pack2)
    ord6 = Order(prod2, pack3)
    ord7 = Order(prod3, pack1)
    ord8 = Order(prod3, pack2)
    ord9 = Order(prod3, pack3)

    state.orders.append(ord1)
    state.orders.append(ord2)
    state.orders.append(ord3)
    state.orders.append(ord4)
    state.orders.append(ord5)
    state.orders.append(ord6)
    state.orders.append(ord7)
    state.orders.append(ord8)
    state.orders.append(ord9)
    return state
