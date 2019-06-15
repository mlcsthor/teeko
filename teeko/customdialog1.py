import tkinter as tk

class CustomDialog1(tk.Toplevel):
    def __init__(self, root, title, message, buttontext1, buttontext2, buttontext3, game):
        self.base = tk.Toplevel(pady = 50)
        self.base.title(title)

        w = self.base.winfo_reqwidth()
        h = self.base.winfo_reqheight()
        ws = root.winfo_reqheight()
        hs = root.winfo_reqheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.base.geometry("+%d+%d" % (x, y))

        self.label = tk.Label(self.base, text=message,font='Helvetica 18 bold')
        self.label.grid(row=0, column=0)
        

        self.scale = tk.Scale(self.base, orient='horizontal', from_=1, to=5, resolution=1, tickinterval=None, length=600)
        self.scale.grid(row=1, column=0, pady = 5)

        self.frame = tk.Frame(self.base)
        self.frame.grid(row=3, column=0, pady=10)
        self.frame.grid_columnconfigure(0, weight=275, uniform="fred")
        self.frame.grid_columnconfigure(1, weight=275, uniform="fred")
        self.frame.grid_columnconfigure(2, weight=275, uniform="fred")
        self.label1 = tk.Label(self.frame, text=buttontext1)
        self.label1.grid(row=0, column=0)
        self.label2 = tk.Label(self.frame, text=buttontext2)
        self.label2.grid(row=0, column=1)
        self.label3 = tk.Label(self.frame, text=buttontext3)
        self.label3.grid(row=0, column=2)

        self.button = tk.Button(self.frame, text="Je valide", command=self.ok, bg='blue',highlightbackground='#3E4149', font='Helvetica 15', padx = 10, pady = 5)
        self.button.grid(row=2, column=1)
        self.game = game
       
    def ok(self):
        self.game.start_game_pvai(self.scale.get())
        self.base.destroy()
    def baseconfig(self, option, value):
        self.base[option] = value
    def labelconfig(self, option, value):
        self.label[option] = value
    def buttonconfig(self, number, option, value):
        exec("self.button{}[option] = value".format(number))