import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import filedialog

#Functions
def new_file():
    if hasattr(window, 'filename'):
        del window.filename
    scr.delete('1.0', tk.END)

def open_file():
    window.filename =  filedialog.askopenfilename(initialdir = "/",
                               title = "Select file",
                               filetypes = (("Txt files","*.txt"),("All files","*.*")))
    if window.filename != '' and hasattr(window, 'filename'):
        with open(window.filename, 'r') as f:
            content = f.read()
        scr.delete('1.0', tk.END)
        scr.insert(tk.END, content)
    
def save_file():
    if not hasattr(window, 'filename') or window.filename == '':
        window.filename = filedialog.asksaveasfilename(initialdir = "/",
                               title = "Save file", defaultextension=".txt",
                               filetypes = (("Txt files","*.txt"),("All files","*.*")))
    if window.filename != '' and hasattr(window, 'filename'):
        with open(window.filename, 'w') as f:
            f.write(scr.get('1.0', tk.END))

def exit_file():
    window.quit()
    window.destroy()
    exit()

def do_search():
    scr.tag_remove('result', '0.0', tk.END)
    if not findStuff.get():
        return
    
    cur = 1.0
    length = tk.IntVar()
    while True:
        cur = scr.search(findStuff.get(), cur, tk.END, count=length)
        if not cur:
            break
        matchEnd = '{0}+{1}c'.format(cur, length.get())
        scr.tag_config('result', background='yellow')
        scr.tag_add('result', cur, matchEnd)
        cur = scr.index(matchEnd)

def find():
    toplevel = tk.Toplevel()
    label = ttk.Label(toplevel, text='Find:')
    label.grid(column=0, row=0)

    global findStuff
    findStuff = tk.StringVar()
    inputBox = ttk.Entry(toplevel, textvariable=findStuff, width=10)
    inputBox.grid(column=1, row=0)
    
    search = ttk.Button(toplevel, text='Search', width=8, command=do_search)
    search.grid(column=2, row=0)
    for i in toplevel.winfo_children():
        i.grid_configure(padx=4, pady=10)

def clear():
    scr.tag_remove('result', '1.0', tk.END)

#Basic Config
window = tk.Tk()
window.title(r"Kam's Notepad")
window.geometry('500x300')

#Content
#----Menu----
menuBar = Menu(window)
window.config(menu=menuBar)
#filemenu
fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label='New', command=new_file)
fileMenu.add_command(label='Open', command=open_file)
fileMenu.add_command(label='Save', command=save_file)
fileMenu.add_command(label='Exit', command=exit_file)
menuBar.add_cascade(label='File', menu=fileMenu)
#editmenu
editMenu = Menu(menuBar, tearoff=0)
editMenu.add_command(label='Find', command=find)
editMenu.add_command(label='Clear', command=clear)
menuBar.add_cascade(label='Edit', menu=editMenu)

#----Main Frame----
scr = scrolledtext.ScrolledText(window, wrap=tk.WORD)
scr.configure(font=('PMingLiU', 11))
scr.pack(fill=tk.BOTH)

#Start
window.mainloop()
