import os
from random import shuffle
import threading
import time
import shutil

from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image

base_path = "PATH WITH THE IMAGES TO CHOSE FROM"
dest_folder = "DESTINATION OF THE FINAL SHORTLISTED PHOTOS"
amount = 39

curr_path1 = ""
curr_path2 = ""

w_box = 480
h_box = 480

def resize(w, h, w_box, h_box, pil_image):
    '''
    resize a pil_image object so it will fit into
    a box of size w_box times h_box, but retain aspect ratio
    '''
    f1 = 1.0*w_box/w  # 1.0 forces float division in Python2
    f2 = 1.0*h_box/h
    factor = min([f1, f2])
    #print(f1, f2, factor)  # test
    # use best down-sizing filter
    width = int(w*factor)
    height = int(h*factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)

def setBtn1(path):
    img = Image.open(path)
    w, h = img.size
    photo = ImageTk.PhotoImage(resize(w, h, w_box, h_box, img))
    btn1.config(image=photo, width="40", command=chose1)
    btn1.image = photo

def setBtn2(path):
    img = Image.open(path)
    w, h = img.size
    photo = ImageTk.PhotoImage(resize(w, h, w_box, h_box, img))
    btn2.config(image=photo, width="40", command=chose2)
    btn2.image = photo

def chose1(*args):
    print("Chose 1")
    sl2.append(curr_path1)
    not_chosen.set(not_chosen.get() + 1)

def chose2(*args):
    print("Chose 2")
    sl2.append(curr_path2)
    not_chosen.set(not_chosen.get() + 1)

def keepboth(*args):
    print("Both")
    sl2.append(curr_path1)
    sl2.append(curr_path2)
    not_chosen.set(not_chosen.get() + 1)

def dropboth(*args):
    print("Drop")
    not_chosen.set(not_chosen.get() + 1)

root = Tk()
root.title("Photo shortlister")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

lbl1 = ttk.Label(mainframe, text="Chose the nicest image").grid(column=1, row=1)
lbl2 = ttk.Label(mainframe)
lbl2.grid(column=2, row=1)

btn1 = ttk.Button(mainframe)
btn2 = ttk.Button(mainframe)
btn3 = ttk.Button(mainframe, text="Keep both", command=keepboth)
btn4 = ttk.Button(mainframe, text="Drop both", command=dropboth)

btn1.grid(column=1,row=2, sticky=W)
btn2.grid(column=2,row=2, sticky=E)
btn3.grid(column=1,row=3, sticky=(W, E))
btn4.grid(column=2,row=3, sticky=(W, E))

shortlist = []
sl2 = []

root.update_idletasks()
root.update()

not_chosen = IntVar()

for path, subdirs, files in os.walk(base_path):
    for name in files:
        if not (name[0:2] == '._') and name[-4:].lower() == '.jpg':
            #print(os.path.join(path, name))
            shortlist.append(os.path.join(path, name))

    lbl2.config(text="Currently there are %d images shortlisted" % len(shortlist))

while len(shortlist) > 2*amount:
    shuffle(shortlist)
    for i,k in zip(shortlist[0::2], shortlist[1::2]):
        curr_path1 = i
        curr_path2 = k
        setBtn1(curr_path1)
        setBtn2(curr_path2)
        btn1.wait_variable(not_chosen)

    shortlist, sl2 = sl2, []
    lbl2.config(text="Currently there are %d images shortlisted" % len(shortlist))

print(shortlist)

if not os.path.exists(dest_folder):
    os.makedirs(dest_folder)

with open(os.path.join(dest_folder, 'originals.txt'), 'w') as f:
    for name in shortlist:
        f.write(str(name) + str("\n"))

for name in shortlist:
    if(os.path.isfile(name)):
        shutil.copy(name, dest_folder)
