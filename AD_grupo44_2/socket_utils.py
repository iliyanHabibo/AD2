#zona para imports
import sys
import socket as s
import struct
import pickle

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
    try:
        sock.connect((HOST, PORT))
    except Exception as e:
        print(f"Error connecting to server: {e}")
        sys.exit(1)

    return sock


def receive_all(socket, size):
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
    #recebe um int (o tamanho do int e de 4 bytes) com o tamanho da mensagem
    #depois recebe a mensagem usando o recv com o argumento size que é o tamanho da mensagem
    size_bytes = socket.recv(4)
    size = struct.unpack('i',size_bytes)[0]
    msg_bytes = socket.recv(size)
    msg = pickle.loads(msg_bytes)
  
    return msg
    

