#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - ticker_pool.py
Grupo: 44
Números de aluno: 58654, 58626 
"""

# Zona para fazer importação
import socket_utils 
import sys
import time

###############################################################################



class resource:
    def __init__(self, resource_id, resource_client_list, resource_time_limit):
        self.resource_id = resource_id

        # dicionario cuja chave é o id do recurso e o valor é a lista de clientes que subscreveram
        self.resource_client_list = resource_client_list

        # dicionario cuja chave é o par (id do recurso, id do cliente) e o valor é o tempo limite
        self.resource_time_limit = resource_time_limit

    def subscribe(self, client_id, time_limit):
        # se o cliente não subscreveu o recurso, adiciona o cliente à lista de clientes que subscreveram o recurso
        if client_id not in self.resource_client_list[self.resource_id]:
            self.resource_client_list[self.resource_id].append(client_id)

        # se o cliente já subscreveu o recurso, atualiza o tempo limite
        # se o cliente não subscreveu o recurso, adiciona o par (id do recurso, id do cliente) ao dicionario
        self.resource_time_limit[(self.resource_id, client_id)] =time_limit + time.time()
        
    def unsubscribe(self, client_id):
        # remove o cliente da lista de clientes que subscreveram o recurso
        self.resource_client_list[self.resource_id].remove(client_id)

        # remove o par (id do recurso, id do cliente) do dicionario
        for key in self.resource_time_limit.copy().keys():
            if key[0] == self.resource_id and key[1] == client_id:
                del self.resource_time_limit[key]

    def status(self, client_id):
        if client_id in self.resource_client_list[self.resource_id]:
            return "SUBSCRIBED"
        else:
            return "UNSUBSCRIBED"

    def __repr__(self):
        output = ""
        output += "R " + str(self.resource_id) + " " + \
            str(len(self.resource_client_list[self.resource_id])) + " "

        # Acrescentar no output a lista de clientes que subscreveram o recurso
        for client in self.resource_client_list[self.resource_id]:
            output += str(client) + " "

        # R <resource_id> <number of clients subscribed> <list of subscribers>
        return output

###############################################################################

class resource_pool:
    def __init__(self, N, K, M,resource_object, resource_client_list, resource_time_limit):
        # N - numero max de subscritores por recurso
        self.N = N
        # K - numero max de recursos por cliente
        self.K = K
        # M - numero max de recursos
        self.M = M

        self.resource_client_list = resource_client_list
        self.resource_time_limit = resource_time_limit

        # dicionario cuja chave é o id do recurso e o valor é o objeto resource
        self.resource_object = resource_object

        #criar recursos e adicionar ao dicionario resource_object
        #recursos vao de 0 a M-1
        for i in range(0, M):
            self.resource_object[i] = resource(i)   

        #criar listas de clientes vazias para o numero de recursos M e colocar no dicionario resource_client_list
        for i in range(0, M):
            self.resource_client_list[i] = []

    def clear_expired_subs(self):
        # usar unsubscribe da classe resource para remover os clientes que expiraram
        time_limit = int(time.time())
        #print (time_limit)
        #print (resource_time_limit[(resource_id, client_id)])
        # percorrer o dicionario resource_time_limit e dar unsubscribe nos clientes que expiraram
        if len(self.resource_time_limit) > 0: 
            for resource_id, client_id in self.resource_time_limit.copy().keys():
                if time_limit > self.resource_time_limit[(resource_id, client_id)]:
                    self.resource_object[resource_id].unsubscribe(client_id)

    def subscribe(self, resource_id, client_id, time_limit):
        return self.resource_object[resource_id].subscribe(client_id, time_limit)

    def unsubscribe(self, resource_id, client_id):
        return self.resource_object[resource_id].unsubscribe(client_id)

    def status(self, resource_id, client_id):
        return self.resource_object[resource_id].status(client_id)

    def infos(self, option, client_id):
        #lista de recursos a que o cliente subscreveu
        lista_subscritos = []
        for resource_id in self.resource_client_list.keys():
            if client_id in self.resource_client_list[resource_id]:
                lista_subscritos.append(resource_id)
        if option == "M":
            return lista_subscritos
        elif option == "K":
            return self.K - len(lista_subscritos)

    def statis(self, option, resource_id = None):
        if option == "L":
            return len(self.resource_client_list[resource_id])
        elif option == "ALL":
            return repr(self)
        
    def __repr__(self):
        output = ""
        for resource_id in self.resource_object.keys():
            output += repr(self.resource_object[resource_id]) + "\n"
        return output
        

