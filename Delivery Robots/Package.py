packs_total = 0 #amount of packing station

#Packing station which receives products
class Pack:
    def __init__(self, x, y , name = 'p'):
        self.x = x
        self.y = y

        global packs_total
        packs_total+= 1
        if name == 'p':
            self.name = "pack" + str(packs_total)
        else:
            self.name = name

    def status(self):
        return self.name + ", (" + str(self.x) + "," + str(self.y) + ")" \
                                                                     ""