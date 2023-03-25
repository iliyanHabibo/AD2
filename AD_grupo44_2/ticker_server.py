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



#criar um objeto resource pool
recursos_objeto = ticker_pool.resource_pool(N,K,M)

#criar um objeto skeleton
skeleton_object = ticker_skel.ListSkeleton(recursos_objeto,M,K,N)

#criar socket TCP
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

listen_socket.bind(('127.0.0.1', 8080))

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
            data = sckt.recv(1024)
            if data:
                skeleton_object.clean_expired_subs()
                resposta = skeleton_object.processMessage(data)
                sckt.sendall(pickle.dumps(resposta))
            else:
                # fechar o socket se nao receber dados
                sckt.close()
                socket_list.remove(sckt)
                print("Cliente desconectado")



