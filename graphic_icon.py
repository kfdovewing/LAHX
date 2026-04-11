import tkinter as tk
from tkinter import *
from PIL import Image

root = tk.Tk()

frame = Frame(root)
frame.pack()

canvas = Canvas(frame, bg="systemTransparent", width=700, height=400)
canvas.pack()

root.wm_attributes('-topmost', True)
root.wm_attributes('-transparent', True) # Make that color invisible
root.config(bg='systemTransparent')

character = PhotoImage(file="egg2.png")
canvas.create_image(0,0,image=character, anchor="center")

# root.image = tk.PhotoImage(file="egg2.png")
# label = tk.Label(root, image=root.image)
# label = tk.Label(root, text="Floating Text", font=("Arial", 24), fg="red")
# label.config(bg='systemTransparent')
# label.pack()
root.mainloop()
