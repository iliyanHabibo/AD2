# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - net_client.py
Grupo: 44
Números de aluno: 58654, 58626 
"""


# Zona para fazer imports
import sys
import ticker_stub as ts

ID= int(sys.argv[1])
HOST = sys.argv[2]
PORT = int(sys.argv[3])

stub = ts.ListStub(HOST, PORT, ID)
stub.connect()

while True:
    comando = input("comando >")
    args = comando.split()
    if args[0] == "EXIT":
        break
    comando_enviar = stub.process_command(args)
    if comando_enviar not in ("UNKNOWN-COMMAND", "MISSING-ARGUMENTS", "INVALID-ARGUMENTS"):
        resposta = stub.send_receive()
        print(resposta)

stub.disconnect()