class DistribuidorPolifasica:
    def __init__(self, qtdArquivos:int, seqsInic:list[list[int]]):
        self._qtdArquivos = qtdArquivos
        self._seqsInic = seqsInic
        self._qtdSeqsArquivo:list[int] = [0]*(qtdArquivos-1) + [1] #Configuração dos arquivos (quantidade de sequencias em cada um)
        self._steps:list[list[int]] = [list(self._qtdSeqsArquivo)]

    @property
    def steps(self)->list[list[int]]:
        return list(self._steps)

    def addStep(self)->None:
        self._steps.append(list(self._qtdSeqsArquivo))

    def firstStep(self)->None:
        for i in range(self._qtdArquivos):
            value:int = self._qtdSeqsArquivo[i]
            if value == 0:
                self._qtdSeqsArquivo[i] = 1
            else:
                self._qtdSeqsArquivo[i] = 0
        self.addStep()

    def nextStep(self, maiorArquivo:int, indexmaiorArquivo:int)->None:
        for i in range(self._qtdArquivos):
            self._qtdSeqsArquivo[i] += maiorArquivo
        self._qtdSeqsArquivo[indexmaiorArquivo] = 0
        self.addStep()

    def reversePolifase(self)->None:
        self.firstStep()

        while sum(self._qtdSeqsArquivo) < len(self._seqsInic):
            maiorArquivo = 0
            indexmaiorArquivo = 0
            for i in range(self._qtdArquivos):
                tamArquivo = self._qtdSeqsArquivo[i]
                if tamArquivo > maiorArquivo:
                    maiorArquivo = tamArquivo
                    indexmaiorArquivo = i

            self.nextStep(maiorArquivo, indexmaiorArquivo)
