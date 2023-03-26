# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 2 - net_client.py
Grupo: 44
Números de aluno: 58654, 58626 
"""

#zona para fazer imports
import net_client as nc
import time


class ListStub:
    def __init__(self, address, port,id):
        self.address = address
        self.port = port
        self.client_id = id
        self.conn_sock = None

        #criar lista de argumentos a enviar
        self.args_send = []

        #criar objeto net_client
        self.net_client = nc.server_connection(self.address, self.port)
        
    def connect(self):
        # código para estabelecer uma ligação ao servidor
        # i.e., tornando self.conn_sock válida
        self.conn_sock = self.net_client.connect()
        return self.conn_sock

    def disconnect(self):
    # Fecha a ligação conn_sock
        self.conn_sock.close()
    
    def send_receive(self):
        # Envia a lista para o servidor
        return self.net_client.send_receive(self.args_send)

    def process_command(self, command):
        # Processa o comando enviado pelo cliente
        #condiçoes para cada comando 
        #transforma comando em lista pronto a ser enviado para o servidor
         # Check if command is valid
        if command[0] not in ['SUBSCR', 'CANCEL', 'STATUS', 'INFOS', 'STATIS', 'STATIS ALL', 'SLEEP', 'EXIT']:
            return "UNKNOWN-COMMAND"
        
        if command[0] == 'SUBSCR':
            if len(command) < 3:
                return "MISSING-ARGUMENTS"
            try:
                timeout = int(command [2])
                command[2] = str(timeout + int(time.time()))
            except ValueError:
                return "INVALID-ARGUMENTS"
            
            self.args_send = [10,int(command[1]),int(command[2]),self.client_id]

        #argumentos a menos
        if command[0] in ['CANCEL', 'STATUS', 'INFOS',"STATIS"] and len(command) < 2:
            return "MISSING-ARGUMENTS"
                
        #argumentos a mais
        if command[0] in ['CANCEL', 'STATUS', 'INFOS'] and len(command) > 2:
            return "INVALID-ARGUMENTS"
        
        #argumentos a menos
        if command[0] == 'STATIS' and command[1]=="L" and len (command) < 3:
            return "MISSING-ARGUMENTS"

        #argumentos a mais
        if command[0] == 'STATIS' and command[1] == "L" and len (command) > 3:
            return "INVALID-ARGUMENTS"
        
        #argumentos a mais
        if command[0] == 'STATIS' and command[1] == "ALL" and len (command) > 2:
            return "INVALID-ARGUMENTS"
        
        #colocar ifs para cada comando e construir a lista a enviar
        if command[0] == "CANCEL":
            self.args_send = [20, int(command[1]), self.client_id]

        if command[0] == "STATUS":
            self.args_send = [30, int(command[1]), self.client_id]

        if command[0] == "INFOS":
            if command[1] == "M":
                self.args_send = [40, self.client_id]
            elif command[1] == "K":
                self.args_send = [50, self.client_id]
        
        if command[0] == "STATIS":
            if command[1] == "L":
                self.args_send = [60, int(command[2])]
            elif command[1] == "ALL":
                self.args_send = [70]
                
        if command[0] == "SLEEP":
            time.sleep(int(command[1]))
