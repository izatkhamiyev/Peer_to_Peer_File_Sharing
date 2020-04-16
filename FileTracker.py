# Assignment was done by:
#       Izat Khamiyev
#       Nursultan Akhmetzhanov

import socket

ftsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 7734 
ftsocket.bind((host, port))        

ftsocket.listen(5)  