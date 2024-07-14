class Arquivo:
    def __init__(self):
        self.lists = []
        self.writeOps = 0

    def addList(self, list: list)->None:
        self.lists.append(list)
        self.writeOps += len(list)

    def addElement(self, elemento: int)->None:
        self.lists[-1].append(elemento)

    def getListByIndex(self, indice: int)->list:
        return self.lists[indice]
    
    def getLists(self)->list:
        return self.lists