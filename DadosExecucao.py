import json

class DadosExecucao:
    def __init__(self, inputSize:int, ramSize:int, nSeqsInic:int)->None:
        self._inputSize:int = inputSize
        self._ramSize:int = ramSize
        self._betas:list[float] = []
        self._nSeqsInic:int = nSeqsInic #Número de sequências iniciais
        self._alpha:int #Fator alfa, definido ao fim da ordenação

    @property
    def inputSize(self)->int:
        return self._inputSize
    
    @property
    def ramSize(self)->int:
        return self._ramSize
    
    @property
    def betas(self)->list[float]:
        return self._betas
    
    @property
    def nSeqsInic(self)->int:
        return self._nSeqsInic
    
    @property
    def alpha(self)->int:
        return self._alpha

    @alpha.setter
    def alpha(self, alpha:int)->None:
        self._alpha = alpha

    def to_dict(self):
        return {
            "inputSize": self.inputSize,
            "ramSize": self._ramSize,
            "betas": self._betas,
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
        dados = DadosExecucao(dict["inputSize"], dict["ramSize"], dict["nSeqsInic"])
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
