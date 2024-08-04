from PolifasicaPackage.ArquivoPolifasica import ArquivoPolifasica

class DistribuidorPolifasica:
    def __init__(self, qtdArquivos:int, seqsInic:list[list[int]]):
        self._qtdArquivos = qtdArquivos
        self._seqsInic = seqsInic
        self._lastStep:list[int] = [0]*(qtdArquivos-1) + [1] #Configuração dos arquivos (quantidade de sequencias em cada um)
        self._steps:list[list[int]] = [list(self._lastStep)]

    @property
    def steps(self)->list[list[int]]:
        return list(self._steps)

    def addStep(self)->None:
        self._steps.append(list(self._lastStep))

    def firstStep(self)->None:
        for i in range(self._qtdArquivos):
            value:int = self._lastStep[i]
            if value == 0:
                self._lastStep[i] = 1
            else:
                self._lastStep[i] = 0
        self.addStep()

    def nextStep(self, maiorArquivo:int, indexmaiorArquivo:int)->None:
        for i in range(self._qtdArquivos):
            self._lastStep[i] += maiorArquivo
        self._lastStep[indexmaiorArquivo] = 0
        self.addStep()

    def reversePolifase(self)->None:
        self.firstStep()

        while sum(self._lastStep) < len(self._seqsInic):
            maiorArquivo = 0
            indexmaiorArquivo = 0
            for i in range(self._qtdArquivos):
                tamArquivo = self._lastStep[i]
                if tamArquivo > maiorArquivo:
                    maiorArquivo = tamArquivo
                    indexmaiorArquivo = i

            self.nextStep(maiorArquivo, indexmaiorArquivo)

    def criarArquivos(self)->list[ArquivoPolifasica]:
        self.reversePolifase()

        arquivos:list[ArquivoPolifasica] = []
        indexSeqAtual = 0
        for i in range(self._qtdArquivos):
            seqs:list[list[int]] = []
            qtdSeqs:int = self._lastStep[i]
            for _ in range(qtdSeqs):
                try:
                    seqs.append(self._seqsInic[indexSeqAtual])
                    indexSeqAtual += 1
                except:
                    seqs.append(["*"])

            arquivos.append(ArquivoPolifasica(seqs))

        return arquivos
