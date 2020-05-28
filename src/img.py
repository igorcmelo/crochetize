from PIL import Image


def reduce_colors(image, num):
	return image.convert (
		'P', 
		palette=Image.ADAPTIVE, 
		colors=num
	)


def pixelate(image, pixel_size):
	image = image.resize ((
		image.size[0] // pixel_size,
		image.size[1] // pixel_size,
	), Image.NEAREST)

	image = image.resize ((
		image.size[0] * pixel_size,
		image.size[1] * pixel_size,
	), Image.NEAREST)

	return image


def identify_colors(arr, line_gap, col_gap):
	h, w = arr.shape
	
	maxl = h // line_gap
	maxc = w // line_gap

	colors = []
	reduced = []

	for l in range(maxl):
		line = line_gap * l
		reduced.append([])

		for c in range(maxc):
			col = col_gap * c
			rgb = arr[line][col].tolist()

			try:
				id_ = colors.index(rgb)
				reduced[l].append(id_)
			
			except ValueError:
				reduced[l].append(len(colors))
				colors.append(rgb)

	return reduced

