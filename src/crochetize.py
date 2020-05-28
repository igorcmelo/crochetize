import img
import random
import numpy as np
from sys import argv
from sys import maxsize
from PIL import Image


BLOCK = '██'

# ANSI colors
NO_COLOR = '\033[0m'
WHITE    = '\033[0;29m'
BLACK    = '\033[0;30m'
RED      = '\033[0;31m'
GREEN    = '\033[0;32m'
ORANGE   = '\033[0;33m'
BLUE     = '\033[0;34m'
MAG      = '\033[0;35m'
CYAN     = '\033[0;36m'
GREY     = '\033[0;37m'
D_GREY   = '\033[0;90m'
L_RED    = '\033[0;91m'
L_GREEN  = '\033[0;92m'
L_ORANGE = '\033[0;93m'
L_BLUE   = '\033[0;94m'
L_MAG    = '\033[0;95m'
L_CYAN   = '\033[0;96m'


def get_instructions(id_matrix, column, color_names, d):
	d = -1 if not d else 1
	instr = []
	color = None
	amount = 1

	for l in id_matrix[::d]:
		current = color_names[l[column]] 
		
		if color == current:
			amount += 1

		elif not color:
			color = current

		else:
			instr.append((amount, color))
			amount = 1

		color = current
	
	instr.append((amount, color))
	return instr


def print_instructions(instr):
	break_line = 0
	for a, c in instr:
		break_line += 1
		
		if break_line == 2:
			print()
			break_line = 0

		print(a, c)


def pprint(array, colors):
	for line in array:
		for id_ in line:
			color = colors[id_]
			print(f'{color}{BLOCK}', end='')
		print('\033[0m')


colors = [
	WHITE,
	BLACK,
	RED,
	GREEN,
	ORANGE,
	BLUE,
	MAG,
	CYAN,
	GREY,
	D_GREY,
	L_RED,
	L_GREEN,
	L_ORANGE,
	L_BLUE,
	L_MAG,
	L_CYAN,
]

fname = argv[1]
px_size = int(argv[2])
num_colors = int(argv[3])

i = Image.open(fname) 
i = img.reduce_colors(i, num_colors)
i = img.pixelate(i, px_size)

arr = np.asarray(i)

reduced = img.identify_colors(arr, px_size, px_size)
random.shuffle(colors)
pprint(reduced, colors[:num_colors])

print()
print("Give a label for each color")

labels = []

for color in colors[:num_colors]:
	label = input(f'{colors.index(color)} [{color}{BLOCK}{NO_COLOR}]: ')
	labels.append(label)

num_cols = len(reduced[0])
while True:
	col = int(input(f'Choose column [1-{num_cols}]: ')) - 1
	if col <= -1:
		break

	d = 1

	instr = get_instructions(reduced, col, labels, d)
	print_instructions(instr)
