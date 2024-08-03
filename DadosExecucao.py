import json

class DadosExecucao:
    def __init__(self, ramSize:int, qtdArquivos:int, seqsInic:list[list[int]])->None:
        self._ramSize:int = ramSize
        self._qtdArquivos = qtdArquivos
        self._inputSize:int = sum([len(seq) for seq in seqsInic])
        self._betas:list[float] = []
        self._seqsInic = list(seqsInic) #Sequências iniciais
        self._nSeqsInic:int = len(seqsInic) #Número de sequências iniciais
        self._alpha:float #Fator alfa, definido ao fim da ordenação

    @property
    def inputSize(self)->int:
        return self._inputSize
    
    @property
    def ramSize(self)->int:
        return self._ramSize
    
    @property
    def qtdArquivos(self)->int:
        return self._qtdArquivos
    
    @property
    def betas(self)->list[float]:
        return self._betas
    
    @property
    def nSeqsInic(self)->int:
        return self._nSeqsInic
    
    @property
    def alpha(self)->float:
        return self._alpha

    @property
    def seqsInic(self)->list[list[int]]
        return self._seqsInic
    
    @alpha.setter
    def alpha(self, alpha:float)->None:
        self._alpha = alpha

    def to_dict(self):
        return {
            "inputSize": self.inputSize,
            "ramSize": self._ramSize,
            "qtdArquivos": self._qtdArquivos,
            "betas": self._betas,
            "seqsInic": self._seqsInic,
            "nSeqsInic": self._nSeqsInic,
            "alpha": self._alpha
        }

    def save_to_json(self, filename):
        data = []
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            pass
        
        data.append(self.to_dict())
        
        with open(filename, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def from_dict(dict)-> 'DadosExecucao':
        dados = DadosExecucao(dict["ramSize"], dict["qtdArquivos"], dict["seqsInic"])
        dados._betas = dict["betas"]
        dados._alpha = dict["alpha"]
        return dados
    
    @staticmethod
    def load_from_json(filename)-> list['DadosExecucao']:
        with open(filename, 'r') as f:
            data = json.load(f)
            dados_list = []
            for item in data:
                dados = DadosExecucao.from_dict(item)
                dados_list.append(dados)
            return dados_list

    def __str__(self)->str:
        return f"inputSize: {self.inputSize}, ramSize: {self.ramSize}, betas: {self.betas}, nSeqsInic: {self.nSeqsInic}, alpha: {self.alpha}"
