#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_server.py
Grupo: 44
Números de aluno: 58654, 58626 
"""

# Zona para fazer importação
import sys
import time
import ticker_pool
import socketserver
import pickle

# dicionario cuja chave é o id do recurso e o valor é o objeto resource
resource_object = {}
# dicionario cuja chave é o id do recurso e o valor é a lista de clientes que subscreveram
resource_client_list = {}

# dicionario cuja chave é o par (id do recurso, id do cliente) e o valor é o tempo limite
resource_time_limit = {}

#funcao auxiliar que conta o numero de recursos a que o cliente subscreveu
def count_resources_client(client_id):
    count = 0
    for resource_id in resource_client_list.keys():
        if client_id in resource_client_list[resource_id]:
            count += 1
    return count

class ListSkeleton:
    def __init__(self,objeto_resource_pool,M,K,N):
        self.servicoLista = []
        self.objeto_resource_pool = objeto_resource_pool

        #numero maximo de recursos
        self.M = M
        #numero maximo de recursos por cliente
        self.K = K
        #numero maximo de subscritores por recurso
        self.N = N

    def processMessage(self, msg_bytes):
        pedido_lista = pickle.loads(msg_bytes)
        resposta = []
        if pedido_lista[0] == 10:
            if pedido_lista[1] not in self.objeto_resource_pool.resource_client_list.keys():
                resposta = [11,None]
            elif count_resources_client(pedido_lista[3]) > self.k:
                resposta = [11,False]
            elif len(self.resource_client_list[1])>self.N:
                resposta = [11,False]
            else:
                self.objeto_resource_pool.subscribe(pedido_lista[1],pedido_lista[3],pedido_lista[2])
                resposta = [11,True]

        elif pedido_lista[0] == 20:
            if pedido_lista[1] not in self.objeto_resource_pool.resource_client_list.keys():
                resposta = [21,None]
            elif pedido_lista[2] not in self.objeto_resource_pool.resource_client_list[pedido_lista[1]]:
                resposta = [21,False]
            else:
                self.objeto_resource_pool.unsubscribe(pedido_lista[1],pedido_lista[2])
                resposta = [21,True]
        
        elif pedido_lista[0] == 30:
            if pedido_lista[1] not in self.objeto_resource_pool.resource_client_list.keys():
                resposta = [31,None]
            elif pedido_lista[2] not in self.objeto_resource_pool.resource_client_list[pedido_lista[1]]:
                resposta = [31,"UNSUBSCRIBED"]
            else:
                resposta = [31,"SUBSCRIBED"]
        
        elif pedido_lista[0] == 40:
            resposta = [41, self.objeto_resource_pool.infos("M",pedido_lista[1])]
        
        elif pedido_lista[0] == 50:
            resposta = [51, self.objeto_resource_pool.infos("K",pedido_lista[1])]
        
        elif pedido_lista[0] == 60:
            if pedido_lista[1] not in self.objeto_resource_pool.resource_client_list.keys():
                resposta = [61,None]
            else:
                resposta = [61, self.objeto_resource_pool.statis("L",pedido_lista[1])]
        
        elif pedido_lista[0] == 70:
            resposta = [71, self.objeto_resource_pool.statis("ALL")]
        
        return pickle.dumps(resposta)
    
    def clean_expired_subs(self):
        self.objeto_resource_pool.clean_expired_subs()