class ArquivoPolifasica:
    def __init__(self, lists: list = []) -> None:
        self._sequencias = lists
        self._writeOps = 0

    def __str__(self)->str:
        string = "{"
        for seq in self._sequencias:
            string += str(seq)
        string += "}"
        return string

    @property
    def isEmpty(self)->bool:
        return len(self._sequencias) == 0 or (len(self._sequencias) == 1 and len(self._sequencias[0]) == 0)

    @property
    def sequencias(self)->list:
        return self._sequencias

    @property
    def qtdRegistros(self)->int:
        n = 0
        for seq in self._sequencias:
            n += len(seq)
        return n
    
    @property
    def qtdSequencias(self)->int:
        n=0
        for seq in self._sequencias:
            if len(seq) > 0:
                n += 1
        return n

    @property
    def writeOps(self)->int:
        return self._writeOps

    def appendElemento(self, value:int):
        if len(self._sequencias)>0:
            self._sequencias[-1].append(value)
            self._writeOps += 1
        else:
            self._sequencias.append([value])
            self._writeOps += 1

    def appendSequencia(self, lista:list):
        self._sequencias.append(lista)
        self._writeOps += len(lista)

    # def congela(self)->None:
    #     if self._congelado:
    #         raise ValueError("Tentativa de congelar arquivo já congelado")
    #     self._congelado = True

    # def descongela(self)->None:
    #     if not self._congelado:
    #         raise ValueError("Tentativa de descongelar arquivo não congelado")
    #     self._congelado = False

    
