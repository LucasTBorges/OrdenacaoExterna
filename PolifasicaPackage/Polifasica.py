from PolifasicaPackage.ArquivoPolifasica import ArquivoPolifasica

class Polifasica:
    def __init__(self, memSize: int, arquivos: list[ArquivoPolifasica]):
        self._arquivos = arquivos

    def __str__(self)->str:
        return str([arq.sequencias for arq in self._arquivos])

    @property
    def completo(self):
        arquivos = [arq for arq in self._arquivos if not arq.isEmpty]
        return len(arquivos) == 1 and len(arquivos[0].sequencias) == 1

    @property
    def arquivos(self)->list[ArquivoPolifasica]:
        return self._arquivos

    def ordenarSequencias(self, sequencias: list):
        new_ordered_list = []
        index = [0] * len(sequencias)

        while any(index[i] < len(sequencias[i]) for i in range(len(sequencias))):
            min_val = float('inf')
            min_idx = None

            for i in range(len(sequencias)):
                if index[i] < len(sequencias[i]) and sequencias[i][index[i]] < min_val:
                    min_val = sequencias[i][index[i]]
                    min_idx = i

            new_ordered_list.append(min_val)
            index[min_idx] += 1

        return new_ordered_list

        
    def polifasear(self):
        while not self.completo:
            target_file = None
            for file in self._arquivos:
                if file.isEmpty:
                    target_file = file
            if target_file is None:
                raise Exception("Tentativa de executar cascata falhou pois todos os arquivos estavam ocupados")

            arquivos = [arq for arq in self._arquivos if not arq.isEmpty and arq != target_file]
            while (all([not arq.isEmpty for arq in arquivos])):
                sequencias = [arq.sequencias[0] for arq in arquivos]
                sequencia_ordenada = self.ordenarSequencias(sequencias)
                target_file.appendSequencia(sequencia_ordenada)
                for arq in self._arquivos:
                    if arq != target_file and len(arq.sequencias) > 0:
                        arq.sequencias.pop(0)

                # arqs = [arq.sequencias for arq in arquivos]
                # print('arquivos: ' + str(arqs))
                # arqs = [arq.sequencias for arq in self._arquivos]
                # print('self._arquivos: ' + str(arqs))





    