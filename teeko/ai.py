from random import *
import teeko.game as teeko
from teeko import utils

class AI:
	def __init__(self, game: teeko, player, depth):
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
		if self.game.turn == 0:
			#self.play_random()
			self.game.board.state[2][2] = self.player
		else:
			max_ = -10000
			tmp = 0
			alpha = -10000
			beta = 10000
			if self.game.turn < 8:
				max_x = 0
				max_y = 0
				for y in range(5):
					for x in range(5):
						if self.game.board.state[y][x] == 0:
							self.game.board.state[y][x] = self.player
							tmp = self.min(self.game.board.state, self.targetDepth, self.targetDepth - 1, self.player, self.game.turn + 1, x, y, alpha, beta)
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
										tmp = self.min(self.game.board.state, self.targetDepth, self.targetDepth - 1, self.player, self.game.turn + 1, x2, y2, alpha, beta)
										utils.move(x2,y2,x1,y1,self.game.board.state,self.player)
										if tmp > max_:
											max_ = tmp
											max_x1 = x1
											max_y1 = y1
											max_x2 = x2
											max_y2 = y2
				utils.move(max_x1,max_y1,max_x2,max_y2,self.game.board.state,self.player)


	def min(self, state, target_depth, current_depth, player, turn, k, l, alpha, beta):
		if current_depth == 0 or utils.is_win(state, player) != 0:
			return self.eval(state, target_depth - current_depth, player, False, k, l)
		min_ = 10000
		tmp = 0
		if turn < 8:
			for y in range(5):
				for x in range(5):
					if state[y][x] == 0:
						state[y][x] = player
						beta = self.max(state, target_depth, current_depth - 1, player, turn + 1, x, y, alpha, beta)
						state[y][x] = 0
						tmp = beta
						if tmp < min_:
							min_ = tmp
						if alpha >= beta:
							return beta
		else:
			for y1 in range(5):
				for x1 in range(5):
					if state[y1][x1] == player:
						for y2 in range(y1-1,y1+2):
							for x2 in range(x1-1, x1+2):
								if x1!=x2 and y1!=y2 and utils.check_coord(x2) and utils.check_coord(y2) and utils.check_move (x1, y1, x2, y2, state):
							
									utils.move(x1,y1,x2,y2,state,player)
									beta = self.max(state, target_depth, current_depth - 1, player, turn + 1, x2, y2, alpha, beta)
									utils.move(x2,y2,x1,y1,state,player)
									tmp = beta
									if tmp < min_:
										min_ = tmp
									if alpha >= beta:
										return beta				
		return min_


	def max(self, state, target_depth, current_depth, player, turn, k, l, alpha, beta):
		opponent = 1 if player == 2 else 2
		if current_depth == 0 or utils.is_win(state, opponent) != 0:
			return self.eval(state, target_depth - current_depth, opponent, True, k, l)
		max_ = -10000
		tmp = 0
		if turn < 8:
			for y in range(5):
				for x in range(5):
					if state[y][x] == 0:
						state[y][x] = opponent
						alpha = self.min(state, target_depth, current_depth - 1, player, turn + 1, x, y, alpha, beta)
						state[y][x] = 0
						tmp = alpha
						if tmp > max_:
							max_ = tmp
						if alpha >= beta:
							return alpha       
		else:
			for y1 in range(5):
				for x1 in range(5):
					if state[y1][x1] == opponent:
						for y2 in range(y1-1,y1+2):
							for x2 in range(x1-1, x1+2):
								if x1!=x2 and y1!=y2 and utils.check_coord(x2) and utils.check_coord(y2) and utils.check_move(x1, y1, x2, y2, state):
						
									utils.move(x1,y1,x2,y2,state,opponent)
									alpha = self.min(state, target_depth, current_depth - 1, player, turn + 1, x2, y2, alpha, beta)
									utils.move(x2,y2,x1,y1,state,opponent)
									tmp = alpha
									if tmp > max_:
										max_ = tmp
									if alpha >= beta:
										return alpha						
		return max_


	def eval(self, state, depth, player, opponent, x, y):
		if not utils.is_win(state, player):
			if opponent:
				return 0 + utils.count_pawn_around(x, y, state)
			else:
				return 0 - utils.count_pawn_around(x, y, state)
		elif opponent:
			return -100 + depth
		else:
			return 100 - depth
