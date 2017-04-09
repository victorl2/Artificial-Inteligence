products_total = 0 #amount of orders

class Product:
    def __init__(self, x, y, name = 'p'):
        #coordinates of where is the product
        self.x = x
        self.y = y

        #Name of the product, the default name is: "prod1","prod2",...,"prodN"
        global products_total
        products_total += 1

        if name == 'p':
            self.name = "prod" + str(products_total)
        else:
            self.name = name

    def status(self):
        return self.name + ", (" + str(self.x) + "," + str(self.y) + ")"