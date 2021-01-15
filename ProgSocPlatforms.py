"""
A simple platforms game. Platforms fall from random positions at the top of the screen and descend
slowly downwards. The player must jump from platform to platform to remain on the screen for as long
as possible.
"""


import pygame
import random
import time


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Platform:
	"""A rectangular platform that the player can jump on"""

	def __init__(self, length, height, ySpeed):
		self.randomise_x()
		self.y = random.randint(0, SCREEN_HEIGHT)
		self.length = length
		self.height = height
		self.platform_img = pygame.image.load("platform.png")
		self.ySpeed = ySpeed

	def randomise_x(self):
		self.x = random.randint(0, SCREEN_WIDTH)

	def update(self):
		self.y += self.ySpeed * deltaTime
		if self.y > SCREEN_HEIGHT:
			self.y = 0
			self.randomise_x()

	def draw(self):
		# drawing the platform
		screen.blit(self.platform_img, (self.x, self.y))

	def touchingPlayer(self, player_x, player_y):
		if self.x == player_x and self.y == player_y - (self.height / 2):
			# every time the player gets on the platform, its position
			# is going to be the same as the platform
			player_x = self.x
			player_y = self.y - (self.height / 2)
			pass


class Player:
	"""The player"""

	JUMP_VELOCITY = -3000
	"""The player's speed in the y direction when they jump or fall"""

	X_SPEED = 400
	"""The player's speed in the x direction when they are moving left or right"""

	GRAVITY = 12000
	"""The player's acceleration downwards"""

	WIDTH = 40
	HEIGHT = 80

	def __init__(self):
		self.x = 400
		self.y = 400

		self.yVelocity = 0
		"""The player's current y velocity"""

		self.onPlatform = True
		"""Is the player currently standing on a platform"""

	def update(self):
		# update x location
		keyIsPressed = pygame.key.get_pressed()
		if keyIsPressed[pygame.K_LEFT]:
			self.x -= Player.X_SPEED * deltaTime
		if keyIsPressed[pygame.K_RIGHT]:
			self.x += Player.X_SPEED * deltaTime

		# update y location
		if not self.onPlatform:
			self.yVelocity += Player.GRAVITY * deltaTime

		self.y += self.yVelocity * deltaTime

		# landing
		if not self.onPlatform and self.yVelocity > 0:
			for platform in platforms:
				if platform.touchingPlayer(self.x, self.y):
					self.y = platform.y - Player.HEIGHT
					self.yVelocity = platform.ySpeed
					self.onPlatform = True
					break

	def draw(self):
		# draw a rectangle representing the player
		blue = (0, 0, 255)
		pygame.draw.rect(screen, blue, pygame.Rect(self.x, self.y, Player.WIDTH, Player.HEIGHT))


def update():
	"""Called each frame to update the game state."""

	global endMessage, running

	for platform in platforms:
		platform.update()

	player.update()

	# Check if player has fallen off screen
	if player.y > SCREEN_HEIGHT:
		endMessage = "GAME OVER!"


def draw():
	"""Called each frame to draw the frame onto the screen."""

	# draw the background
	screen.fill((0, 0, 0))

	for platform in platforms:
		platform.draw()

	player.draw()


# this must be called at the start of every Pygame program
pygame.init()

gameOverFont = pygame.font.SysFont('Arial', 30)

screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
"""
The `Surface` representing the whole computer screen. 

In Pygame, a `Surface` is something you can draw on, e.g. an image. Whenever we want to draw on 
the screen we draw on the screen `Surface` and call `pygame.display.flip()` each frame to update the
actual screen with the contents of the screen `Surface`.
"""

"""All of the platforms on the screen"""
NO_OF_PLATFORMS = 8
platforms = [ Platform(10, 5, random.randint(10,100)) for i in range(NO_OF_PLATFORMS) ]


player = Player()
"""The player"""

deltaTime = 0
"""The time it took to complete the last frame cycle"""

running = True
"""Whether the program is currently running"""

endMessage = None
"""If this is not none, the game ends and the message is displayed"""

print("Program initialised!")

# ------ Main Game Loop --------
while running:
	# record initial time (to calculate `deltaTime`)
	initialTime = time.time()

	# handle events
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			# close window when close button pressed
			running = False
			print("Quitting game")

		elif event.type == pygame.KEYDOWN:

			if event.key == pygame.K_SPACE:
				# make the player jump when space is pressed
				player.yVelocity = Player.JUMP_VELOCITY
				player.onPlatform = False
				print("Player jumped")

	if endMessage is None:
		# these procedures update and draw all of the platforms and the player
		update()
		draw()
	else:
		# game over
		screen.fill(0)
		textsurface = gameOverFont.render(endMessage, True, pygame.Color("white"))
		screen.blit(textsurface, (20, 20))

	# called each frame to update the actual screen with the contents of the screen `Surface`
	pygame.display.flip()

	# `deltaTime` (the time it took to perform the last frame) is the current time minus the time
	# at the start of the frame
	deltaTime = time.time() - initialTime
