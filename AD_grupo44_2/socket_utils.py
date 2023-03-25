#zona para imports
import sys
import socket as s
import struct

#zona para classes

def create_tcp_server_socket(address, port, queue_size):
    """
    Função que cria um socket TCP e estabelece a ligação ao servidor especificado
    nos parâmetros.

    Parâmetros:
    address - endereço IP do servidor
    port - número de porta do servidor
    queue_size - tamanho máximo da fila de conexões pendentes

    Retorna:
    socket - socket TCP ligado ao servidor

    Excepções:
    socket.error - se ocorrer algum erro na criação do socket ou na ligação
    """

    HOST = address
    PORT = int(port)

    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(queue_size)

    conn, addr = sock.accept()  # accept incoming connection

    return conn, addr

def create_tcp_client_socket(address, port):
    """
    Função que cria um socket TCP e estabelece a ligação ao servidor especificado
    nos parâmetros.

    Parâmetros:
    address - endereço IP do servidor
    port - número de porta do servidor

    Retorna:
    socket - socket TCP ligado ao servidor

    Excepções:
    socket.error - se ocorrer algum erro na criação do socket ou na ligação
    """

    HOST = address
    PORT = int(port)

    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect((HOST, PORT))

    return sock

def receive_all(socket, length):
    """
    Função que recebe uma quantidade de dados específica de uma socket.

    Parâmetros:
    socket - socket TCP ligada ao servidor
    length - quantidade de dados a receber

    Retorna:
    data - dados recebidos

    Excepções:
    socket.error - se ocorrer algum erro na recepção dos dados
    """
    data = b''
    remaining = length
    while remaining > 0:
        chunk = socket.recv(remaining)
        if not chunk:
            raise socket.error("Socket closed before receiving all data")
        data += chunk
        remaining -= len(chunk)
  
    # Unpack the received data using the appropriate format string
    fmt = f"{length}s"
    unpacked_data = struct.unpack(fmt, data)
    return unpacked_data[0].decode()
