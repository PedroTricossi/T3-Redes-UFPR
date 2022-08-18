from sqlalchemy import false, true
from termcolor import colored
from mensagem import Mensagem
import os

ENQUADRAMENTO = '01100111'
MSG_INICIO = 0
MSG_ORIGEM = 1
MSG_DESTINO = 2
MSG_RECEBIDA = 3
MSG_LIDA = 4
MSG_TIPO = 5
MSG_DADOS = 6
MSG_PARIDADE = 7

def calcula_paridade(data):
    patidadeRecv = 0

    strDados = str(data[MSG_DADOS])
    strDados = strDados.encode()

    for caracte in strDados:
        patidadeRecv ^= caracte
    
    if (patidadeRecv == data[MSG_PARIDADE]):
        return true
    
    return false


def ringNetwork(player):
    msg = Mensagem()
    data, address = player.sock.recvfrom(2048)

    data = data.decode('utf-8')
    data = eval(data)

    if (data[0] == ENQUADRAMENTO):
        msg.recebe_mensagem(data)
    
    if(calcula_paridade(data)):
        msg.le_mensagem(data)

    if(data[MSG_DESTINO][1] == player.jogador_addr[1] and data[MSG_RECEBIDA] == 1 and data[MSG_LIDA] == 1):
        if(player.retorna_bastao() == player.jogador_addr):
            if (data[MSG_TIPO] == 0):
                jogada = player.cria_jogada()
                msg.envia_mensagem(player, player.prox_addr, 0, 0, 1, jogada)

            elif (data[MSG_TIPO] == 1):
                if(data[MSG_DADOS][2][1] == player.jogador_addr[1]):
                    res = player.realiza_jogada(data)
                    resultado = [res, player.fichas, player.jogador_addr]
                    msg.envia_mensagem(player, msg.retorna_bastao(), 0, 0, 4, resultado)
                else:
                    msg.envia_mensagem(player, data[MSG_DADOS][2], 0, 0, 2, data[MSG_DADOS])
                    
            elif (data[MSG_TIPO] == 4):
                if(data[MSG_DADOS][1] <= 0):
                    print('entrou')
                    fim = [player.fichas, player.jogador_addr]
                    msg.envia_mensagem(player, player.prox_addr, 0, 0, 6, fim)
                else:
                    print('O jogador ' + colored(f'{data[MSG_DADOS][2]} ', 'yellow') + colored(f'{"ganhou" if data[MSG_DADOS][0] == 1 else "perdeu"}', 'cyan') + ' E agora tem' + colored(f' {data[MSG_DADOS][1]} ', 'red') + 'fichas')
                    msg.envia_mensagem(player, player.prox_addr, 0, 0, 5, data[MSG_DADOS])
            
            elif (data[MSG_TIPO] == 5):
                msg.envia_mensagem(player, player.prox_addr, 0, 0, 0, player.passa_bastao())
            
            elif (data[MSG_TIPO] == 6):
                os.system('clear')
                print(f'O ganhador é o jogador {data[MSG_DADOS][1]}')
            
            return
                

        if (data[MSG_TIPO] == 0):
            player.inicia_bastao(data[MSG_DADOS])
            
            msg.envia_mensagem(player, player.prox_addr, 0, 0, 0, data[MSG_DADOS])
            
        
        elif (data[MSG_TIPO] == 1):
            os.system('clear')

            player.propoe_aposta(data)
            msg.envia_mensagem(player, player.prox_addr, 0, 0, 1, data[MSG_DADOS])
            
            
        elif(data[MSG_TIPO] == 2):
            res = player.realiza_jogada(data)
            resultado = [res, player.fichas, player.jogador_addr]

            msg.envia_mensagem(player, player.retorna_bastao(), 0, 0, 4, resultado)
        
        elif (data[MSG_TIPO] == 5):
            print('O jogador ' + colored(f'{data[MSG_DADOS][2]} ', 'yellow') + colored(f'{"ganhou" if data[MSG_DADOS][0] == 1 else "perdeu"}', 'cyan') + ' E agora tem' + colored(f' {data[MSG_DADOS][1]} ', 'red') + 'fichas')
            msg.envia_mensagem(player, player.prox_addr, 0, 0, 5, data[MSG_DADOS])
        
        elif (data[MSG_TIPO] == 6):
            if (data[MSG_DADOS][0] < player.fichas):
                data[MSG_DADOS][0] = player.fichas
                data[MSG_DADOS][1] = player.jogador_addr
        
            msg.envia_mensagem(player, player.prox_addr, 0, 0, 6, data[MSG_DADOS])
    
    else:
        msg.envia_mensagem(player, data[MSG_DESTINO], data[MSG_RECEBIDA], data[MSG_LIDA], data[MSG_TIPO], data[MSG_DADOS])