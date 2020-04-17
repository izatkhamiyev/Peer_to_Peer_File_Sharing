shared_files = {
'filename1': ['<text, 100kb, 24/10/1998, 127.0.0.1, 64819>', 
'<text, 100kb, 24/10/1998, 127.0.0.2, 64819>'], 
'filename3': ['<text, 100kb, 24/10/1998, 127.0.0.1, 64819>']
}
def delete_peer(addr):
    for k, v in shared_files.items():
        for i in range(len(v) - 1, -1, -1):
            ip, port = v[i][1:-1].split(", ")[-2:]
            if addr[0] == ip and int(port) == addr[1]:
                shared_files[k].remove(v[i]) 

    to_del = []
    for k in shared_files.keys():
        if not shared_files[k]:
            to_del.append(k)
    
    for i in to_del:
        del shared_files[i]

delete_peer(('127.0.0.1', 64819))
print(shared_files)