import socket
import threading 
import sys

class ReceiveThread(threading.Thread):
    """
        Classe (thread) usada para receber e "printar" mensagens vindas do servidor
    """
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn
        
    def run(self):
        while True:
            data = self.conn.recv(1024).decode('utf-8')
            if not data:
                break
            print(data)
            
class PlayerClient(threading.Thread):
    """
        Classe responsável mandar mensagens para o servidor,
        também inicia a classe ReceiveThread (receber mensagens do servidor)
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.HOST = 'localhost'
        self.PORT = int(sys.argv[1])
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        self.client.connect((self.HOST, self.PORT))
        print(f'Conectado ao servidor {self.HOST}:{self.PORT}')
    
    def run(self):
        message_thread = ReceiveThread(self.client)
        message_thread.start()
        self.setName()
        print('Digite uma mensagem (utilize -m para mandar mensagens para outros jogadores):')
        while True:
            message = input("")
            if message == 'quit':
                break
            self.client.sendall(message.encode('utf-8'))
        self.client.close()
    
    def setName(self):
        prefix = "-n "
        message = input("Digite seu nome/apelido: ")
        send = prefix + message
        self.client.sendall(send.encode('utf-8'))
      
class Player:
    def __init__(self, conn):
        self.conn = conn
        self.name = None
        self.points = 0
        
    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
      
if __name__ == "__main__":
    player_thread = PlayerClient()
    player_thread.start()