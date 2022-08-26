from sqlalchemy import false, true
from termcolor import colored
from mensagem import Mensagem
import os

import constants

def calcula_paridade(data):
    patidadeRecv = 0

    strDados = str(data[constants.MSG_DADOS])
    strDados = strDados.encode()

    for caracte in strDados:
        patidadeRecv ^= caracte
    
    if (patidadeRecv == data[constants.MSG_PARIDADE]):
        return true
    
    return false


def ringNetwork(player):
    msg = Mensagem()
    data, address = player.sock.recvfrom(128)

    data = data.decode('utf-8')
    data = eval(data)

    if (data[0] == constants.ENQUADRAMENTO):
        msg.recebe_mensagem(data)
    
    if(calcula_paridade(data)):
        msg.le_mensagem(data)

    if(data[constants.MSG_DESTINO][1] == player.jogador_addr[1] and data[constants.MSG_RECEBIDA] == 1 and data[constants.MSG_LIDA] == 1):
        if(player.retorna_bastao() == player.jogador_addr):
            if (data[constants.MSG_TIPO] == constants.PASSAGEM_BASTAO):
                jogada = player.cria_jogada()
                msg.envia_mensagem(player, player.prox_addr, 0, 0, 1, jogada)

            elif (data[constants.MSG_TIPO] == constants.FAZ_APOSTA):
                if(data[constants.MSG_DADOS][2][1] == player.jogador_addr[1]):
                    res = player.realiza_jogada(data)
                    resultado = [res, player.fichas, player.jogador_addr]
                    msg.envia_mensagem(player, player.retorna_bastao(), 0, 0, constants.ENVIA_RESULTADOS, resultado)
                else:
                    msg.envia_mensagem(player, data[constants.MSG_DADOS][2], 0, 0, constants.FAZ_JOGADA, data[constants.MSG_DADOS])
                    
            elif (data[constants.MSG_TIPO] == constants.ENVIA_RESULTADOS):
                if(data[constants.MSG_DADOS][1] <= 0):
                    print("ENTROU")
                    fim = [player.fichas, player.jogador_addr]
                    msg.envia_mensagem(player, player.prox_addr, 0, 0, constants.VERIFICA_GANHADOR, fim)
                else:
                    print('O jogador ' + colored(f'{data[constants.MSG_DADOS][2]} ', 'yellow') + colored(f'{"ganhou" if data[constants.MSG_DADOS][0] == 1 else "perdeu"}', 'cyan') + ' E agora tem' + colored(f' {data[constants.MSG_DADOS][1]} ', 'red') + 'fichas')
                    msg.envia_mensagem(player, player.prox_addr, 0, 0, constants.ATUALIZA_FICHAS, data[constants.MSG_DADOS])
            
            elif (data[constants.MSG_TIPO] == constants.ATUALIZA_FICHAS):
                msg.envia_mensagem(player, player.prox_addr, 0, 0, constants.PASSAGEM_BASTAO, player.passa_bastao())
            
            elif (data[constants.MSG_TIPO] == constants.VERIFICA_GANHADOR):
                os.system('clear')
                print(f'O ganhador é o jogador {data[constants.MSG_DADOS][1]}')
                msg.envia_mensagem(player, player.prox_addr, 0, 0, constants.ANUNCIA_GANHADOR, data[constants.MSG_DADOS][1])
                exit(0)
            
            return
                

        if (data[constants.MSG_TIPO] == constants.PASSAGEM_BASTAO):
            player.inicia_bastao(data[constants.MSG_DADOS])
            
            msg.envia_mensagem(player, player.prox_addr, 0, 0, constants.PASSAGEM_BASTAO, data[constants.MSG_DADOS])
            
        
        elif (data[constants.MSG_TIPO] == constants.FAZ_APOSTA):
            os.system('clear')

            player.propoe_aposta(data)
            msg.envia_mensagem(player, player.prox_addr, 0, 0, constants.FAZ_APOSTA, data[constants.MSG_DADOS])
            
            
        elif(data[constants.MSG_TIPO] == constants.FAZ_JOGADA):
            res = player.realiza_jogada(data)
            resultado = [res, player.fichas, player.jogador_addr]

            msg.envia_mensagem(player, player.retorna_bastao(), 0, 0, constants.ENVIA_RESULTADOS, resultado)
        
        elif (data[constants.MSG_TIPO] == constants.ATUALIZA_FICHAS):
            print('O jogador ' + colored(f'{data[constants.MSG_DADOS][2]} ', 'yellow') + colored(f'{"ganhou" if data[constants.MSG_DADOS][0] == 1 else "perdeu"}', 'cyan') + ' E agora tem' + colored(f' {data[constants.MSG_DADOS][1]} ', 'red') + 'fichas')
            msg.envia_mensagem(player, player.prox_addr, 0, 0, constants.ATUALIZA_FICHAS, data[constants.MSG_DADOS])
        
        elif (data[constants.MSG_TIPO] == constants.VERIFICA_GANHADOR):
            if (data[constants.MSG_DADOS][0] < player.fichas):
                data[constants.MSG_DADOS][0] = player.fichas
                data[constants.MSG_DADOS][1] = player.jogador_addr
        
            msg.envia_mensagem(player, player.prox_addr, 0, 0, constants.VERIFICA_GANHADOR, data[constants.MSG_DADOS])

        elif (data[constants.MSG_TIPO] == constants.ANUNCIA_GANHADOR):
            os.system('clear')
            print(f'O ganhador é o jogador {data[constants.MSG_DADOS]}')
            msg.envia_mensagem(player, player.prox_addr, 0, 0, constants.ANUNCIA_GANHADOR, data[constants.MSG_DADOS])
            player.sock.close()
            exit(0)
    
    else:
        msg.envia_mensagem(player, data[constants.MSG_DESTINO], 0, 0, data[constants.MSG_TIPO], data[constants.MSG_DADOS])