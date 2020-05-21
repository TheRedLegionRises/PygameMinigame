import pygame, sys
from random import randint
from pygame.locals import *
from tkinter import *
from tkinter import messagebox

#Shows instructions of the game
Tk().wm_withdraw() #to hide the main window
messagebox.showinfo("Game Introduction", "Goal: \nSurvive as long as possible \n\nInstructions: \nUse the WASD keys to control your character, which is the green square. Move around in order to avoid the white squares, which are obstacles. You start with 3 lives, and if you hit a white square, you lose a life. After hitting a white square, your character will turn yellow, which indicates that it is invincible during that time. \n\nPoints: \nYou gain points just by surviving. You can also hit the red squares to get bonus points, and if you get 10 red squares, you gain an extra life. See how high you can score without dying. \n\nPress OK to start the game.")

GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

#Functions that detect if objects have collided
def detectCollision(object1, object2):
    for a, b in [(object1, object2), (object2, object1)]:
        if ((isPointInsideRect(a.left, a.top, b)) or (isPointInsideRect(a.left, a.bottom, b)) or (isPointInsideRect(a.right, a.top, b)) or (isPointInsideRect(a.right, a.bottom, b))):
            return True

def isPointInsideRect(xcoordinate, ycoordinate, object):
    if (xcoordinate > object.left) and (xcoordinate < object.right) and (ycoordinate > object.top) and (ycoordinate < object.bottom):
        return True
    
    else:
        return False    

def gameOver():
    messagebox.showinfo('Game Over!', finalScore + "\n\nPress OK to quit the game")

pygame.init()
mainClock = pygame.time.Clock()

windowHeight = 600
windowLength = 600

size = (windowHeight, windowLength)
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Game')

player = pygame.Rect(280, 500, 30, 30)

MOVESPEED = 10
OBJECTMOVESPEED = 5

moveUporDown = False
moveLeftorRight = False

numberOfObjects = 0
time = 0
spawnTime = 30
objectSize = 20
listOfFoods = []
obstacles = []
score = 0
lives = 3
invincible = 10
extraLives = 0

#spawns initial obstacles and food
for i in range(1):
    listOfFoods.append(pygame.Rect(randint(0, windowLength - objectSize), 0, objectSize, objectSize))

for i in range(5):
    obstacles.append(pygame.Rect(randint(0, windowLength - objectSize), 0, objectSize, objectSize))

#loop
while True:
    for event in pygame.event.get():
        #If user manually quits
         if event.type == QUIT:
             pygame.quit()
             sys.exit()
             
         #Movement Keys
         if event.type == KEYDOWN:
             if event.key == ord('a') or event.key == ord("d"):
                 if event.key == ord('a'):
                     moveLeftorRight = 1
                 else:
                     moveLeftorRight = 2

             if event.key == ord('w') or event.key == ord("s"):
                 if event.key == ord("w"):
                     moveUporDown = 1
                 else:
                     moveUporDown = 2
         
         if event.type == KEYUP:
             if event.key == ord('a') or event.key == ord("d"):
                    moveLeftorRight = False

             if event.key == ord('w') or event.key == ord("s"):
                    moveUporDown = False
    
    #As time passes, score increases
    time += 1
    score += 10
    
    #Spawntime for obstacles
    if ((time % 6) == 0):
        obstacles.append(pygame.Rect(randint(0, windowLength), 0, objectSize, objectSize))
    
    #Spawntime for "food"
    if time >= spawnTime:
        time = 0
        listOfFoods.append(pygame.Rect(randint(0, windowLength), 0, objectSize, objectSize))
    
    #Fills background
    screen.fill(BLACK)
    
    #Moves the player
    if moveUporDown == 2 and player.bottom < windowHeight:
        player.top += MOVESPEED

    if moveUporDown == 1 and player.top > 0:
        player.top -= MOVESPEED

    if moveLeftorRight == 1 and player.left > 0:
        player.left -= MOVESPEED

    if moveLeftorRight == 2 and player.right < windowLength:
         player.right += MOVESPEED
    
    #Final Score
    finalScore = "Your Final Score: " + str(score)
    
    for dangers in obstacles[:]:
        #If 10 red squares are eaten, 1up
        if (extraLives == 10):
            extraLives = 0
            lives += 1
        if detectCollision(player, dangers):
            #if you still have lives left
            if (lives != 0):
                #if you are invincible and hit it, remove the obstacle
                if invincible > 0:
                    obstacles.remove(dangers)
                #if you aren't, remove 1 life and become invincible for a few seconds
                else:
                    lives -= 1
                    invincible = 50
                    
            #if you have no lives left, end the game
            else:
                gameOver()
                pygame.quit()
                sys.exit()
        #makes objects move
        dangers.top += OBJECTMOVESPEED
    
    #duration of invincibility goes down
    invincible -= 1
            
    #Colour depending if player is invincible or not
    if invincible > 0:
        pygame.draw.rect(screen, YELLOW, player)
    else:
        pygame.draw.rect(screen, GREEN, player)
    
    #If player gets a red square, add one to extraLives counter, where if it reaches ten then player gets a 1up
    #Also increases score by 1000
    for object in listOfFoods[:]:
        if detectCollision(player, object):
            listOfFoods.remove(object)
            score += 100
            extraLives += 1
        #Makes it move
        object.top += OBJECTMOVESPEED
    
    #Shows score on the screen
    font = pygame.font.SysFont("ComicSans", 40)
    scoreText = font.render("Score = " + str(score), 1, WHITE)
    screen.blit(scoreText, (0, 0))
    
    #Shows number of lives on the screen
    numberOfLives = font.render("Lives: " + str(lives), 2, WHITE)
    screen.blit(numberOfLives, (windowLength - 110, 0))
    
    #Draws the obstacles and food
    for i in range(len(listOfFoods)):
        pygame.draw.rect(screen, RED, listOfFoods[i])
        
    for i in range(len(obstacles)):
        pygame.draw.rect(screen, WHITE, obstacles[i])
        
    pygame.display.update()
    mainClock.tick(60)