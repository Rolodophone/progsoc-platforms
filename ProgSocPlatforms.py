"""
A simple platforms game. Platforms fall from random positions at the top of the screen and descend
slowly downwards. The player must jump from platform to platform to remain on the screen for as long
as possible.
"""


import pygame
import random
import time


def spawnPlatform():
	"""Spawn a new platform with random properties"""

	length = random.randint(10, 50)
	x1 = 0;
	x2 = 0

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
	"""A rectangular platform that the player can jump on"""

	def __init__(self, x, y, length, ySpeed):
		self.x = x
		self.y = y
		self.length = length
		self.ySpeed = ySpeed
		self.platform_img = pygame.image.load("platform.png")

	def update(self):
		self.y += 20 * deltaTime

	def draw(self):
		# drawing the platform
		screen.blit(self.platform_img, (self.x, self.y))

	def touchingPlayer(self):
		pass


class Player:
	"""The player"""

	Y_SPEED = 100
	"""The player's speed in the y direction when they jump or fall"""

	X_SPEED = 50
	"""The player's speed in the x direction when they are moving left or right"""

	WIDTH = 80
	HEIGHT = 130

	def __init__(self):
		self.x = 400
		self.y = 400

		self.xVelocity = 0
		"""The player's current x velocity"""

		self.yVelocity = 0
		"""The player's current y velocity"""

		self.onPlatform = False
		"""Is the player currently standing on a platform"""

	def update(self):
		# update location according to x and y velocity
		self.x += self.xVelocity * deltaTime
		self.y += self.yVelocity * deltaTime

		# landing
		# if not self.onPlatform and self.ySpeed < 0:
		# 	for platform in platforms:
		# 		if platform.touchingPlayer():
		# 			self.y = platform.y
		# 			self.ySpeed = platform.ySpeed
		# 			self.onPlatform = True
		# 			break

	def draw(self):
		# draw a rectangle representing the player
		blue = (0, 0, 255)
		pygame.draw.rect(screen, blue, pygame.Rect(self.x, self.y, Player.WIDTH, Player.HEIGHT))


def update():
	"""Called each frame to update the game state."""

	for platform in platforms:
		platform.update()

	player.update()


def draw():
	"""Called each frame to draw the frame onto the screen."""

	# draw the background
	screen.fill((0, 0, 0))

	for platform in platforms:
		platform.draw()

	player.draw()


# this must be called at the start of every Pygame program
pygame.init()

screen = pygame.display.set_mode(size=(1000, 800))
"""
The `Surface` representing the whole computer screen. 

In Pygame, a `Surface` is something you can draw on, e.g. an image. Whenever we want to draw on 
the screen we draw on the screen `Surface` and call `pygame.display.flip()` each frame to update the
actual screen with the contents of the screen `Surface`.
"""

platforms = []
"""All of the platforms on the screen"""

player = Player()
"""The player"""

deltaTime = 0
"""The time it took to complete the last frame cycle"""

running = True
"""Whether the program is currently running"""

print("Program initialised!")

# ------ Main Game Loop --------
while running:
	# record initial time (to calculate `deltaTime`)
	initialTime = time.time()

	# handle events
	for event in pygame.event.get():

		if event.type == pygame.QUIT:  # close button pressed
			running = False

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_LEFT:
				player.xVelocity = -Player.X_SPEED

			elif event.key == pygame.K_RIGHT:
				player.xVelocity = Player.X_SPEED

			elif event.key == pygame.K_SPACE:
				player.yVelocity = -Player.Y_SPEED

	# these procedures update and draw all of the platforms and the player
	update()
	draw()

	# called each frame to update the actual screen with the contents of the screen `Surface`
	pygame.display.flip()

	# `deltaTime` (the time it took to perform the last frame) is the current time minus the time
	# at the start of the frame
	deltaTime = time.time() - initialTime
