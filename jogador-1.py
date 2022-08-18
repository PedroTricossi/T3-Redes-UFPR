from email.headerregistry import Address
import socket
import string
import sys
from rede import ringNetwork
from jogador import Jogador
from mensagem import Mensagem

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

jogador_addr = ('localhost', 11111)
prox_addr = ('localhost', 10001)
sock.bind(jogador_addr)

player = Jogador(jogador_addr, prox_addr, sock)
msg = Mensagem()

player.inicia_bastao(player.jogador_addr)


msg.envia_mensagem(player, prox_addr, 0, 0, 0, player.retorna_bastao())

while True:
    ringNetwork(player)

