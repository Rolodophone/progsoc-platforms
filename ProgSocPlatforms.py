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

	WIDTH = 71*4
	HEIGHT = 16*4

	def __init__(self, length, height, ySpeed):
		self.randomise_x()
		self.y = random.randint(0, SCREEN_HEIGHT)
		self.length = length
		self.height = height
		smallImg = pygame.image.load("platform.png")
		self.platform_img = pygame.transform.scale(smallImg, (Platform.WIDTH, Platform.HEIGHT))
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

	def touchingPlayer(self):
		thisRect = pygame.Rect(self.x, self.y, Platform.WIDTH, Platform.HEIGHT)
		playerRect = pygame.Rect(player.x, player.y, Player.WIDTH, Player.HEIGHT)
		return thisRect.colliderect(playerRect)


class Player:
	"""The player"""

	JUMP_VELOCITY = -3000
	"""The player's speed in the y direction when they jump or fall"""

	X_SPEED = 400
	"""The player's speed in the x direction when they are moving left or right"""

	GRAVITY = 12000
	"""The player's acceleration downwards"""

	WIDTH = 29*2
	HEIGHT = 45*2

	def __init__(self):
		self.x = 400
		self.y = -Player.HEIGHT

		self.yVelocity = 0
		"""The player's current y velocity"""

		self.onPlatform = True
		"""Is the player currently standing on a platform"""

		smallImg = pygame.image.load("character.png")
		self.playerImg = pygame.transform.scale(smallImg, (Player.WIDTH, Player.HEIGHT))

	def update(self):
		# update x location
		keyIsPressed = pygame.key.get_pressed()
		if keyIsPressed[pygame.K_LEFT]:
			self.x -= Player.X_SPEED * deltaTime
		if keyIsPressed[pygame.K_RIGHT]:
			self.x += Player.X_SPEED * deltaTime

		# update onPlatform
		self.onPlatform = False
		for platform in platforms:
			self.onPlatform = self.y == platform.y - Player.HEIGHT

		# apply gravity
		if not self.onPlatform:
			self.yVelocity += Player.GRAVITY * deltaTime

		# apply velocity
		self.y += self.yVelocity * deltaTime

		# landing
		if not self.onPlatform and self.yVelocity > 0:
			for platform in platforms:
				if platform.touchingPlayer():
					self.y = platform.y - Player.HEIGHT
					self.yVelocity = platform.ySpeed
					self.onPlatform = True
					break

	def draw(self):
		screen.blit(self.playerImg, (self.x, self.y))


def update():
	"""Called each frame to update the game state."""

	global endMessage, running, score_number, start_time, score

	# get the number for the score
	score_number = pygame.time.get_ticks() - start_time
	score = myfont.render(f"SCORE: {score_number}", False, (255, 255, 255))

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
	screen.blit(score, (10, 10))

	for platform in platforms:
		platform.draw()

	player.draw()


# this must be called at the start of every Pygame program
pygame.init()
pygame.font.init()

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
platforms = [Platform(10, 5, random.randint(10, 100)) for i in range(NO_OF_PLATFORMS)]


player = Player()
"""The player"""

deltaTime = 0
"""The time it took to complete the last frame cycle"""

running = True
"""Whether the program is currently running"""

endMessage = None
"""If this is not none, the game ends and the message is displayed"""

# ------------------- Creating score ----------------------------------- #
start_time = pygame.time.get_ticks()
score_number = pygame.time.get_ticks() - start_time
myfont = pygame.font.SysFont('Arial', 30)
score = myfont.render(f"SCORE: {score_number}", False, (255, 255, 255))
# ---------------------------------------------------------------------- #

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
		game_over_background = pygame.image.load("gameOverBackground.jpg")
		screen.blit(game_over_background, (0, 0))
		textsurface = gameOverFont.render(endMessage, True, pygame.Color("white"))
		screen.blit(textsurface, (20, 20))

	# called each frame to update the actual screen with the contents of the screen `Surface`
	pygame.display.flip()

	# `deltaTime` (the time it took to perform the last frame) is the current time minus the time
	# at the start of the frame
	deltaTime = time.time() - initialTime
