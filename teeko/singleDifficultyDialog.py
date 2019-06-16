import tkinter as tk

class SingleDifficultyDialog(tk.Toplevel):
    def __init__(self, root, title, message, difficulties, game):
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

        for index, label_text in enumerate(difficulties):
            self.frame.grid_columnconfigure(index, weight=275, uniform="fred")
            label = tk.Label(self.frame, text=label_text)
            label.grid(row=0, column=index)

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