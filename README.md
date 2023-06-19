# Servidor de Jogo

Este código em Python configura um servidor de jogo que permite que vários jogadores se conectem e joguem. Ele utiliza sockets para comunicação em rede e multithreading para lidar com várias conexões de jogadores simultaneamente.
Nomes: Jean Alves, Maria Julia Acosta, Felipe Robaina

## Pré-requisitos

- Python 3.x

## Utilização

1. Execute o script executando o seguinte comando:

   ```shell
   python game_server.py
   ```

2. O servidor será iniciado em uma porta aleatória entre 9000 e 10000 em `localhost`.

3. Os jogadores podem se conectar ao servidor usando um cliente TCP, como Telnet ou um script de cliente personalizado.

4. O servidor lida com várias conexões de jogadores simultaneamente, criando uma thread separada para cada jogador.

## Classes

### GameServer

- Responsável por iniciar o servidor de jogo, aguardar conexões de jogadores e criar uma thread separada para cada jogador.
- Os jogadores conectados a esta instância do servidor são armazenados no atributo `players`.

### PlayerThread

- Manipula as threads individuais para cada jogador.
- Cada jogador está associado a um jogo, e vários jogadores podem participar de um único jogo.

### Game

- Executa o jogo, rodando como uma thread separada.
- Gerencia a mecânica do jogo, como rodadas, atribuição de palavras, pontos e conclusão do jogo.
- Interage diretamente com os jogadores por meio do servidor.

### ReceiveThread

- Classe de thread usada para receber e imprimir mensagens do servidor.

### PlayerClient

- Classe de thread responsável por enviar mensagens para o servidor.
- Também inicia a classe `ReceiveThread` para receber mensagens do servidor.

### Player

- Representa um jogador, armazenando sua conexão, nome e pontos no jogo.

## Protocolo de Comunicação

A comunicação entre o servidor e os jogadores segue um protocolo simples baseado em texto. As mensagens trocadas entre o servidor e os jogadores usam prefixos específicos para indicar o objetivo da mensagem.

- `-n`: Atribui um novo nome à conexão do jogador.
- `-m`: Envia uma mensagem do jogador para todos os outros jogadores.
- `-s`: Inicia o jogo.
- Sem prefixo: Durante o jogo, mensagens sem prefixo são tratadas como palavras do jogo a serem processadas.

## Como o Jogo Funciona

1. O servidor de jogo é inicializado e aguarda conexões de jogadores.

2. Os jogadores se conectam ao servidor usando um cliente TCP (PlayerClient).

3. Assim que o número desejado de jogadores estiver conectado, um dos jogadores pode enviar o comando `-s` para iniciar o jogo.

4. O servidor de jogo inicia uma nova thread para lidar com o jogo.

5. O servidor de jogo seleciona aleatoriamente uma letra do alfabeto e uma opção das possibilidades disponíveis (por exemplo: "Estado", "País", "Objeto").

6. O servidor de jogo envia uma mensagem para todos os jogadores, solicitando que eles forneçam uma palavra que corresponda à letra e à opção escolhidas dentro de um limite de tempo especificado.

7. Os jogadores enviam suas palavras para o servidor de jogo.

8. O servidor de jogo atribui pontos aos jogadores com base no tamanho das palavras que eles enviaram.

9. Os passos 5 a 8 são repetidos para um número específico de rodadas.

10. Após o número de rodadas especificado, o servidor de jogo exibe a pontuação final de cada jogador.

11. Os pontos são redefinidos e o jogo é encerrado. Os jogadores podem iniciar um novo jogo enviando o comando `-s`.

## Cliente

Um cliente pro jogador é fornecido para conectar ao servidor do jogo e participar das partidas.

### Utilização do cliente

1. Rode o cliente utilizando o seguinte comando:

    ```Shell
    python player_client.py <PORTA>
    ``` Troque `<PORTA>` pela porta em que o servidor está rodando

2. O cliente vai se conectar ao servidor do jogo em `localhost` na porta especificada.

3. Digite o nome ou apelido quando solicitado
4. Para mandar mensagens durante o jogo, simplesmente digite e então pressione Enter. Use o prefixo `-m` para mandar mensagens aos outros jogadores
5. Para sair do jogo digite `quit`
