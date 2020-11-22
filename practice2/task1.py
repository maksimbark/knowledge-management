from PIL import Image, ImageDraw  # Подключим необходимые библиотеки.

image = Image.open("fail.jpg")  # Открываем изображение.
draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования.
width = image.size[0]  # Определяем ширину.
height = image.size[1]  # Определяем высоту.
pix = image.load()  # Выгружаем значения пикселей.



# повышаем яркость
koeffBright = 45

for i in range(width):
	for j in range(height):
		r = pix[i, j][0] + koeffBright
		g = pix[i, j][1] + koeffBright
		b = pix[i, j][2] + koeffBright

		if r > 255:
			r = 255
		if g > 255:
			g = 255
		if b > 255:
			b = 255
		draw.point((i, j), (r, g, b))

# увеличиваем контрастность

midlight = 0

for i in range(width):
	for j in range(height):
		midlight += pix[i, j][0] * 0.299 + pix[i, j][1] * 0.587 + pix[i, j][2] * 0.114

midlight //= width * height

k = 3
pixelChanger = []

for i in range(256):
	delta = i - midlight
	temp = round(midlight + k * delta)

	if temp < 0:
		temp = 0
	if temp > 255:
		temp = 255

	pixelChanger.append(temp)

for i in range(width):
	for j in range(height):
		r = pix[i, j][0]
		g = pix[i, j][1]
		b = pix[i, j][2]
		draw.point((i, j), (pixelChanger[r], pixelChanger[g], pixelChanger[b]))

image.save("ans.jpg", "JPEG")
del draw
