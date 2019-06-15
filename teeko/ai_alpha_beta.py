#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import *
import teeko.game as teeko
from teeko import utils
import math 
import copy
import time
import threading

class AI_Alpha_Beta:
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

	def play_alea(self):
		while True:
			x = randint(0,4)
			y = randint(0,4)
			if self.game.board.state[y][x] == 0:
				break
		self.game.board.state[y][x] = self.player

	def play_minmax(self):
		print("\n ## Joueur " + str(self.player) + " ##")
		if self.game.turn == 0:
			#self.play_alea()
			self.game.board.state[2][2] = self.player
		else:
			max_ = -10000
			tmp = 0
			alpha = -10000
			beta = 10000
			if self.game.turn < 8:
				maxX = 0
				maxY = 0
				for y in range(5):
					for x in range(5):
						if self.game.board.state[y][x] == 0:
							self.game.board.state[y][x] = self.player
							tmp = self.Min(self.game.board.state, self.targetDepth, self.targetDepth-1, self.player, self.game.turn+1,x,y, alpha, beta)
							self.game.board.state[y][x] = 0
							if tmp > max_:
								max_ = tmp
								maxX = x
								maxY = y			
				self.game.board.state[maxY][maxX] = self.player
			else:
				maxX1 = 0
				maxY1 = 0
				maxX2 = 0
				maxY2 = 0
				for y1 in range(5):
					for x1 in range(5):
						if self.game.board.state[y1][x1] == self.player:
							for y2 in range(y1-1,y1+2):
								for x2 in range(x1-1, x1+2):
									if x1!=x2 and y1!=y2 and utils.checkCoord(x2) and utils.checkCoord(y2) and utils.checkMove(x1,y1,x2,y2,self.game.board.state):
										print("...")
										utils.move(x1,y1,x2,y2,self.game.board.state,self.player)
										tmp = self.Min(self.game.board.state, self.targetDepth, self.targetDepth-1, self.player, self.game.turn+1,x2,y2, alpha, beta)
										utils.move(x2,y2,x1,y1,self.game.board.state,self.player)
										if tmp > max_:
											max_ = tmp
											maxX1 = x1
											maxY1 = y1
											maxX2 = x2
											maxY2 = y2
				utils.move(maxX1,maxY1,maxX2,maxY2,self.game.board.state,self.player)


	def Min(self, state, targetDepth, currentDepth, player, turn, k,l, alpha, beta):
		if currentDepth == 0 or utils.isWin(state, player) != 0:
			return self.eval(state, targetDepth - currentDepth, player, False, k,l)
		min_ = 10000
		tmp = 0
		if turn < 8:
			for y in range(5):
				for x in range(5):
					if state[y][x] == 0:
						state[y][x] = player
						beta = self.Max(state,targetDepth,currentDepth-1,player, turn+1,x,y, alpha, beta)
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
								if x1!=x2 and y1!=y2 and utils.checkCoord(x2) and utils.checkCoord(y2) and utils.checkMove (x1,y1,x2,y2,state):
							
									utils.move(x1,y1,x2,y2,state,player)
									beta = self.Max(state,targetDepth, currentDepth-1, player, turn+1,x2,y2, alpha, beta)
									utils.move(x2,y2,x1,y1,state,player)
									tmp = beta
									if tmp < min_:
										min_ = tmp
									if alpha >= beta:
										return beta				
		return min_


	def Max(self, state, targetDepth, currentDepth, player, turn,k,l, alpha, beta):
		opponent = 1 if player == 2 else 2
		if currentDepth == 0 or utils.isWin(state, opponent) != 0:
			return self.eval(state, targetDepth - currentDepth, opponent, True,k,l)
		max_ = -10000
		tmp = 0
		if turn < 8:
			for y in range(5):
				for x in range(5):
					if state[y][x] == 0:
						state[y][x] = opponent
						alpha = self.Min(state,targetDepth, currentDepth-1,player, turn+1,x,y, alpha, beta)
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
								if x1!=x2 and y1!=y2 and utils.checkCoord(x2) and utils.checkCoord(y2) and utils.checkMove(x1,y1,x2,y2,state):
						
									utils.move(x1,y1,x2,y2,state,opponent)
									alpha = self.Min(state,targetDepth, currentDepth-1, player, turn+1,x2,y2, alpha, beta)
									utils.move(x2,y2,x1,y1,state,opponent)
									tmp = alpha
									if tmp > max_:
										max_ = tmp
									if alpha >= beta:
										return alpha						
		return max_


	def eval(self, state, depth, player, opponent, x, y):
		if not utils.isWin(state, player):
			if opponent:
				return 0 + utils.countPawnAround(x,y,state)
			else:
				return 0 - utils.countPawnAround(x,y,state)
		elif opponent:
			return -100 + depth
		else:
			return 100 - depth


  