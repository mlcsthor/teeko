import tkinter
from tkinter.messagebox import showerror, showinfo
from .singleDifficultyDialog import *
from .dualDifficultyDialog import *
from teeko import utils, config
from teeko import game as g
from PIL import ImageTk

class Interface:
    def __init__(self, game: g):
        self.game = game
        self.game.set_interface(self)
        self.pawnPositionDraw = []
        self.potentialMovesDraw = []

        self.offsetX = 402
        self.offsetY = 77
        self.distanceBetweenCircles = 149

        self.root = self.configure_root()
        self.set_background(self.root)

        frame = tkinter.Frame(self.root)
        frame.pack(side = tkinter.BOTTOM)

        self.canvas = tkinter.Canvas(frame, width=config.WINDOW_WIDTH, height=config.CANVAS_HEIGHT,
             bg=config.BACKGROUND_COLOR, highlightthickness=0)

        board_image = utils.load_image('board.png')
        self.draw_image(board_image, (config.WINDOW_WIDTH/2, config.CANVAS_HEIGHT/2))

        self.add_buttons()
        self.add_handler()

        self.canvas.pack()

        self.root.mainloop()

    @staticmethod
    def configure_root():
        root = tkinter.Tk()
        root.title('Teeko')
        root.configure(background=config.BACKGROUND_COLOR)
        root.geometry('{}x{}'.format(config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        root.resizable(False, False)

        return root

    @staticmethod
    def set_background(root):
        background_image = utils.load_image('background.png')

        background_label = tkinter.Label(root, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image

    def add_buttons(self):
        pvai_image = utils.load_image('button_pvai.png', (175, 40))
        aivai_image = utils.load_image('button_aivai.png', (175, 40))
        pvp_image = utils.load_image('button_pvp.png', (175, 40))

        button_pvp = tkinter.Button(self.canvas, image=pvp_image, background=config.BACKGROUND_COLOR,
            activebackground=config.BACKGROUND_COLOR, bd=0, highlightthickness=0, command=self.game.launch_game_pvp)
        button_pvp.place(x=0 + pvai_image.width()/2, y=config.CANVAS_HEIGHT - pvp_image.height()*5)
        button_pvp.image = pvp_image

        button_pvai = tkinter.Button(self.canvas, image=pvai_image, background=config.BACKGROUND_COLOR,
            activebackground=config.BACKGROUND_COLOR, bd=0, highlightthickness=0, command=self.game.launch_game_pvai)
        button_pvai.place(x=0 + pvai_image.width()/2, y=config.CANVAS_HEIGHT - pvai_image.height()*3.5)
        button_pvai.image = pvai_image

        button_aivai = tkinter.Button(self.canvas, image=aivai_image, background=config.BACKGROUND_COLOR,
            activebackground=config.BACKGROUND_COLOR, bd=0, highlightthickness=0, command=self.game.launch_game_aivai)
        button_aivai.place(x=0 + aivai_image.width()/2, y=config.CANVAS_HEIGHT - aivai_image.height()*2)
        button_aivai.image = aivai_image

    def add_handler(self):
        self.canvas.bind('<Button-1>', self.on_click)

    def on_click(self, event):
        print(self.game.game_launched)

        if not self.game.game_launched: return

        for i in range(self.offsetX, self.offsetX + 5*self.distanceBetweenCircles, self.distanceBetweenCircles):
            for j in range(self.offsetY, self.offsetY + 5*self.distanceBetweenCircles, self.distanceBetweenCircles):
                if i + 34 >= event.x > i - 34 and j + 34 >= event.y > j - 34:
                    x = int((i - self.offsetX)/self.distanceBetweenCircles)
                    y = int((j - self.offsetY)/self.distanceBetweenCircles)

                    if self.game.is_placement_phase():
                        if self.game.board.can_play((x, y)):
                            self.game.board.play((x, y), self.game.player)
                            self.game.next_turn()
                            break
                        else:
                            self.show_error()
                    else:
                        if self.game.board.playerWantToMove:
                            if self.game.board.can_choose((x, y), self.game.player):
                                self.game.board.select_pawn((x, y))

                                self.clear_potential_moves()
                                self.show_potential_moves()
                            elif self.game.board.can_move((x, y)):
                                self.game.board.move((x, y), self.game.player)
                                self.game.next_turn()
                            else:
                                self.show_error()
                        else:
                            self.clear_potential_moves()

                            if self.game.board.can_choose((x, y), self.game.player):
                                self.game.board.select_pawn((x, y))
                                self.show_potential_moves()
                            else:
                                self.show_error()

    def show_potential_moves(self):
        locations = self.game.board.get_possible_move_locations(self.game.board.playerSelected)

        for location in locations:
            (x, y) = location

            new_x = x*self.distanceBetweenCircles + self.offsetX
            new_y = y*self.distanceBetweenCircles + self.offsetY

            move_image = utils.load_image('move{}.png'.format(self.game.player))
            move = self.draw_image(move_image, (new_x, new_y))

            self.potentialMovesDraw.append(move)
            self.canvas.pack()

    def show_game(self):
        print("Show Game")
        self.clear_board()

        for i in range(5):
            for j in range(5):
                x = i*self.distanceBetweenCircles + self.offsetX
                y = j*self.distanceBetweenCircles + self.offsetY

                pawn = None

                if self.game.board.state[j][i] is not 0:
                    pawn_image = utils.load_image('pawn{}.png'.format(self.game.board.state[j][i]))
                    pawn = self.draw_image(pawn_image, (x, y))

                if pawn: self.pawnPositionDraw.append(pawn)

        self.canvas.update_idletasks() 


    def clear_potential_moves(self):
        for pos in self.potentialMovesDraw: self.canvas.delete(pos)
        self.canvas.pack()

    def clear_board(self):
        for pos in self.pawnPositionDraw: self.canvas.delete(pos)
        self.clear_potential_moves()

    def draw_image(self, image: ImageTk, coord: tuple):
        (x, y) = coord

        # Keep references so tkinter doesn't delete the image
        label = tkinter.Label()
        label.photo = image

        return self.canvas.create_image(x, y,  image=image)


    def ask_difficulty(self, mode):
        if mode == 1:
            difficulties = [
                'Facile, pfff',
                'Plus difficile que \'Facile\'',
                'Non sérieusement,\n laisse tomber'
            ]

            SingleDifficultyDialog(self.root, "Difficulté", 'Choisis un niveau de difficulté', difficulties, self.game)
        else:
            DualDifficultyDialog(self.root, "Difficultés", 'Choisis un niveau de difficulté pour les 2 IA', self.game)
        

    @staticmethod
    def show_error():
        showerror('Erreur', 'Vous ne pouvez pas jouer ce coup !')

    def show_winner(self):
        showinfo('Fin de partie', 'Le Joueur {} a gagné !'.format(self.game.player))
        self.game.launched = False