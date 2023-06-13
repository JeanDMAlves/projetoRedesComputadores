import socket
import threading
import random
from player import Player
from game import Game
class GameServer(threading.Thread):
    """
        Classe responsável por iniciar o servidor de 1 jogo, 
        esperar por conexões de "jogadores" e 
        criar 1 thread por jogador através da classe 'PlayerThread', 
        salvando os jogadores presentes nessa instância de servidor no atributo players 
    """
    def __init__(self):
        threading.Thread.__init__(self)
        self.HOST = 'localhost'
        self.PORT = random.randint(9000, 10000)
        self.players = {}
        self.lock = threading.Lock() # Objeto de "tranca" -> Concorrência
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Usando TCP
        self.game = None
        print(f'Jogo iniciado em {self.HOST}:{self.PORT}')
    
    def run(self):
        self.server.bind((self.HOST, self.PORT))
        self.server.listen()
        while True:
            conn, addr = self.server.accept()
            thread = PlayerThread(conn, addr, self)
            thread.start()

class PlayerThread(threading.Thread):
    """
        Classe responsável por lidar com as threads de cada player
        Cada player estará associado a um jogo, podem haver diversos players em um único jogo 
    """
    def __init__(self, conn, addr, game_server):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.game_server = game_server
        
    def run(self):
        with self.game_server.lock:
            self.game_server.players[self.conn] = Player(self.conn)
        
        print(f'Conectado a {self.addr}')

        while True:
            data = self.conn.recv(1024).decode('utf-8')
            actual_player = self.game_server.players[self.conn]
            if not data: break
            
            elif data[0:3] == "-n ": # Prefixo que indica que a mensagem é para colocar um novo nome
                name = data[3:]
                actual_player.setName(name)
            
            elif data[0:3] == "-m ": # Prefixo que indica que a mensagem é para enviar uma mensagem aos novos jogadores
                send = f'<{actual_player.getName()}>: {data[3:]}'
                print(send)
                with self.game_server.lock:
                    for player in self.game_server.players:
                        if not (player == self.conn): # Mando para todos os usuários, exceto o próprio usuário que enviou a mensagem                    
                            player.sendall(send.encode('utf-8'))
                            
            elif data [0:3] == "-s": # prefiro que indica que a mensagem está para iniciar o jogo
                if self.game_server.game == None:  
                    self.game_server.game = Game(self.game_server)
                    self.game_server.game.start()
                else:
                    self.conn.sendall("Jogo já está rolando...".encode("utf-8"))
            
            else:        
                if self.game_server.game != None:
                    self.game_server.game.word_per_player[actual_player] = data

        with self.game_server.lock:
            self.game_server.players.remove(self.conn)
            
        self.conn.close()
        print('Disconnected:', self.addr)
        
if __name__ == "__main__":
    game_thread = GameServer()
    game_thread.start()