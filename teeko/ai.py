from random import *
from teeko import utils, game as g

class AI:
	def __init__(self, game: g, player, depth):
		self.game = game
		self.player = player
		self.targetDepth = depth
		self.weights = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 2, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]

	def play_random(self):
		while True:
			x = randint(0,4)
			y = randint(0,4)
			if self.game.board.state[y][x] == 0:
				break
		self.game.board.state[y][x] = self.player

	def play_minmax(self):
		print("\n ## Joueur " + str(self.player) + " ##")
		max_ = -1000
		tmp = 0
		alpha = -1000
		beta = 1000
		opponent = 1 if self.player == 2 else 2
		if self.game.turn < 8:
			max_x = 0
			max_y = 0
			for y in range(5):
				for x in range(5):
					if self.game.board.state[y][x] == 0:
						self.game.board.state[y][x] = self.player
						tmp = self.min(self.game.board.state, self.targetDepth - 1, alpha, beta, x, y)
						self.game.board.state[y][x] = 0
						if tmp > max_:
							max_ = tmp
							max_x = x
							max_y = y
			self.game.board.state[max_y][max_x] = self.player
		else:
			max_x1 = 0
			max_y1 = 0
			max_x2 = 0
			max_y2 = 0
			for y1 in range(5):
				for x1 in range(5):
					if self.game.board.state[y1][x1] == self.player:
						for y2 in range(y1-1,y1+2):
							for x2 in range(x1-1, x1+2):
								if x1!=x2 and y1!=y2 and utils.check_coord(x2) and utils.check_coord(y2) and utils.check_move(x1, y1, x2, y2, self.game.board.state):
									print("...")
									utils.move(x1,y1,x2,y2,self.game.board.state,self.player)
									tmp = self.min(self.game.board.state, self.targetDepth - 1, alpha, beta, x2, y2)
									utils.move(x2,y2,x1,y1,self.game.board.state,self.player)
									if tmp > max_:
										max_ = tmp
										max_x1 = x1
										max_y1 = y1
										max_x2 = x2
										max_y2 = y2
			utils.move(max_x1,max_y1,max_x2,max_y2,self.game.board.state,self.player)


	def min(self, state, current_depth, alpha, beta, l, m):
		if utils.is_win(state, self.player) == True or current_depth == 0:
			return self.eval(state, self.player, l, m, current_depth)
		min_ = 1000
		tmp = 0
		opponent = 1 if self.player == 2 else 2
		if self.game.turn + self.targetDepth - current_depth < 8:
			for y in range(5):
				for x in range(5):
					if state[y][x] == 0:
						state[y][x] = opponent
						beta = self.max(state, current_depth - 1, alpha, beta, x, y)
						state[y][x] = 0
						tmp = beta
						if tmp < min_:
							min_ = tmp
						if alpha >= beta:
							return beta
		else:
			for y1 in range(5):
				for x1 in range(5):
					if state[y1][x1] == opponent:
						for y2 in range(y1-1,y1+2):
							for x2 in range(x1-1, x1+2):
								if x1!=x2 and y1!=y2 and utils.check_coord(x2) and utils.check_coord(y2) and utils.check_move (x1, y1, x2, y2, state):
									utils.move(x1,y1,x2,y2,state,opponent)
									beta = self.max(state, current_depth - 1, alpha, beta, x2, y2)
									utils.move(x2,y2,x1,y1,state,opponent)
									tmp = beta
									if tmp < min_:
										min_ = tmp
									if alpha >= beta:
										return beta				
		return min_


	def max(self, state, current_depth, alpha, beta, l, m):
		opponent = 1 if self.player == 2 else 2
		if utils.is_win(state, opponent) == True or current_depth == 0:
			return self.eval(state, opponent, l, m, current_depth)
		max_ = -1000
		tmp = 0
		if self.game.turn + self.targetDepth - current_depth < 8:
			for y in range(5):
				for x in range(5):
					if state[y][x] == 0:
						state[y][x] = self.player
						alpha = self.min(state, current_depth - 1, alpha, beta, x, y)
						state[y][x] = 0
						tmp = alpha
						if tmp > max_:
							max_ = tmp
						if alpha >= beta:
							return alpha       
		else:
			for y1 in range(5):
				for x1 in range(5):
					if state[y1][x1] == self.player:
						for y2 in range(y1-1,y1+2):
							for x2 in range(x1-1, x1+2):
								if x1!=x2 and y1!=y2 and utils.check_coord(x2) and utils.check_coord(y2) and utils.check_move(x1, y1, x2, y2, state):
									utils.move(x1,y1,x2,y2,state,self.player)
									alpha = self.min(state, current_depth - 1, alpha, beta, x2, y2)
									utils.move(x2,y2,x1,y1,state,self.player)
									tmp = alpha
									if tmp > max_:
										max_ = tmp
									if alpha >= beta:
										return alpha						
		return max_

	def eval(self, state, current_player, x, y, current_depth):
		value = 0
		if utils.is_win(state, current_player):
			value = 10 + current_depth
		else: 
			value = self.weights[y][x] + utils.count_pawn_around(x,y,state)
		if current_player != self.player:
			value = -1 * value
		return value
