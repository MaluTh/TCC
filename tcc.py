# -*- coding: utf-8 -*-
from errbot import BotPlugin, botcmd
from pandas import read_csv
from pandas import concat
from pybrain3.tools.shortcuts import buildNetwork
from pybrain3.datasets import SupervisedDataSet
from pybrain3.supervised.trainers import BackpropTrainer
from pybrain3.tools.neuralnets import NNclassifier
from ImportData import ImportData
import numpy
import time
import datetime


class TCC(BotPlugin):
    """TCC da Maria Luiza"""

    # função para treinar a rede neural
    def treinar(self):
        self.warn_admins('Treinando a rede...')
        dataset = read_csv('data/plugins/MaluTh/tcc/saida.csv')

        values = dataset.values

        entradas = values[:, 3:9]

        saida = values[:, 9:10]

        tamanho = len(entradas)

        ds = SupervisedDataSet(6, 1)

        self.nn = buildNetwork(6, 6, 1, bias=True)

        for n, s in zip(entradas, saida):
            ds.addSample(n, s)

        trainer = BackpropTrainer(self.nn, ds, learningrate=0.4, momentum=0.3)

        for i in range(0, 1000):
            n = trainer.train()
            self.warn_admins(str(n))

    # função para coletar novos dados e ser testados pela rede neural
    @botcmd(split_args_with=None)
    def novos_dados(self):
        falso_positivo_alto = 0
        falso_positivo_medio = 0
        falso_positivo_baixo = 0
        
        gera_novo_dado = ImportData()

        newdata = read_csv('data/plugins/MaluTh/tcc/nova_saida.csv')
        #newdata = read_csv('data/plugins/MaluTh/tcc/saida.csv')
        total = len(newdata)
        values = newdata.values

        nova_entrada = values[:, :]

        e1 = values[:, 3:4]
        e2 = values[:, 4:5]
        e3 = values[:, 5:6]
        e4 = values[:, 6:7]
        e5 = values[:, 7:8]
        e6 = values[:, 8:9]

        for e1, e2, e3, e4, e5, e6 in zip(e1, e2, e3, e4, e5, e6):
            
            z = self.nn.activate((e1, e2, e3, e4, e5, e6))
            if z > 0.5:
                if (e1 < 0.5) and (e2 < 0.5) and (e3 < 0.5) and (e4 < 0.5) and (e5 < 0.5) and (e6 < 0.5):
                    falso_positivo_alto = falso_positivo_alto + 1
            elif z < 0.5 or z > 0.1:
                if (e1 > 0.5) and (e2 > 0.5) and (e3 > 0.5) and (e4 > 0.5) and (e5 > 0.5) and (e6 > 0.5):
                    falso_positivo_medio = falso_positivo_medio + 1
                elif (e1 < 0.1) and (e2 < 0.1) and (e3 < 0.1) and (e4 < 0.1) and (e5 < 0.1) and (e6 < 0.1):
                    falso_positivo_medio = falso_positivo_medio + 1
                else:
                    pass
            else: 
                if (e1 > 0.1) and (e2 > 0.1) and (e3 > 0.1) and (e4 > 0.1) and (e5 > 0.1) and (e6 > 0.1):
                    falso_positivo_baixo = falso_positivo_baixo + 1
            
            if z > 0.5:
                self.warn_admins('O consumo de recursos está alto em:')

                nova_info = [e1, e2, e3, e4, e5, e6]

                for linha in nova_entrada:
                    if (nova_info[0] == linha[3]) and (nova_info[1] == linha[4]) and (nova_info[2] == linha[5]) and (nova_info[3] == linha[6]) and (nova_info[4] == linha[7]) and (nova_info[5] == linha[8]):
                        data = datetime.date.fromtimestamp(linha[2])
                        datacerta = data.strftime("%d/%m/%Y")
                        nova_saida = 'POD: ' + str(linha[1]) + '\n' + 'Data: ' + str(datacerta) + '\n' + 'container_cpu_usage_seconds_total: ' + str(linha[3]) + '\n' + 'container_memory_usage_bytes: ' + str(linha[4]) + '\n' + 'container_fs_reads_bytes_total: ' + str(linha[5]) + '\n' + 'container_fs_writes_bytes_total: ' + str(linha[6]) + '\n' + 'container_network_receive_bytes_total: ' + str(linha[7]) + '\n' + 'container_network_transmit_bytes_total: ' + str(linha[8])
                        self.warn_admins(nova_saida)
                        break
        self.warn_admins('Falsos positivos: ' + str((falso_positivo_alto + falso_positivo_medio + falso_positivo_baixo)))
        erro = (falso_positivo_alto + falso_positivo_medio + falso_positivo_baixo)/total
        acerto = (1 - erro)*100
        self.warn_admins('Taxa de acerto: ' + str(acerto) + '%')

    # função que irá chamar as outras funções
    def activate(self):
        super().activate()
        self.nn = buildNetwork(6, 6, 1, bias=True)
        self.treinar()
        self.start_poller(1800, self.novos_dados)
