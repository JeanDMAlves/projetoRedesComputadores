import socket
import threading
import string
import random
import time

class Game(threading.Thread):
    def __init__(self, game_server, player_thread):
        threading.Thread.__init__(self)
        self.player_thread = player_thread
        self.server = game_server
        self.word_per_player = {}
        self.alphabet = list(string.ascii_lowercase)
        self.prefix = "<Jogo>"
        self.possibilities = ["Estado", "País", "Objeto"] # Dá pra colocar mais opções aqui
        self.rounds = 4 # Quantidade de rounds que o jogo terá
        self.wait_time = 5
        
    def run(self):
        "Falta implementar a lógica do jogo"
        self.send_all_players(f"{self.prefix}: Jogo está sendo iniciado... boa sorte")
        count_rounds = 0
        while count_rounds < self.rounds:
            letter = self.alphabet[random.randint(0, len(self.alphabet) - 1)] # Escolhendo uma letra aleatória
            possibility =  self.possibilities[random.randint(0, len(self.possibilities) -1 )] # Escolhendo uma 'possibilidade aleatória'
            full_text = f"Digite um(a) {possibility} com a letra {letter}"
            self.send_all_players(full_text)
            time.sleep(self.wait_time)
            count_rounds += 1
        
        self.player_thread.game = None
    
    def send_all_players(self, text):
        with self.server.lock:
            for player in self.server.players:
                player.sendall(text.encode("utf-8"))
        
        