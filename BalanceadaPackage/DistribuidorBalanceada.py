from BalanceadaPackage.ArquivoBalanceada import ArquivoBalanceada

class DistribuidorBalanceada:
    def __init__(self, qtdArquivos:int, seqsInic:list[list[int]]):
        self._qtdArquivos = qtdArquivos
        self._seqsInic = seqsInic




    def criarArquivosEntrada(self)->dict[int:ArquivoBalanceada]:
        

        arquivos:dict[int: ArquivoBalanceada] = {index+1: ArquivoBalanceada() for index in range(self._qtdArquivos//2)}

        for i in range(len(self._seqsInic)):
            arquivos[(i)%(self._qtdArquivos//2)+1].appendSequencia(self._seqsInic[i])

        return arquivos
    
    def criarArquivosSaida(self)->dict[int: ArquivoBalanceada]:
        arquivos:dict[int: ArquivoBalanceada] = {index: ArquivoBalanceada() for index in range(1+self._qtdArquivos//2, self._qtdArquivos+1)}


        return arquivos

