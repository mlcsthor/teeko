from PIL import Image, ImageTk

def contains(small_list: list, big_list: list):
	for i in range(len(big_list) - len(small_list) + 1):
		for j in range(len(small_list)):
			if big_list[i+j] != small_list[j]:
				break
		else:
			return i, i + len(small_list)
	return False

def input_integer_with_bounds(min_bound: int, max_bound: int, message: str):
	n = int(input(message))

	while not min_bound <= n <= max_bound:
		print('Incorrect value')
		n = int(input(message))

	return n

def input_coordinates(min_bound: int, max_bound: int):
	x = input_integer_with_bounds(min_bound, max_bound, 'Coord x : ')
	y = input_integer_with_bounds(min_bound, max_bound, 'Coord y : ')

	return x, y

def load_image(filename: str, size: tuple = None):
	image = Image.open('assets/{}'.format(filename)).convert('RGBA')

	if size: image = image.resize(size)

	return ImageTk.PhotoImage(image)

## Thomas
def get_coord(string):
	while True:
		x = int(input(string))
		if check_coord(x):
			break
		print("Nombre entre 0 et 4 inclus")
	return x

def check_coord(x):
	if 0 <= x < 5 :
		return True
	return False

def count_pawn_around(x1, y1, state):
	c = 0
	for y2 in range(y1-1, y1+2):
		for x2 in range(x1-1, x1+2):
			if x1!=x2 or y1!=y2 and check_coord(x2) and check_coord(y2) and state[y2][x2] == state[y1][x1]:
				c = c + 1
	return c


def check_move(x1, y1, x2, y2, state):
	if abs(x1 - x2) > 1 or abs(y1 - y2) > 1:
		return False
	if state[y2][x2] != 0:
		return False
	return True

def move(x1, y1, x2, y2, state, player):
	state[y1][x1] = 0
	state[y2][x2] = player
	return state


def is_win(state, player):
	k = 0
	while k<25 and state[int((k-(k%5))/5)][k%5]!=player:
		k = k+1
	i = int((k-(k%5))/5)
	j = k%5
	if i < 4 and j < 4 and state[i][j+1] == state[i+1][j] == state[i+1][j+1] == player: #carré
		return True
	elif j < 2 and state[i][j+1] == state[i][j+2] == state[i][j+3] == player: #ligne
		return True
	elif i < 2 and state[i+1][j] == state[i+2][j] == state[i+3][j] == player: #colonne
		return True
	elif i < 2 and j < 2 and state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3] == player: #diagonale 
		return True
	elif i < 2 and j > 2 and state[i+1][j-1] == state[i+2][j-2] == state[i+3][j-3] == player: #diagonale
		return True
	else:
		return False