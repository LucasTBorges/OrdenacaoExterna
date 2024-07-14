import No
class Heap:
    def __init__(self, m):
        self.Heap = []
        self.parent = None
        self.tamMax = m
        self.tam = 0
        

    def insert(self, value):
        if self.tam == self.tamMax:
            return
        
        self.tam += 1

        if self.parent == None:
            return
        
        noAtual = self.parent

        while True:
            if noAtual.childLeft == None:
                noAtual.childLeft.value = value
                return
            
            if noAtual.childRight == None:
                noAtual.childRight.value = value
                return
            
            


            

    