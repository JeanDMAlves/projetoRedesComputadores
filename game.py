import socket
import threading
import string
import random
import time

class Game(threading.Thread):
    """
        Classe responsável por efetivamente executar o jogo
        é uma thread separada que rodará o pseudo-stop, interagindo diretamente com os jogadores
        também atribuindo pontos e mostrando, ao final, os pontos que cada jogador fez  
    """
    
    def __init__(self, game_server):
        threading.Thread.__init__(self)
        self.server = game_server
        self.word_per_player = {}
        self.alphabet = list(string.ascii_lowercase)
        self.prefix = "<Jogo>"
        self.possibilities = ["Estado", "País", "Objeto"] # Opções de "assuntos" pro pseudo-stop
        self.rounds = 4 # Quantidade de rounds que o jogo terá
        self.wait_time = 5 # tempo de espera para os jogadores digitarem suas respostas
        
    def run(self):
        """
            Método responsável por iniciar a thread, escolher aleatoriamente uma letra do alfabeto
            e uma opção de 'assunto', mandará para os jogadores essas escolhas, esperará 'self.wait_time'
            segundos para os jogadores digitarem suas palavras, adicionará para os jogadores seus respectivos pontos,
            isso continuará por 'self.rounds' rounds, após sair do loop será mostrado os pontos de cada jogador,
            os pontos serão resetados e o jogo "acabará" 
        """
        self.send_to_all_players(f"{self.prefix}: Jogo está sendo iniciado... boa sorte")
        count_rounds = 0
        while count_rounds < self.rounds:
            letter = self.alphabet[random.randint(0, len(self.alphabet) - 1)] # Escolhendo uma letra aleatória
            possibility =  self.possibilities[random.randint(0, len(self.possibilities) -1 )] # Escolhendo uma 'possibilidade aleatória'
            full_text = f"{self.prefix} Digite um(a) {possibility} com a letra {letter}"
            self.send_to_all_players(full_text)
            time.sleep(self.wait_time)
            self.assign_points_to_players(letter) # Verifica as palavras escritas pelos jogadores
            count_rounds += 1
        self.show_placement()
        self.reset_points_of_players() # No fim do jogo, reseta os pontos dos jogadores
        self.server.game = None
        self.send_to_all_players("------Jogo terminado------")
        
    def send_to_all_players(self, text):
        # Método para enviar algum texto para todos os jogadores
        with self.server.lock:
            for player in self.server.players:
                player.sendall(text.encode("utf-8"))
    
    def assign_points_to_players(self, letter):
        # Método para checar as palavras que os jogadores digitaram
        # se for válida vai adicionamos os pontos para os jogadores
        # os pontos são computados de acordo com o tamanho da palavra
        for player in self.word_per_player:
            word = self.word_per_player[player]
            if word[0] == letter:
                word_length = len(word)
                player.points += word_length
                
    def reset_points_of_players(self):
        # Método para resetar os pontos dos jogadores no final do jogo
        for player in self.server.players.values():
            player.points = 0
    
    def show_placement(self):
        # Mostra para os jogadores quantos pontos cada um fez nesse jogo
        send = ""
        for player in self.server.players.values():
            send += f"*<{player.getName()} fez {player.points} pontos>*\n"
        self.send_to_all_players(send)
        