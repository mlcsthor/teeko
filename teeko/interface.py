import tkinter
from teeko import utils
import teeko.game as teeko
from PIL import ImageTk

WIDTH = 1400
HEIGHT = 750
PLAYERS_COLOR = ['#53F798', '#E94057']
BACKGROUND_COLOR = '#161719'

class Interface:
    def __init__(self, game: teeko):
        self.game = game
        self.game.set_interface(self)

        self.pawnPositionDraw = []
        self.potentialMovesDraw = []

        self.offsetX = 402
        self.offsetY = 77
        self.distanceBetweenCircles = 149

        root = self.configure_root()
        self.set_background(root)


        frame = tkinter.Frame(root)
        frame.pack(side = tkinter.BOTTOM)

        self.canvas = tkinter.Canvas(frame, width=WIDTH, height=HEIGHT, bg=BACKGROUND_COLOR, highlightthickness=0)

        board_image = utils.load_image('board.png')
        self.draw_image(board_image, (WIDTH/2, HEIGHT/2))

        self.add_buttons()
        self.add_handler()

        self.canvas.pack()

        root.mainloop()

    @staticmethod
    def configure_root():
        root = tkinter.Tk()
        root.title('Teeko')
        root.configure(background=BACKGROUND_COLOR)
        root.geometry('{}x900'.format(WIDTH))
        root.resizable(False, False)

        return root

    @staticmethod
    def set_background(root):
        background_image = utils.load_image('background3.png')

        background_label = tkinter.Label(root, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background_image

    def add_buttons(self):
        button_pai = utils.load_image('button_pai.png', (175, 40))

        button = tkinter.Button(self.canvas, image=button_pai, background=BACKGROUND_COLOR,highlightbackground=BACKGROUND_COLOR)
        button.place(x=0 + button_pai.width()/2, y=HEIGHT - button_pai.height()*2)
        button.image = button_pai
        #self.draw_image(button_pai, (0 + button_pai.width(), HEIGHT - button_pai.height()*2))

        button_pvp = utils.load_image('button_pvp.png', (175, 40))
        self.draw_image(button_pvp, (0 + button_pvp.width(), HEIGHT - button_pai.height()*3.5))

    def add_handler(self):
        self.canvas.bind('<Button-1>', self.on_click)

    def on_click(self, event):
        if not self.game.game_launched: return

        print(event.x)
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
                        if self.game.board.playerWantToMove:
                            if self.game.board.can_choose((x, y), self.game.player):
                                self.game.board.select_pawn((x, y))

                                self.clear_potential_moves()
                                self.show_potential_moves()

                            if self.game.board.can_move((x, y)):
                                self.game.board.move((x, y), self.game.player)
                                self.game.next_turn()
                        else:
                            self.clear_potential_moves()

                            if self.game.board.can_choose((x, y), self.game.player):
                                self.game.board.select_pawn((x, y))
                                self.show_potential_moves()

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

                self.canvas.pack()

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