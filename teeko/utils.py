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