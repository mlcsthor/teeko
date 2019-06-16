import tkinter as tk

class DualDifficultyDialog(tk.Toplevel):
    def __init__(self, root, title, message, game):
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

        self.scale1 = tk.Scale(self.base, orient='horizontal', from_=1, to=5, resolution=1, tickinterval=2, length=600, label='IA n°1')
        self.scale1.grid(row=1, column=0, pady = 5)
        self.scale2 = tk.Scale(self.base, orient='horizontal', from_=1, to=5, resolution=1, tickinterval=2, length=600, label='IA n°2')
        self.scale2.grid(row=2, column=0, pady = 5)

        self.frame = tk.Frame(self.base)
        self.frame.grid(row=3, column=0, pady=10)

        for i in range(3):
            self.frame.grid_columnconfigure(i, weight=275, uniform="fred")
       
        self.button = tk.Button(self.frame, text="Je valide", command=self.ok, bg='blue',highlightbackground='#3E4149', font='Helvetica 15', padx = 10, pady = 5)
        self.button.grid(row=3, column=1)
        self.game = game

    def ok(self):
        scale1 = self.scale1.get()
        scale2 = self.scale2.get()

        self.base.destroy()
        self.game.start_game_aivai(scale1, scale2)

    def baseconfig(self, option, value):
        self.base[option] = value

    def labelconfig(self, option, value):
        self.label[option] = value

    def buttonconfig(self, number, option, value):
        exec("self.button{}[option] = value".format(number))