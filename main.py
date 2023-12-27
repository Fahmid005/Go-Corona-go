import pygame
import random

import math

import time
import sys

from pygame import mixer

# Initialize pygame 
pygame.init()
# Title
pygame.display.set_caption("GO CORONA GO")
icon = pygame.image.load("img/ufo.png")
pygame.display.set_icon(icon)

# Console window
WIDTH = 800
HEIGHT =600
console = pygame.display.set_mode( (WIDTH,HEIGHT), pygame.RESIZABLE )
FPS = 100
clock = pygame.time.Clock()
score_val  = 0
#player isAlive()
isAlive = True


# BG sound
mixer.music.load("sounds/background.wav")
mixer.music.set_volume(0.4)
mixer.music.play(-1)



# Score design

font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10
def showScore(x,y):
	score = font.render("Score: " + str(score_val),True, (0,255,0) )
	console.blit(score, (x,y))

# GAME OVER design 
def game_over():
	GO_font = pygame.font.Font("freesansbold.ttf",64)
	game_over_txt = GO_font.render("GAME OVER" , True, (255,0,200) )
	console.blit( game_over_txt, (200,250) )
	test = GO_font.render("COVID-19 WON",True,(255,0,100))
	console.blit( test, (200,320) )

# WIN design 
def win():
	win_font = pygame.font.Font("freesansbold.ttf",80)
	win_txt = win_font.render("YOU WIN", True, (0,255,50))
	console.blit(win_txt, (250,320))






#Player Design
player_img = pygame.image.load("img/space-ship.png")
xPos = 370
yPos = 480
xPos_change, yPos_change = 0 , 0

def player(x,y):
	console.blit(player_img, (x,y))

# Enemy design
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = [] 
enemyY_change = []
enemy_count = random.randint(8,15)

for i in range(enemy_count):
	enemy_img.append(pygame.image.load("img/virus.png"))
	enemyX.append(random.randint(0,735))
	enemyY.append(random.randint(30,150))
	enemyX_change.append(5)
	enemyY_change.append(40)

def enemy(x, y, i):
	console.blit(enemy_img[i], (x,y))


#Background design
bg = pygame.image.load("img/background.jpg")

def BG():
	console.blit(bg, (0,0))

# Shooter design
shooter_img = pygame.image.load("img/drop.png")
shooterX = 0
shooterY = 480
shooterX_change = 0
shooterY_change = 5
shooter_speed =   clock.tick(30)
resistance = -3
# "ready" state ----> no bullets on screen
# "fire" state ---->  bullet fired already 
shooter_state = "ready"

def shoot(x,y):
	global shooter_state
	shooter_state = "fire"
	console.blit(shooter_img,(x + 16 , y ))

#Calculate  Collision distance  -----> bool func----> shooter and virus
def isCollision(enemyX, enemyY, shooterX, shooterY):
	dist = math.sqrt( ((enemyX-shooterX)**2) + ((enemyY-shooterY)**2) )

	if dist < 27:
		return True
	else:
		return False





#Game loop
run = True
while run:
	# RGB console fill (Red,Green,Blue)
	console.fill((0,0,10))

	BG()

	clock.tick(FPS)
	for event in pygame.event.get():
		#wait = pygame.mouse.get_pressed()
		#pygame.mouse.set_visible(True)

		if event.type == pygame.QUIT:
			run = False
		# Player movements ---> keyboard inputs
		# Key pressed events
		# W ---> Up | S ---> Down | A ---> Left | D ---> Right | 
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				xPos_change = -2 
			if event.key == pygame.K_d:
				xPos_change = 2
			#if event.key == pygame.K_w:
				#yPos_change = -2
			#if event.key == pygame.K_s:
				#yPos_change = 2
			if event.key == pygame.K_ESCAPE:
				run = False
			if event.key == pygame.K_SPACE:
				if shooter_state == "ready":
					# Shooter sound
					shooter_sound = mixer.Sound("sounds/laser.wav")
					shooter_sound.set_volume(0.7)
					shooter_sound.play()

					shooterX = xPos
					shoot(xPos,shooterY)

			
				
	 			
		# Key released events
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_a or  event.key == pygame.K_d:
				xPos_change = 0
			#if event.key == pygame.K_w or  event.key == pygame.K_s:
				#yPos_change = 0

	xPos += xPos_change
	yPos += yPos_change
	#----------player boundary restriction-----------------
	# x axis Boundary
	if xPos <= 0:
		xPos = 0
	elif xPos >= (800-64):
		xPos =  (800-64)

	#y axis Bouundary 
	if yPos <=0:
		yPos = 0
	elif yPos >= (600-64):
		yPos = 600-64

	#--------------Enemy movement------------
	for i in range(enemy_count):
		#!!!!!!GAME OVER!!!!!!
		if enemyY[i] >= 440:
			for j in range(enemy_count):
				enemyY[j] = 900
			game_over()
			isAlive = False
			break


		enemyX[i] += enemyX_change[i]
		if enemyX[i] <= 0:
			enemyX_change[i] = 3.5
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= (800-64):
			enemyX_change[i] = -3.5
			enemyY[i] += enemyY_change[i]

		if enemyY[i] >= 600-64:
			enemyY[i] = 0
		# Collision handle
		col = isCollision(enemyX[i],enemyY[i],shooterX,shooterY)
		if col:
			# Explosion sound
			explosion_sound = mixer.Sound("sounds/explosion.wav")
			explosion_sound.set_volume(0.4)
			explosion_sound.play()

			# Explosion img
			explosion_img = pygame.image.load("img/blast.png")
			console.blit(explosion_img, (shooterX,shooterY))
			#clock.tick(500)

			shooterY = yPos 
			shooter_state = "ready"
			# if collide---> Add +1 score value
			score_val += 1
			# If collide decrease enemy count by -1
			enemy_count -= 1
			#Re-Spawn enemy
			#clock.tick(75) 
			#enemyX[i] = random.randint(0,750)
			#enemyY[i] = random.randint(30,150)
		
		#display enemy at every new instant
		enemy(enemyX[i] , enemyY[i] , i)

	# Kill all enemy---> WIN
	if enemy_count == 0:
		win()


	'''if enemyY >= 600-64:
		enemyY = 0'''

	#------ Bullet movement----------
	if shooter_state == "fire":
		shoot(shooterX,shooterY)
		shooterY -= shooterY_change + shooter_speed*0.01
		#shooterY -= resistance 

	#after on bullet fired ---> reset bullut position and state 
	if shooterY <= 0:
		shooterY = yPos   
		shooter_state = "ready"

	 


	#display player at every new instant 
	player(xPos,yPos)	

	showScore(textX , textY)
	#keep console updated
	pygame.display.flip()

pygame.quit()