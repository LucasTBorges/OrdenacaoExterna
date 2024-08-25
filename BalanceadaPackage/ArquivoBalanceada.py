class ArquivoBalanceada:
    def __init__(self, sequencias: list = []) -> None:
        self._sequencias = list(sequencias)
        self._writeOps = 0

    def __str__(self) -> str:
        string = ""
        for seq in self._sequencias:
            string += "{"
            for value in seq:
                string += f"{value} "
            string = string[:-1]
            string += "}"
        return string
    
    @property
    def isEmpty(self) -> bool:
        return len(self._sequencias) == 0

    @property
    def getSequencias(self) -> list:
        return self._sequencias
    
    @property
    def getWriteOps(self)->int:
        return self._writeOps
    
    @property
    def getQtdRegistros(self) -> int:
        n = 0
        for seq in self._sequencias:
            n += len(seq)
        return n
    
    @property
    def clear(self) -> None:
        self._sequencias.clear()
    
    @property
    def getQtdSequencias(self) -> int:
        n = 0
        for seq in self._sequencias:
            if len(seq)> 0:
                n += 1
        return n
    


    def appendSequencia(self, lista:list)->None:
        if len(lista)==0:
            return
        self._sequencias.append(lista)

    def removeSequencia(self, index: int) -> None:
        del self._sequencias[index]

    def appendNewSequencia(self, lista:list)->None:
        if len(lista) == 0:
            return
        self._sequencias.append(lista)
        self._writeOps += len(lista)    

    