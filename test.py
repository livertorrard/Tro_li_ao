import tkinter as tk
from tkinter import *

Gui = tk.Tk()
Gui.geometry("500x500")
Gui.resizable(False, False)
frame= Frame(Gui)
Scroll = tk.Scrollbar(frame)
assistant_text = tk.Text(frame, height=5, width=50)
Scroll.pack(side=tk.RIGHT, fill=tk.Y)
assistant_text.pack(side=tk.LEFT, fill=tk.Y)
Scroll.config(command=assistant_text.yview)
assistant_text.config(yscrollcommand=Scroll.set)
quote = """HAMLET: To be, or not to be--that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune
Or to take arms against a sea of troubles
And by opposing end them. To die, to sleep--
No more--and by a sleep to say we end
The heartache, and the thousand natural shocks
That flesh is heir to. 'Tis a consummation
Devoutly to be wished."""
assistant_text.insert(tk.END, quote)
frame.place(x=50,y=50)
tk.mainloop()