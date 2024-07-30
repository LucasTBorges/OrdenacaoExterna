from CascataPackage.SequenciaCascata import SequenciaCascata

class DistribuidorCascata:
    def __init__(self, input:list[list[int]], qtdFiles:int)->None: #Recebe lista de listas ordenadas de inteiros, mas armazena como objeto Sequência Ordenada
        self._input:list[SequenciaCascata] = [SequenciaCascata(seq) for seq in input]
        if(qtdFiles<2):
            raise ValueError("Quantidade de arquivos deve ser maior ou igual a 2")
        self._files:list[int] = [0]*(qtdFiles-1) + [1] #Lista de inteiros que representa a quantidade de sequências em cada arquivo
        self._frozenFiles:list[bool] = [True]*qtdFiles #Lista de booleanos que indica se o arquivo daquele índice em self._files está congelado
        self._steps:list[list[int]] = [list(self._files)] #Lista de cada passo da simulação da cascata
    
    def calcDistribution(self)->list[int]: #Calcula a distribuição ideal de sequências entre os arquivos
        if(self.qtdSeq < 2): #Se houver apenas uma sequência ordenada, já temos todos os registros ordenados
            return self._files
        self.firstCascade()
        while sum(self._files) < self.qtdSeq:
            self.reverseCascade()
            self._steps.append(list(self._files))
        return self._files
    

    def stringSteps(self)->str: #Retorna uma string com os passos da simulação da cascata
        qtdSteps:int = len(self._steps)
        stringSteps:str = ""
        for i in range(qtdSteps-1,-1,-1):
            stringSteps += f"Fase {qtdSteps-i-1}: {DistribuidorCascata.stringStep(self._steps[i])}\n"
        return stringSteps

    def reverseCascade(self)->None: #Realiza um passo da simulação da cascata reversa
        sequences: int
        self._frozenFiles = [x!=0 for x in self._files] #Congela todos os arquivos não vazios
        while self.someFrozen():
            sequences  = 0
            minFileIndex: int = self.minFile()
            unfrozenFiles: list[int] = self.unfrozenFiles()
            if len(unfrozenFiles)!=0:
                sequences, self._files[minFileIndex] = self._files[minFileIndex], sequences #Esvazia o arquivo congelado com o menor número de sequências e guarda o número de sequências em sequences
                for i in self.unfrozenFiles():#Distribui o número de sequências do arquivo selecionado para os outros arquivos
                    self._files[i] += sequences
            self._frozenFiles[minFileIndex] = False #Descongela o arquivo selecionado

    def firstCascade(self)->None: #Realiza o primeiro passo da simulação da cascata, especial pois todos menos um arquivo está vazio
        #Distribui as sequências do arquivo não vazio para os outros arquivos
        for i in range(self.qtdFiles):
            value: int = self._files[i]
            if value == 0:
                self._files[i] = 1
            else:
                self._files[i] = 0



    def unfrozenFiles(self)->list[int]: #Retorna uma lista com os índices dos arquivos que não estão congelados
        return [i for i in range(self.qtdFiles) if not self._frozenFiles[i]]
    
    def someFrozen(self)->bool: #Retorna True se algum arquivo não vazio estiver congelado
        for i in range(self.qtdFiles):
            if self._frozenFiles[i]:
                return True
        return False

    def minFile(self)->int: #Retorna o índice do arquivo não vazio congelado com o menor número de sequências
        min:int|None = None
        for i in range(self.qtdFiles):
            if self._frozenFiles[i]:
                if min is None or self._files[i] <= self._files[min]:
                    min = i
        return min
    
    @staticmethod
    def stringStep(files:list[int])->str:
        totalSequences:int = sum(files)
        return "{" + " ".join([DistribuidorCascata.stringFile(file) for file in files]) + "}" + f" ({totalSequences} sequência{"s" if totalSequences != 1 else ''})"
    
    @staticmethod
    def stringFile(int)->str:
        if int == 0:
            return "-"
        return str(int)

    @property
    def qtdSeq(self)->int:#Número de sequências ordenadas do input
        return len(self._input)
    
    @property
    def qtdFiles(self)->int:
        return len(self._files)
    
    @property
    def steps(self)->list[list[int]]:
        return list(self._steps)


        

    
        