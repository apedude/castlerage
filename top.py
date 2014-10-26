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
	name = "fighter"
	speedX = 0
	speedY = 0
	maxHitPoints = 100
	currentHitPoints = 100
	maxSpeed = 0
	armor = 0
	walls = None
	
	def __init__(self,x,y,maxSpeed,size,color):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([size,size])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		self.maxSpeed = maxSpeed
		self.size = size
		self.color = color

	def move(self):
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
		
	def propagateL(self):
			self.rect.x -= self.maxSpeed

	def draw(self,screen):
		pygame.draw.rect(screen,self.color,[self.rect.x,self.rect.y,self.size,self.size])

	def collide(self,Character):
		if self.rect.right > Character.rect.left and self.rect.left < Character.rect.left and self.rect.top < Character.rect.top and self.rect.bottom > Character.rect.top:
			return True
		return False

	def follow(self, player):
		dx = player.rect.x - self.rect.x
		dy = player.rect.y - self.rect.y
	  	dist = math.hypot(dx, dy)
	  	dx = dx / dist
	  	dy = dy / dist
	  	self.rect.x += dx * self.maxSpeed
        	self.rect.y += dy * self.maxSpeed

	def update(self):
		you.rect.x += you.speedX
		block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
		for block in block_hit_list:
		# If we are moving right, set our right side to the left side of the item we hit
			if self.speedX > 0:
				self.rect.right = block.rect.left
			else:
				self.rect.left = block.rect.right
		# Check and see if we hit anything
		you.rect.y += you.speedY
		block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
		for block in block_hit_list:
		# Reset our position based on the top/bottom of the object.
			if self.speedY > 0:
				self.rect.bottom = block.rect.top
			else:
				self.rect.top = block.rect.bottom

class Wall(pygame.sprite.Sprite):
	
	def __init__(self, x, y, width, height):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface([width,height])
		self.image.fill(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x

pygame.init()

# Variables
size = (700,500)
screen = pygame.display.set_mode(size)
gameName = pygame.display.set_caption("Chase!")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Calibri',25,False,False)
score = 0
textScore = font.render("Score: " + str(score),True,BLACK)
# new code
wall_list = pygame.sprite.Group()
all_sprite_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
wall = Wall(0,0,10,500)
wall_list.add(wall)
all_sprite_list.add(wall)
wall = Wall(10,0,690,10)
wall_list.add(wall)
all_sprite_list.add(wall)
you = Character(10,350,3,50,GREEN)
you.walls = wall_list
all_sprite_list.add(you)
runner = Character(random.randrange(-10,0),random.randrange(0,490),2,10,BLUE)
bullet = Character(700,random.randrange(0,495),5,5,RED)
bullet_list.add(bullet)
bullet = Character(700,random.randrange(0,495),5,5,RED)
bullet_list.add(bullet)


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
	for bullet in bullet_list:
		if bullet.rect.x < 699 or bullet.rect.x > -5:
			bullet.propagateL()
		if bullet.rect.x < -5:
			bullet_list.remove(bullet)
			bullet = Character(700,random.randrange(0,495),5,5,RED)
			bullet_list.add(bullet)
		if you.collide(bullet):
			score += 1
			textScore = font.render("Score: " + str(score),True,BLACK)

	if you.rect.x != runner.rect.x and you.rect.y != runner.rect.y:
		runner.follow(you)

	all_sprite_list.update()
	screen.fill(WHITE)

	#drawing code goes here
	all_sprite_list.draw(screen)
	bullet_list.draw(screen)
#	you.draw(screen)
	runner.draw(screen)
#	bullet_1.draw(screen)
	screen.blit(textScore,[600,10])

	if score >= 100:
		screen.fill(BLACK)
		textScore = font.render("GAME OVER",True,WHITE)
		screen.blit(textScore,[315,225])

	pygame.display.flip()
	clock.tick(60)	

pygame.quit()
