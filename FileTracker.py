# Assignment was done by:
#       Izat Khamiyev
#       Nursultan Akhmetzhanov

import socket
import pickle
from _thread import *


ftsocket = socket.socket()
host = '127.0.0.1'
port = 7772
ftsocket.bind(('', port))
ftsocket.listen(5)  

shared_files = {}
online_peers = {}
keys = ["Filename", "File-Type", "File-Size", "Last-Modified-Data", "IP-address", "Port"]


def delete_peer(addr):
    for k, v in shared_files.items():
        for i in range(len(v) - 1, -1, -1):
            # ip, port = v[i][1:-1].split(", ")[-2:]
            # if addr[0] == ip and int(port) == addr[1]:
            if v[i] in online_peers[addr]:    
                shared_files[k].remove(v[i]) 

    to_del = []
    for k in shared_files.keys():
        if not shared_files[k]:
            to_del.append(k)
    
    for i in to_del:
        del shared_files[i]

    if addr in online_peers:
        del online_peers[addr]


def parse_reveived_data(addr, data):
    for piece in data:
        splitted_data = [val.strip() for val in str(piece[1:-1]).split(',')]
        value = ", ".join(splitted_data[1:])
        value = "<" + value + ">"
        if splitted_data[0] in shared_files:
            shared_files[splitted_data[0]].append(value)
        else:
            shared_files[splitted_data[0]] = [value]

        if addr in online_peers:
            online_peers[addr].append(value)
        else:
            online_peers[addr] = [value]


def search(filename):
    if filename in shared_files:
        return shared_files[filename]


def get_peer(peer, addr):
    hand_shake = peer.recv(2048)
    hand_shake = pickle.loads(hand_shake)
    if(hand_shake != "HELLO"):
        peer.close()
        return
    peer.send(pickle.dumps("HI"))
    
    data = peer.recv(2048)
    data = pickle.loads(data)
    parse_reveived_data(addr, data)
   
    #accept peer
    while True:
        req = peer.recv(2048)#receive_message(peer)
        req = pickle.loads(req)
        if "SEARCH" in req:
            files = search(req.split()[1])
            if not files:
                peer.send(pickle.dumps("NOT FOUND"))
            else:
                res = "FOUND: "
                for f in range(len(files)):
                    res += files[f]
                    if f != len(files) - 1:
                        res += ";"
                peer.send(pickle.dumps(res))
        if "BYE" in req:
            delete_peer(addr)
            break
    peer.close()
    exit()

while True:
    peer, addr = ftsocket.accept()
    start_new_thread(get_peer, (peer, addr)) 
    
