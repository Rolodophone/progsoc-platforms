import pygame
import random
import time


def spawnPlatform():
	length = random.randint(10, 50)
	x1 = 0; x2 = 0

	Absolute = abs(x1 - x2)  # x co-ordinates of the platforms
	while not (abs(x1 - x2) > 50 and abs(x1 - x2) < 10):
		x1 = random.randint(0, 800)
		x2 = random.randint(0, 800)

		print(x1, x2)
		print(abs(x1 - x2))
	# y co-ordinates of the platforms
	"""
	for every time the player jumps off a platform and hits the next

	previousy -= 130
	y1 = y co-ordinate of previous + 130
	y2 = y1 + 10

	green = (0,200,0)
	pygame.draw.rect(surface, green, (x1, y1, x2, y2)))
	"""


class Platform:
	def __init__(self, x, y, length, ySpeed):
		self.x = x
		self.y = y
		self.length = length
		self.ySpeed = ySpeed
		self.platform_img = pygame.image.load("platform.png")

	def update(self):
		self.y += 20 * deltaTime
		pass

	def draw(self):
		# drawing the platform
		screen.blit(self.platform_img, (self.x, self.y))
		pass

	def touchingPlayer(self):
		pass


class Player:
	def __init__(self):
		self.x = 400
		self.y = 400
		self.w = 80
		self.h = 130
		self.xSpeed = 5
		self.ySpeed = 5
		self.onPlatform = False

	def update(self):
		self.y += self.ySpeed

		# player movement
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					self.x -= self.xSpeed
				elif event.key == pygame.K_RIGHT:
					self.x += self.xSpeed
				elif event.key == pygame.K_SPACE:
					self.y += self.ySpeed

		# landing
		if not self.onPlatform and self.ySpeed < 0:
			for platform in platforms:
				if platform.touchingPlayer():
					self.y = platform.y
					self.ySpeed = platform.ySpeed
					self.onPlatform = True
					break

	def draw(self):
		blue = (0, 0, 255)
		pygame.draw.rect(screen, blue, pygame.Rect(50, 50, 100, 100))
		pygame.display.flip()


def update():
	for platform in platforms:
		platform.update()

	player.update()


def draw():
	for platform in platforms:
		platform.draw()

	player.draw()


pygame.init()

screen = pygame.display.set_mode((800, 800))

platforms = []
player = Player()

deltaTime = 0

running = True

# ------ Main Game Loop --------
while running:
	initialTime = time.time()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	update()
	draw()

	pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(0, 0, 100, 100))

	pygame.display.flip()

	deltaTime = time.time() - initialTime
