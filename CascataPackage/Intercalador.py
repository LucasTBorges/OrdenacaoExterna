from CascataPackage.ArquivoCascata import ArquivoCascata
from CascataPackage.HeapCascata import HeapCascata
class Intercalador():
    def __init__(self, files: list[ArquivoCascata], targetFile:ArquivoCascata, heap: HeapCascata)->None:
        self._files = files
        self._targetFile = targetFile
        self._heap = heap
        self._seqsSizes = [file.getFirstSeqSize() for file in files]

    def intercala(self)->None:#Perdoe a falta de legibilidade
        #for i in range(self.nRegistros):
        currFile: int = 0 #Índice do arquivo que está sendo lido 
        #O bloco a seguir parece bizarro mas garanto que ele é eficiente, ele só parece bizarro, explico o porquê a seguir:

        iter:int = 0 #DEBUG ################## TODO: Remover

        while not self.done:
            #Vai executar exatamente n vezes, onde n é o número de registros a serem lidos
            while not self.ram.isFull and self.remaining > 0: #Enquanto tem espaço na memória e ainda tem registros a serem lidos vai carregando a heap com os registros
                #Na primeira iteração vai executar m vezes, onde m é o tamanho da memória principal, mas nas demais iterações vai executar apenas 1 vez (ou 0 vezes, nas últimas n-m iterações) 
                while self.seqsSizes[currFile] == 0: #Vai iterando pelos arquivos até encontrar um arquivo não vazio para carregar um registro dele na memória
                    #Vai executar no máximo k-1 vezes, onde k é o número de arquivos. Entretanto, no começo, quando o segundo while é executado pela primeira vez (e o único momento que roda mais de uma vez), não irá executar
                    currFile = (currFile + 1) % len(self.files)

                    iter += 1 #DEBUG ##################
                    if iter == 1000:
                        raise Exception("Loop infinito, 3º while")

                self.ram.queue(self.files[currFile].dequeue(), currFile)
                self.seqsSizes[currFile] -= 1
                currFile = (currFile + 1) % len(self.files)

                iter += 1 #DEBUG ###################
                if iter == 1000:
                    raise Exception("Loop infinito, 2º while")

            record = self.ram.dequeue() #Retira o menor registro da memória principal (vem em forma de dicionário, com o valor e o arquivo de origem)
            self.targetFile.appendElement(record["value"]) #Adiciona o registro ao arquivo alvo
            currFile = record["file"] #Atualiza o arquivo atual para o arquivo de origem do registro removido, pois vamos puxar o próximo registro dele

            iter += 1  #DEBUG ####################
            if iter == 1000:
                raise Exception("Loop infinito, 1º while")

        self.targetFile.closeSeq() #Fecha a sequência resultado e encerra a intercalação atual

    @property
    def done(self)->bool:
        return all([length == 0 for length in self.seqsSizes]) and self._heap.isEmpty


    @property
    def seqsSizes(self)->list:
        return self._seqsSizes

    @property
    def remaining(self)->int: #Número de registros restantes para serem lidos
        return sum(self._seqsSizes)

    @property
    def files(self)->list:
        return self._files
    
    @property
    def targetFile(self)->ArquivoCascata:
        return self._targetFile
    
    @property
    def ram(self)->HeapCascata:
        return self._heap
    
    @files.setter
    def files(self, files: list)->None:
        self._files = files
    
    @targetFile.setter
    def targetFile(self, targetFile: ArquivoCascata)->None:
        self._targetFile = targetFile

    @ram.setter
    def ram(self, ram: HeapCascata)->None:
        self._heap = ram
        