import socket
import sys
from rede import ringNetwork
from jogador import Jogador

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
jogador_addr = ('localhost', 10003)
sock.bind(jogador_addr)

prox_addr = ('localhost', 11111)

player = Jogador(jogador_addr, prox_addr, sock)

while True:
    ringNetwork(player)

    