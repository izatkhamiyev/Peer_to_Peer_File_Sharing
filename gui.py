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
        for i in range(20):
            tree.insert("", "end", text=text, values=exampleList)


tk.Button(searchFrame, text="Search", command=onsearch).pack(side=tk.LEFT)


def ondownload():
    cur = tree.focus()
    if cur:
        text = tree.item(cur)['text']
        values = tree.item(cur)['values']
        print(values)
        tk.Label(window, text=f'File {text} was succesfully downloaded from {values[3]}').pack()


tk.Button(window, text="Download", command=ondownload).pack()


window.mainloop()

