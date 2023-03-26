#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_server.py
Grupo: 44
Números de aluno: 58654, 58626 
"""

#zona para imports
import sys
import ticker_skel
import ticker_pool
import socket
import select
import struct
import pickle

#zona para definir variaveis
HOST = sys.argv[1]
PORT = int(sys.argv[2])
#numero maximo de recursos
M = int(sys.argv[3])
#numero maximo de recursos por cliente
K = int(sys.argv[4])
#numero maximo de subscritores por recurso
N = int(sys.argv[5])

# dicionario cuja chave é o id do recurso e o valor é o objeto resource
resource_object = {}
# dicionario cuja chave é o id do recurso e o valor é a lista de clientes que subscreveram
resource_client_list = {}
# dicionario cuja chave é o par (id do recurso, id do cliente) e o valor é o tempo limite
resource_time_limit = {}



#criar um objeto resource pool
recursos_objeto = ticker_pool.resource_pool(M,K,N,resource_object,resource_client_list,resource_time_limit)

#criar um objeto skeleton
skeleton_object = ticker_skel.ListSkeleton(recursos_objeto,resource_client_list,resource_time_limit,M,K,N)

#criar socket TCP
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

listen_socket.bind((HOST, PORT))

#começa a escutar conexoes de clientes
listen_socket.listen()

socket_list = [listen_socket]

while True:
    # wait for sockets with activity
    R,W,X = select.select(socket_list, [], [])

    for sckt in R:
        if sckt is listen_socket:
            # handle incoming connection
            conn, addr = sckt.accept()
            socket_list.append(conn)
            print("Novo cliente com o endereço {}".format(addr))
        else:
            #tratar a mensagem recebida do cliente
            data_size = sckt.recv(4) 
            data_size = struct.unpack ('i',data_size)[0]
            msg_bytes = sckt.recv(data_size)
            msg = pickle.loads(msg_bytes)
            if msg:
                skeleton_object.clear_expired_subs()
                resposta = skeleton_object.processMessage(msg)
                resposta_bytes = pickle.dumps(resposta,-1)
                #mandar o tamanho da resposta ao cliente
                size_resposta_bytes = struct.pack('i', len(resposta_bytes))
                sckt.sendall(size_resposta_bytes)
                sckt.sendall(resposta_bytes)
            else:
                # fechar o socket se nao receber dados
                sckt.close()
                socket_list.remove(sckt)
                print("Cliente desconectado")




