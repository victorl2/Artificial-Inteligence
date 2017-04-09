orders_total = 0 #amount of orders

class Order:
    def __init__(self,product, pack, name='o'):
        self.product = product #product object
        self.pack = pack #product to be delivered

        #Name of the order, the default name is: "order1","order2",...,"orderN"
        global orders_total
        orders_total+=1

        if name == 'o':
            self.name = "order" + str(orders_total)
        else:
            self.name = name

    #A informative string of the current order
    def status(self):
        origin = "(" + str(self.product.x) + "," + str(self.product.y) + ")"
        destiny = "(" + str(self.pack.x) + "," + str(self.pack.y) + ")"
        return self.name + ", " + origin + ", " + destiny

    def __eq__(self, other):
        return self.name == other.name
