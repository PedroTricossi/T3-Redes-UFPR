from pickle import FALSE, TRUE
from random import randint
from termcolor import colored
import constants

class Jogador:
    def __init__(self, jogador_addr, prox_addr, sock):
        self.jogador_addr = jogador_addr
        self.prox_addr = prox_addr
        self.sock = sock
        self.fichas = 3
        self.bastao = 0
    
    def inicia_bastao(self, bastao_addr):
        self.bastao = bastao_addr
    
    def retorna_bastao(self):
        return self.bastao
    
    def passa_bastao(self):
        self.bastao = self.prox_addr

        return self.bastao
    
    def realiza_aposta(self, aposta):
        self.fichas -= aposta
    
    def recebe_aposta(self, aposta):
        self.fichas += aposta

    def cria_jogada(self):
        jogada = []

        num_jogada = input("Escolha uma jogada para realizar: ")
        num_jogada = int(num_jogada)

        if(num_jogada == 1):
            nome = '1 par'
            valor = 2
        elif(num_jogada == 2):
            nome = '1 trio'
            valor = 3
        elif(num_jogada == 3):
            nome = '2 par'
            valor = 4
        elif(num_jogada == 4):
            nome = '1 full house'
            valor = 5
        elif(num_jogada == 5):
            nome = '1 sequência baixa'
            valor = 7
        elif(num_jogada == 6):
            nome = '1 sequência alta'
            valor = 7
        elif(num_jogada == 7):
            nome = '1 quadra'
            valor = 10
        elif(num_jogada == 8):
            nome = '1 quinteto'
            valor = 15
        
        jogada.append(nome)
        jogada.append(1)
        jogada.append(self.jogador_addr)
        jogada.append(valor)
            
        return jogada
    
    def propoe_aposta(self, data):
        print('Você tem fichas:' + colored(f'{self.fichas}', 'green'))

        print (f'O jogador' + colored(f' {data[constants.MSG_DADOS][2][1]} ', 'yellow') + 'fez a jogada' + colored(f' {data[constants.MSG_DADOS][0]} ', 'red') + 'o valor da aposta está em' + colored(f' {data[constants.MSG_DADOS][1]} fichas', 'cyan'))

        res = input("\n Deseja cobrir a aposta do jogador por mais 1 ficha? (s para sim e n para não)")

        while(res != 's' and res != 'n'):
            res = input("\n Deseja cobrir a aposta do jogador por mais 1 ficha? (s para sim e n para não)")

        if(res == 's'):
            data[constants.MSG_DADOS][1] += 1
            data[constants.MSG_DADOS][2] = self.jogador_addr

    def joga_dados(self):
        dados = []
        dados.append(randint(1,6))
        dados.append(randint(1,6))
        dados.append(randint(1,6))
        dados.append(randint(1,6))
        dados.append(randint(1,6))

        return dados

    def joga_dados_com_bloqueio(self, dados, bloqueio):
        i = 0

        for block in bloqueio:
            dados[i] = dados[int(block)]
            i+=1
        
        for j in range(i, 5):
            dados[j] = randint(1,6)

        return dados


    def verifica_vitoria(self, dados, jogada):
        if (jogada == '1 par'):
            for i in range(1,7):
                if(dados.count(i) >= 2):
                    return TRUE

            return FALSE
        
        elif(jogada == '1 trio'):
            for i in range(7):
                if(dados.count(i) >= 3):
                    return TRUE

            return FALSE

        elif(jogada == '2 par'):
            num_pares = 0
            for i in range(1,7):
                if(dados.count(i) >= 2):
                    num_pares += 1
                if(dados.count(i) >= 4):
                    num_pares = 2

                if(num_pares >= 2):
                    return TRUE

            return FALSE

        elif(jogada == '1 full house'):
            num_par = 0
            num_trio = 0
            for i in range(1,7):
                if(dados.count(i) == 3):
                    num_trio = 1

                if(dados.count(i) == 2):
                    num_par += 1

                if(num_par and num_trio == 1):
                    return TRUE

            return FALSE

            
            return FALSE
        elif(jogada == '1 sequência baixa'):
            aux = []
            for i in range(1,7):
                aux.append(dados.count(i))

            if(aux[0] >= 1 and aux[1] >= 1 and aux[2] >= 1 and aux[3] >= 1):
                return TRUE
                        
            return FALSE
        elif(jogada == '1 sequência alta'):
            for i in range(1,7):
                aux.append(dados.count(i))

            if(aux[4] >= 1 and aux[1] >= 1 and aux[2] >= 1 and aux[3] >= 1):
                return TRUE
                        
            return FALSE
        elif(jogada == '1 quadra'):
            for i in range(1,7):
                if(dados.count(i) >= 4):
                    return TRUE

            return FALSE
        elif(jogada == '1 quinteto'):
            for i in range(1,7):
                if(dados.count(i) >= 5):
                    return TRUE

            return FALSE
    
    def realiza_jogada(self, data):
        self.realiza_aposta(data[constants.MSG_DADOS][1])

        dados = self.joga_dados()

        print(f'{dados}, ')

        if (self.verifica_vitoria(dados, data[constants.MSG_DADOS][0]) == TRUE):
            self.recebe_aposta(data[constants.MSG_DADOS][3])
            print('Você ganhou!!!')

            return 1

        for i in range(2):
            block = input('gostaria de bloquear algum dado? (digite n para não ou o numero dos dados que serão bloqueados)')

            if(block == 'n'):
                dados = self.joga_dados()
                print(f'{dados}, ')

            else:
                block = block.split(',')
                dados = self.joga_dados_com_bloqueio(dados, block)

                print(f'{dados}, ')
            
            if (self.verifica_vitoria(dados, data[constants.MSG_DADOS][0]) == TRUE):
                self.recebe_aposta(data[constants.MSG_DADOS][3])
                print('Você ganhou!!!')

                return 1

        print('Você é um perdedor')

        return 0
        
        