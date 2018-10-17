from tkinter import *
from PIL import ImageTk, Image
import os

root = Tk()
root.geometry("800x500")
img = ImageTk.PhotoImage(Image.open("images/vn.png"))
panel = Label(root, image=img)
panel.pack(side="bottom", fill="both", expand="yes")
entry = Entry(root, width=10).pack(side=TOP,padx=10,pady=10)
entry.bind('<Return>', )
root.mainloop()
