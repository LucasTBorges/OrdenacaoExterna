class Record:
    def __init__(self, value:int, marked:bool = False):
        self._value = value
        self._marked = marked #indicador de se o registro foi marcado por ser menor que o último elemento adicionado à sequência ordenada durante a seleção natural

    def __str__(self):
        string:str = str(self._value)
        if self._marked:
            string += "*"
        return string
    
    def __repr__(self):
        return str(self)
    
    def __lt__(self, other: "Record") -> bool:#Registros marcados são considerados maiores que não marcados. Registros de igual marcação são comparados com base no valor.
        if not self._marked:
            return self._value < other.value
        if not other.marked:
            return False
        return self._value < other.value
        
    @property
    def value(self):
        return self._value
    
    @property
    def marked(self):
        return self._marked