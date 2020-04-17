import socket
import pickle
import random
from _thread import *
import time


s = socket.socket()
host = '127.0.0.1'
port = 7771
s.connect((host, port))

local_files = [
    {"FileName":"filename1", "FileType":"text", "FileSize":"100kb", "Date":"24/10/1998"},
    {"FileName":"filename2", "FileType":"text", "FileSize":"100kb", "Date":"24/10/1998"},
    {"FileName":"filename3", "FileType":"text", "FileSize":"100kb", "Date":"24/10/1998"}
]

### GUI code starts
 
import tkinter as tk
import tkinter.ttk as ttk

window = tk.Tk()
window.geometry("480x600")
window.title("Tiger File Tracker")

h1 = tk.Label(window, text="Tiger File Tracker", font=("Colibri bold", 30))
h1.pack()

searchFrame = tk.Frame()
searchFrame.pack()

tk.Label(searchFrame, text="File Name: ").pack(side=tk.LEFT)
textField = tk.Entry(searchFrame, width=20)
textField.pack(side=tk.LEFT)

tree = ttk.Treeview(window)
tree["columns"] = ("type", "size", "modified", "ip", "port")
tree.heading("#0", text="File Name", anchor=tk.W)
tree.heading("type", text="Type", anchor=tk.W)
tree.heading("size", text="Size", anchor=tk.W)
tree.heading("modified", text="Last Modified", anchor=tk.W)
tree.heading("ip", text="Host IP", anchor=tk.W)
tree.heading("port", text="Host Port", anchor=tk.W)

tree.column("#0", width=100, stretch=tk.NO)
tree.column("type", width=50, stretch=tk.NO)
tree.column("size", width=50, )
tree.column("modified", width=100, stretch=tk.NO)
tree.column("ip", width=100, stretch=tk.NO)
tree.column("port", width=60, stretch=tk.NO)
tree.pack()

exampleList = ["png","250kb","16/04/2020","192.168.1.1","27027"]

def onsearch():
    text = textField.get()
    if text != "":
        res_list = parse_data(search(text))
        for i in res_list:
            tree.insert("", "end", text=text, values=i)


tk.Button(searchFrame, text="Search", command=onsearch).pack(side=tk.LEFT)


def ondownload():
    cur = tree.focus()
    if cur:
        text = tree.item(cur)['text']
        values = tree.item(cur)['values']
        p2p_request([text, values[0], values[1]], values[3], int(values[4]))
        tk.Label(window, text=f'File {text} was succesfully downloaded from {values[3]}').pack()


tk.Button(window, text="Download", command=ondownload).pack()

### GUI code ends


def parse_data(data):
    res = [val[1:-1].split(", ") for val in data]
    return res


def prepare_local_files(ip, port):
    files = []
    for f in local_files:
        files.append("<{}, {}, {}, {}, {}, {}>"
        .format(f["FileName"], f["FileType"], f["FileSize"], f["Date"], ip, port))
    return files


def receive_message(peer):
    message = peer.recv(2048)
    if not message:
        return
    return pickle.loads(message)


def search(filename):
    message = "SEARCH " + filename
    message = pickle.dumps(message)
    s.send(message)
    res = receive_message(s)
    if res == "FOUND: ":
        data = s.recv(2024)
        data = pickle.loads(data)
        return data
    else:
        return []


def p2p_request(file_record, peer_ip, peer_port):
    peer = socket.socket()
    peer.connect((peer_ip, int(peer_port)))
    message = "DOWNLOAD: " + file_record[0] + ", " + file_record[1] + ", " + file_record[2]
    peer.send(pickle.dumps(message))
    data = peer.recv(2048)
    data = pickle.loads(data)
    print(data)



def p2p_listen_thread(port):
    p2p_socket = socket.socket()
    p2p_socket.bind(('', port))
    p2p_socket.listen(5)
    while True:
        peer_client, addr = p2p_socket.accept()
        message = peer_client.recv(2048)
        message = pickle.loads(message)
        req = message[0:10]
        file_info = message[10:].split(", ")
        if "DOWNLOAD: " == req:
            peer_client.send(pickle.dumps("THNAKSa"))


def establish_connection(files, listen_port):
    s.send(pickle.dumps("HELLO"))
    hand_shake_ack = receive_message(s)
    if hand_shake_ack != "HI":
        return
    s.send(pickle.dumps(files))
    start_new_thread(p2p_listen_thread, (listen_port,))


def leave_FT():
    s.send(pickle.dumps("BYE"))
    s.close()


listen_port = 60000 + random.randint(1, 5000) 
establish_connection(prepare_local_files(host,listen_port), listen_port)

window.mainloop()

leave_FT()