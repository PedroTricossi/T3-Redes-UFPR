from ctypes.wintypes import MSG


ENQUADRAMENTO = '01100111'

class Mensagem:
    def __init__(self):
        self.bastao = 0

    # Destino -> quem ira receber a mensagem
    # Recebida -> diz se a mensagem foi recebida pelo destino (0 = não recebido pelo destino/ 1= recebido pelo destino) 
    # lida -> Diz se a mensagem passou pelo teste de paridade com sucesso (0 = caso não tenha tido sucesso / 1 = caso tenha tido sucesso)
    # tipo -> Diz o tipo da mensagem (0 = passagem de bastão, 1 = fase de aposta, 2 = executar jogada, 3 = fim da jogada atualiza valores)
    # dados -> dados da mensagem
    
    def envia_mensagem(self, player, destino, recebida, lida, tipo, dados):
        msg = []
        msg.append(ENQUADRAMENTO)
        msg.append(player.jogador_addr)
        msg.append(destino)
        msg.append(recebida)
        msg.append(lida)
        msg.append(tipo)
        msg.append(dados)

        paridade = 0
        
        dadosStr = str(dados)
        dadosStr = dadosStr.encode()

        for caracte in dadosStr:
            paridade ^= caracte
        
        msg.append(paridade)

        msg = str(msg)
        msg = msg.encode()

        player.sock.sendto(msg, player.prox_addr)

    def recebe_mensagem(self, mensagem):
        mensagem[3] = 1

    def le_mensagem(self, mensagem):
        mensagem[4] = 1

