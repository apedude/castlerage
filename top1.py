# import lib
import math
import pygame
import random

# color definition
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
BLUE  = (0,0,255)
RED   = (255,0,0)
YELLOW = (255,255,0)
ORANGE = (255,150,0)

clock = pygame.time.Clock()

# Classes
class GameMenu():
	def __init__(self,screen,items,bgColor,fontColor):
		self.screen = screen
		self.scr_width = self.screen.get_rect().width
		self.scr_height = self.screen.get_rect().height
		self.bgColor = bgColor
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont('Calibri',25,False,False)
		self.fontColor = fontColor
		self.items = []
		for index, item in enumerate(items):
			label = self.font.render(item,True,fontColor)
			width = label.get_rect().width
			height = label.get_rect().height
 
			posx = (self.scr_width / 2) - (width / 2)
			# t_h: total height of text block
			t_h = len(items) * height * 3
			posy = (self.scr_height / 2) - (t_h / 2) + (index * height)
 
			self.items.append([item, label, (width, height), (posx, posy)])
 

	def run(self):
		mainLoop = True
		while mainLoop:
			self.clock.tick(50)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					mainLoop = False
			self.screen.fill(self.bgColor)	
			
			for name, label, (width, height), (posx, posy) in self.items:
				self.screen.blit(label, (posx, posy))
			pygame.display.flip()




class Character(pygame.sprite.Sprite):
	speedX = 0
	speedY = 0
	maxSpeed = 0
	hp = 0
	walls = None
	bullets = pygame.sprite.Group()
#	pointX = [200,600,800]
#	pointY = [75,75,300]
#	it = 0
	
	def __init__(self,startpos = (50,100),maxSpeed = 0,size = 0,color = BLACK,hp = 0):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([size,size])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.x = startpos[0]
		self.rect.y = startpos[1]
		self.maxSpeed = maxSpeed
		self.hp = hp

	def move(self):
		pressedkeys=pygame.key.get_pressed()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				self.speedX  = (self.maxSpeed)*(-1)
			if event.key == pygame.K_RIGHT:
				self.speedX  = self.maxSpeed
			if event.key == pygame.K_UP:
				self.speedY  = (self.maxSpeed)*(-1)
			if event.key == pygame.K_DOWN:
				self.speedY  = self.maxSpeed

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				self.speedX = 0
			if event.key == pygame.K_RIGHT:
				self.speedX = 0
			if event.key == pygame.K_UP:
				self.speedY = 0
			if event.key == pygame.K_DOWN:
				self.speedY = 0
		if pressedkeys[pygame.K_SPACE]:
			bullet = Bullet(self)
			self.bullets.add(bullet)
		if pressedkeys[pygame.K_LCTRL]: 
			pygame.time.wait(clock.get_time())


		
#	def follow(self):
#		if self.it < 3:
#			for i in range(self.it,self.it+1):
#				if self.rect.x != self.pointX[i] or self.rect.y != self.pointY[i]:
#					dx = self.pointX[i] - self.rect.x
#					dy = self.pointY[i] - self.rect.y
#			  		dist = math.hypot(dx, dy)
#			  		dx = dx / dist
#	  				dy = dy / dist
#		  			self.speedX = dx * self.maxSpeed
 #       				self.speedY = dy * self.maxSpeed
#				else:
#					self.it +=1

	def update(self):
		self.rect.x += self.speedX
		block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
		for block in block_hit_list:
		# If we are moving right, set our right side to the left side of the item we hit
			if self.speedX > 0 :
				self.rect.right = block.rect.left
			else:
				self.rect.left = block.rect.right
		# Check and see if we hit anything
		self.rect.y += self.speedY
		block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
		for block in block_hit_list:
		# Reset our position based on the top/bottom of the object.
			if self.speedY > 0:
				self.rect.bottom = block.rect.top
			else:
				self.rect.top = block.rect.bottom

#		bullet_hit_list = pygame.sprite.spritecollide(creep,self.bullets, True)
#		for hit in bullet_hit_list:
#			creep.hp -= 1
#			if creep.hp == 0:
#				creep.kill()
				

class Creep(pygame.sprite.Sprite):

	walls = None
	bullets = None
	pointX = [200,600,800]
	pointY = [75,75,300]
	it = 0

	def __init__(self,startpos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([12,12])
		self.image.fill(BLUE)
		self.rect = self.image.get_rect()
		self.rect.x = startpos[0]
		self.rect.y = startpos[1]
		self.maxSpeed = 1.5
		self.speedX = 0
		self.speedY = 0
		self.hp = 25

	def follow(self):
		if self.it < 3:
			for i in range(self.it,self.it+1):
				if self.rect.x != self.pointX[i] or self.rect.y != self.pointY[i]:
					dx = self.pointX[i] - self.rect.x
					dy = self.pointY[i] - self.rect.y
					dist = math.hypot(dx, dy)
					dx = dx / dist
					dy = dy / dist
					self.speedX = dx * self.maxSpeed
					self.speedY = dy * self.maxSpeed
				else:
					self.it +=1


	def update(self):
		self.rect.x += self.speedX
		block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
		for block in block_hit_list:
			if self.speedX > 0 :
				self.rect.right = block.rect.left
			else:
				self.rect.left = block.rect.right

		self.rect.y += self.speedY
		block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
		for block in block_hit_list:
			if self.speedY > 0:
				self.rect.bottom = block.rect.top
			else:
				self.rect.top = block.rect.bottom

		bullet_hit_list = pygame.sprite.spritecollide(self,self.bullets, True)
		for hit in bullet_hit_list:
			self.hp -= 1
			if self.hp == 0:
				self.kill()


class Wall(pygame.sprite.Sprite):
	
	def __init__(self, x, y, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width,height])
		self.image.fill(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x

	def update(self):

		bullet_hit_list = pygame.sprite.spritecollide(self,Character.bullets,True)
		bullet_hit_list = pygame.sprite.spritecollide(self,AIPlayer.bullets,True)

class Bullet(pygame.sprite.Sprite):

	def __init__(self,player):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([5,5])
		self.image.fill(ORANGE)
                self.rect = self.image.get_rect()
		self.player = player
		self.dx = 0
		self.dy = 0
		self.rect.x = player.rect.x
		self.rect.y = player.rect.y
		self.dx += self.player.speedX
		self.dy += self.player.speedY
	
	def update(self):
		self.rect.x += 3*self.dx
		self.rect.y += 3*self.dy
		if self.rect.x < 0 or self.rect.y < 0:
			self.kill()
		if self.rect.x > screenSizeWidth or self.rect.y > screenSizeHeight:
			self.kill()
		if self.dx == 0 and self.dy == 0:
			self.kill()

class Coin(pygame.sprite.Sprite):

	def __init__(self,startpos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([10,10])
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		self.rect.x = startpos[0]
		self.rect.y = startpos[1]
		self.progress = 0

	def capture(self,player):
		if player.rect.x > screenSizeWidth*0.45 and player.rect.x < screenSizeWidth*0.55 and player.rect.y > screenSizeHeight*0.45 and player.rect.y < screenSizeHeight*0.55:
			if self.progress < 1:
				self.progress += 0.001
				pygame.draw.rect(screen, BLUE,pygame.Rect(screenSizeWidth*0.1,screenSizeHeight*0.1,100*self.progress,10))
				pygame.draw.rect(screen, RED,pygame.Rect(screenSizeWidth*0.1,screenSizeHeight*0.1,100,10),1)
			else:
				self.kill()
				self.progress = 0

class AIPlayer(pygame.sprite.Sprite):

	walls = None
	bullets = pygame.sprite.Group()

	def __init__(self,startpos = (710,250),starthp = 100):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([30,30])
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.x = startpos[0]
		self.rect.y = startpos[1]
		self.maxspeed = 2
		self.speedX = 0
		self.speedY = 0
		self.state = "neutral"

	def move(self,Coin,player):
		if self.state == "neutral":
			self.state = "chasecoin"
		if self.state == "chasecoin":
			if self.rect.x != Coin.rect.x or self.rect.y != Coin.rect.y:
				dx = Coin.rect.x - self.rect.x
				dy = Coin.rect.y - self.rect.y
				dist = math.hypot(dx, dy)
				dx = dx / dist
				dy = dy / dist
				self.speedX = dx * self.maxspeed
				self.speedY = dy * self.maxspeed

		if self.rect.x != player.rect.x or self.rect.y != player.rect.y:
				dx = player.rect.x - self.rect.x
				dy = player.rect.y - self.rect.y
				dist = math.hypot(dx,dy)
				if dist < 150:
					self.state = "chaseplayer"
					dx = dx / dist
					dy = dy / dist
					self.speedX = dx * self.maxspeed
					self.speedY = dy * self.maxspeed
					bullet = Bullet(self)
					self.bullets.add(bullet)

				else:
					self.state = "chasecoin"

	def update(self):
		self.rect.x += self.speedX
		block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
		for block in block_hit_list:
		# If we are moving right, set our right side to the left side of the item we hit
			if self.speedX > 0 :
				self.rect.right = block.rect.left
				self.rect.y += self.speedY*3.3
			else:
				self.rect.left = block.rect.right
				self.rect.y += self.speedY*3.3

		self.rect.y += self.speedY		
		block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
		for block in block_hit_list:
		# Reset our position based on the top/bottom of the object.
			if self.speedY > 0:
				self.rect.bottom = block.rect.top
				self.rect.x += self.speedX*3.3
			else:
				self.rect.top = block.rect.bottom
				self.rect.x += self.speedX*3.3

pygame.init()

## Variables
screenSizeWidth = 800
screenSizeHeight = 600
size = (screenSizeWidth,screenSizeHeight)
screen = pygame.display.set_mode(size)
gameName = pygame.display.set_caption("Chase!")
#clock = pygame.time.Clock()
#font = pygame.font.SysFont('Calibri',25,False,False)
score = 0
#textScore = font.render("Score: " + str(score),True,BLACK)
# List are generated and filled here
wall_list = pygame.sprite.Group()
all_sprite_list = pygame.sprite.Group()
#boarder walls
wall = Wall(0,0,5,screenSizeHeight)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall(5,0,screenSizeWidth-5,5)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall(5,screenSizeHeight-5,screenSizeWidth-5,5)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall(screenSizeWidth-5,5,5,screenSizeHeight-10)
wall_list.add(wall)
all_sprite_list.add(wall)
#left base walls
wall = Wall(5,screenSizeHeight*0.45,screenSizeWidth*0.05,5)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall(5,screenSizeHeight*0.55,screenSizeWidth*0.05,5)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall(5,screenSizeHeight*0.55,screenSizeWidth*0.05,5)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall(5+screenSizeWidth*0.05,screenSizeHeight*0.45,5,(screenSizeHeight*0.1)+5)
wall_list.add(wall)
all_sprite_list.add(wall)
#right base walls
wall = Wall((screenSizeWidth*0.95)-10,screenSizeHeight*0.55,5+screenSizeWidth*0.05,5)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall((screenSizeWidth*0.95)-10,screenSizeHeight*0.45,5+screenSizeWidth*0.05,5)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall((screenSizeWidth*0.95)-10,screenSizeHeight*0.45,5,(screenSizeHeight*0.1)+5)
wall_list.add(wall)
all_sprite_list.add(wall)
#coin walls
wall = Wall(screenSizeWidth*0.25,screenSizeHeight*0.25,screenSizeWidth*0.2125,5)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall(screenSizeWidth*0.5375,screenSizeHeight*0.25,screenSizeWidth*0.2125,5)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall(screenSizeWidth*0.25,screenSizeHeight*0.75,screenSizeWidth*0.2125,5)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall(screenSizeWidth*0.5375,screenSizeHeight*0.75,screenSizeWidth*0.2125,5)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall(screenSizeWidth*0.25,screenSizeHeight*0.25,5,screenSizeHeight*0.2)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall(screenSizeWidth*0.74375,screenSizeHeight*0.25,5,screenSizeHeight*0.2)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall(screenSizeWidth*0.25,screenSizeHeight*0.55,5,screenSizeHeight*0.2)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall(screenSizeWidth*0.74375,screenSizeHeight*0.55,5,screenSizeHeight*0.2)
wall_list.add(wall)
all_sprite_list.add(wall)
#players
you = Character((10,350),3,50,GREEN,100)
you.walls = wall_list
bullet_list_player = you.bullets
all_sprite_list.add(you)
#AI player 
aiplayer = AIPlayer()
aiplayer.walls = wall_list
bullet_list_ai = aiplayer.bullets
all_sprite_list.add(aiplayer)
#creeps
creep = Creep((screenSizeWidth*0.065,screenSizeHeight*0.498))
creep.walls = wall_list
creep.bullets = bullet_list_ai
all_sprite_list.add(creep)
#coin
coin = Coin((screenSizeWidth*0.5,screenSizeHeight*0.5))
all_sprite_list.add(coin)

#menuItems = ('Start','Options','Quit')
#gm = GameMenu(screen,menuItems,BLACK,WHITE)
#gm.run()

done = False
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True

	#game logic
	you.move()
	aiplayer.move(coin,you)
	creep.follow()
	all_sprite_list.update()
	bullet_list_player.update()
	bullet_list_ai.update()
	screen.fill(WHITE)

	#drawing code goes here
	coin.capture(you)
	coin.capture(aiplayer)
	all_sprite_list.draw(screen)
	bullet_list_player.draw(screen)
	bullet_list_ai.draw(screen)
#	screen.blit(textScore,[screenSizeWidth-100,10])

	pygame.display.flip()
	clock.tick(40)	

pygame.quit()
