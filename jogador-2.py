import socket
import sys

from sqlalchemy import null
from rede import ringNetwork
from jogador import Jogador

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
jogador_addr = ('localhost', 10001)
sock.bind(jogador_addr)

prox_addr = ('localhost', 10002)

player = Jogador(jogador_addr, prox_addr, sock)

while True:
    ringNetwork(player)
