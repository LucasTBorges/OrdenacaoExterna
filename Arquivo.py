class Arquivo:
    def __init__(self):
        self.lists = []
        self.wrightOps = 0

    def addList(self, list: list)->None:
        self.lists.append(list)
        self.wrightOps += len(list)

    def addElement(self, elemento: int)->None:
        self.lists[-1].append(elemento)

    def getListByIndex(self, indice: int)->list:
        return self.lists[indice]
    
    def getLists(self)->list:
        return self.lists