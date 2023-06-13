import socket
import threading
import string
import random
import time

class Game(threading.Thread):
    def __init__(self, game_server):
        threading.Thread.__init__(self)
        self.server = game_server
        self.word_per_player = {}
        self.alphabet = list(string.ascii_lowercase)
        self.prefix = "<Jogo>"
        self.possibilities = ["Estado", "País", "Objeto"] # Dá pra colocar mais opções aqui
        self.rounds = 4 # Quantidade de rounds que o jogo terá
        self.wait_time = 5 # tempo de espera para os jogadores digitarem suas respostas
        
    def run(self):
        self.send_to_all_players(f"{self.prefix}: Jogo está sendo iniciado... boa sorte")
        count_rounds = 0
        while count_rounds < self.rounds:
            letter = self.alphabet[random.randint(0, len(self.alphabet) - 1)] # Escolhendo uma letra aleatória
            possibility =  self.possibilities[random.randint(0, len(self.possibilities) -1 )] # Escolhendo uma 'possibilidade aleatória'
            full_text = f"Digite um(a) {possibility} com a letra {letter}"
            self.send_to_all_players(full_text)
            time.sleep(self.wait_time)
            self.assign_points_to_players(letter) # Verifica as palavras escritas pelos jogadores
            count_rounds += 1
        self.show_placement()
        self.reset_points_of_players() # No fim do jogo, reseta os pontos dos jogadores
        self.server.game = None
    
    def send_to_all_players(self, text):
        with self.server.lock:
            for player in self.server.players:
                player.sendall(text.encode("utf-8"))
    
    def assign_points_to_players(self, letter):
        for player in self.word_per_player:
            word = self.word_per_player[player]
            if word[0] == letter:
                word_length = len(word)
                player.points += word_length
                
    def reset_points_of_players(self):
        for player in self.server.players.values():
            player.points = 0
    
    def show_placement(self):
        send = ""
        for player in self.server.players.values():
            send += f"*<{player.getName()} fez {player.points} pontos>*"
        self.send_to_all_players(send)
        