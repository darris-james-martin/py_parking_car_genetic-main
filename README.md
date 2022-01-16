This was a group project perform by James Martin and Bismarck Perez

# Presentation
Watch the presentation posted to my YouTube Page</br>
https://www.youtube.com/watch?v=NQYwW9HaEjA&ab_channel=frostbyte000jm

# Genetic Algorithm
Genetic Algorithm is a method to solve optimization problems through AI using natural selection. It does this through:</br>
	• Create a Random Population</br>
	• Test each member of the Population and give them a score. </br>
	• Randomly pair members of the population with other members of the population. </br>
	• Mutate random pairing in an attempt to improve the score.</br>
	• Run them through the test again. </br>
	• Keep going until desired outcome is reached or max number of generations are reached. </br>

# Project
When studying the genetic algorithm, the process felt random. After digging a little deeper into the algorithm, the beginning process was random but as it moved through generations it kept improving. We (Perez and Martin) wanted to explore improving the Genetic Algorithm. 
We want to replace reproducing with cloning. What this means is to adjust the results of the best parents instead of merging them with others. 
We also want to have a Fitness function make some corrections as we move along. 
The last adjustment is to pass down knowledge. Once a certain number of generations have progressed, we want to take the best answer and pass that to a new set of movements that will try and move further.

# Problem to Solve
The problem we are trying to solve is to have a car park itself using the Genetic Algorithm. There are better algorithms to solve this, but the reason we are using a car parking experiment is because we want to test a theory of passing down knowledge. Once the car has progressed the best it can to a location, the algorithm will grow a new population and continue to find a better direction from there.

## Changes
1) The fitness test will check if the object has moved out of bounds if it has it will reselect a direction to keep it in bounds. 
2) Instead of creating children we will randomly mutate movements that the original population made
3) After fitness test we will purge the population that fell under a certain amount and using the best answers repopulation to the population.
4) When the high score stops changing after a certain number of generations, we will pass on that knowledge to move the object further. 

## References used
https://www.geeksforgeeks.org/genetic-algorithms/ </br>
https://www.codingame.com/playgrounds/334/genetic-algorithms/history </br>
https://www.sciencedirect.com/topics/engineering/genetic-algorithm </br>


# Code
## Code for Genetic Algorithm
```python
import random, pygame, math

from classes.checkRect import DistToSpot
from classes.sprites import Sprite
from classes.checkRect import isParked

pygame.init()

# global variables
nPopSize = 1000
nPopKept = 50
nChildrenProduced = 5
nMoveCount = 100
nAddMoveCount = 100
nGenSize = 150
nAges = 3
nBurnout = 25
nTest = 1


# This will return a Score based on how well the car performed
def fitness(rPop, spriteParkingSpot):
    # move car - After each move check to see if inside square. If so cut remaining moves and send back correct answer.
    rMovesRevised = []
    spritePlayerCar = rPop[0]
    moves = rPop[1]

    # First check if OOB, if so correct, if not: move the car, see if it is parked, measure the distance.
    for i, move in enumerate(moves):
        # Turns out the car never goes out of bounds.
        bOOB = True
        while bOOB:
            nSpeed = move[0]
            nTurnVal = move[1]
            spritePlayerCar.speed = nSpeed
            spritePlayerCar.angle += nTurnVal

            # check if out of bounds
            testx = spritePlayerCar.x + spritePlayerCar.speed * math.sin(math.radians(spritePlayerCar.angle))
            testy = spritePlayerCar.y + spritePlayerCar.speed * math.cos(math.radians(-spritePlayerCar.angle))
            # print("testx:",testx,"testy:",testy)
            if (0 > testx > 800) or (0 > testy > 600):
                moves[i] = randomMove()
                print("Bounce!")
            else:
                spritePlayerCar.x += spritePlayerCar.speed * math.sin(math.radians(spritePlayerCar.angle))
                spritePlayerCar.y += spritePlayerCar.speed * math.cos(math.radians(-spritePlayerCar.angle))
                spritePlayerCar.draw()
                rMovesRevised.append(move)
                bParked = isParked(spriteParkingSpot.rect, spritePlayerCar.rect)
                if bParked:
                    return 100000, rMovesRevised
                bOOB = False

    nDist = DistToSpot(spritePlayerCar, spriteParkingSpot)

    return (1 / nDist), rMovesRevised


def randomMove():
    # The car can move forward, backward, left forward, left backward, right forward, right backward.
    rMoves = [(1.5, 0), (-1.5, 0), (1.5, 0.9), (1.5, -0.9), (-1.5, 0.9), (-1.5, -0.9)]

    tMove = random.choice(rMoves)
    # print(f"tMove: {tMove}")
    return tMove


def addPopulation(rPopStart, playerCar_pg):
    # create a bunch of random moves
    rPopulation = []
    # print("rPopulation at Start:",rPopulation)
    global nPopSize, nMoveCount, nAddMoveCount
    for _ in range(nPopSize):
        rCarMoves = rPopStart[:]
        if len(rCarMoves) > 0:
            nMoveCount = nAddMoveCount
        for _ in range(nMoveCount):
            rCarMoves.append(randomMove())

        spritePlayerCar = Sprite(playerCar_pg.pos, playerCar_pg.height, playerCar_pg.width, playerCar_pg.img)
        rPopulation.append([spritePlayerCar, rCarMoves])
    # print("rPopulation at End:", rPopulation)
    return rPopulation


# Creates population of Cars then sends them to the Genetic Algorithm
def createPop(rParkingSpot_pg, playerCar_pg, rNpcCar_pg):
    rSolution = []
    # This is so I can test a few times. This can take a while to run.
    for t in range(nTest):
        # Create new parking spot
        spriteParkingSpot = []

        # This will copy the starting pos of the car.
        for i, ps in enumerate(rParkingSpot_pg):
            if ps.bGoalSpot:
                spriteParkingSpot = Sprite(ps.pos, ps.height, ps.width, ps.img, True)

        # create a bunch of random moves
        rPopulation = []
        rPopulation = addPopulation(rPopulation, playerCar_pg)

        # Run this through the Genetic Algorithm
        rSolution = geneticAlgorithm(rPopulation, spriteParkingSpot, playerCar_pg)
    return rSolution


def geneticAlgorithm(rPopulation, spriteParkingSpot, playerCar_pg):
    # declarations
    global nGenSize, nAges
    bAfterFirst = False

    # If Ages is being used, this is to take what was before and move to the next step.
    for a in range(nAges):
        if bAfterFirst:
            rPopulation = addPopulation(rPopulation[0][1], playerCar_pg)
        else:
            bAfterFirst = True
        nHighScoreCount = 0
        nHighScore = 0

        for i in range(nGenSize):
            rRankedAnswers = []
            for pop in rPopulation:
                # print("pop",pop)
                nScore, rMovesRevised = fitness(pop, spriteParkingSpot)

                rRankedAnswers.append([nScore, rMovesRevised])
                # print("nScore:",nScore,"rMovesRevised:",rMovesRevised)

            rRankedAnswers.sort()
            rRankedAnswers.reverse()

            # if i == 0 or i == (nGenSize - 1) or nHighScoreCount == (nBurnout - 1):
            print(
                f"Best Score Era({a}) Generation ({i}) pop ({len(rRankedAnswers)}) size ({len(rRankedAnswers[0][1])}), idx ({nHighScoreCount}): ",
                rRankedAnswers[0])

            if rRankedAnswers[0][0] > 2:
                return rRankedAnswers[0][1]

            nHS = rRankedAnswers[0][0]
            if nHS == nHighScore:
                nHighScoreCount += 1
            else:
                nHighScoreCount = 0
                nHighScore = nHS

            if nHighScoreCount > nBurnout:
                break

            # grab the best parents
            rBestAnswers = rRankedAnswers[:nPopKept]

            # create Children
            rChildren = []
            spritePlayerCar = Sprite(playerCar_pg.pos, playerCar_pg.height, playerCar_pg.width, playerCar_pg.img)
            rChildren.append([spritePlayerCar, rBestAnswers[0][1]])
            for i in range(0, len(rBestAnswers), 2):
                for l in range(nChildrenProduced):
                    nMutate = random.randrange(a * nAddMoveCount, len(rBestAnswers[i][1]))  #switch on/off when you want producing children.
                    rChild = []
                    for j in range(0, len(rBestAnswers[i][1])):
                        # print(f"Steps: i:{i}, l: {l}, j:{j} mutate: {nMutate}")
                        # bMutate = random.randrange(0,25) == 0  #Switch on/off for random mutation vs producing children
                        nCoin = random.randrange(i, i + 2) # l  #switch formula for random mutation vs producing children
                        if j == nMutate: #bMutate:  #switch formula when you want mutation vs producing children.
                            tValue = randomMove()
                            # print(f"Mutated: i:{i}, l: {l}, j:{j} ")
                        else:
                            tValue = rBestAnswers[nCoin][1][j]
                        rChild.append(tValue)
                    spritePlayerCar = Sprite(playerCar_pg.pos, playerCar_pg.height, playerCar_pg.width,
                                             playerCar_pg.img)
                    rChildren.append([spritePlayerCar, rChild])

            rPopulation = rChildren
    return rPopulation[0][1]
```
 
## Code For Interface
``` python
import pygame, math

from classes.createBoard import createParkingSpots, createPlayerCar, createNPCCars
from classes.checkRect import isCollision, isParked
# from classes.geneticParking import createPop

# initialize game
from classes.geneticParking import createPop

pygame.init()
bRunning = True

# set Screen Size
nScreenW = 800
nScreenH = 600
screen = pygame.display.set_mode((nScreenW, nScreenH))

# Title and Icon
pygame.display.set_caption("Parking A Car")

# background
background = pygame.image.load('graphics/parking spot/parkingLot.png')

# Randoms


while bRunning:
    # Create Game Board
    rParkingSpot = createParkingSpots()
    playerCar = createPlayerCar()
    rNpcCar = createNPCCars(rParkingSpot)

    # declarations
    player_xpos_change = 0.0
    player_ypos_change = 0.0
    nTurn = 0
    nSpeed = 0
    clock = pygame.time.Clock()
    bGame = True
    bSolve = False
    

    # Temporary until we get a system that fills rStack
    #for i in range(1000):
     #   rStack.append((-1.5,-0.9))

    # Game Loop
    while bGame:

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bRunning = False
                bGame = False

            # key down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("pressed escape")
                    bRunning = False
                if event.key == pygame.K_UP:
                    print("pressed Up")
                    nSpeed = -playerCar.accel
                    # playerCar.speed += playerCar.accel
                if event.key == pygame.K_DOWN:
                    print("pressed Down")
                    nSpeed = playerCar.accel
                if event.key == pygame.K_LEFT:
                    print("pressed Left")
                    nTurn = playerCar.turn
                if event.key == pygame.K_RIGHT:
                    print("pressed Right")
                    nTurn = -playerCar.turn

            # key up
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    nTurn = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    nSpeed = 0
                if event.key == pygame.K_r:
                    bGame = False
                if event.key == pygame.K_s:
                     #send the GA the car, parking lot, and NPCs
                     #createPop(rParkingSpot,playerCar,rNpcCar)

                     bSolve = True
                if event.key == pygame.K_w:
                    rStack = createPop(rParkingSpot, playerCar, rNpcCar)
                    rStack.append((0,0))
                    rStack.reverse()
                    print("rStack:", rStack)
                    bSolve = True

        # move player car
        if bSolve and len(rStack)>0:
            stack = rStack.pop()
            # print('stack',stack)
            nSpeed = stack[0]
            nTurn = stack[1]
        playerCar.speed = nSpeed
        nTurnVal = 0
        if nSpeed != 0:
            nTurnVal = nTurn
        else:
            nTurnVal = 0
        playerCar.angle += nTurnVal
        playerCar.x += playerCar.speed * math.sin(math.radians(playerCar.angle))
        playerCar.y += playerCar.speed * math.cos(math.radians(-playerCar.angle))
        # print("playerCar.x",playerCar.x,"playerCar.y",playerCar.y)
        # print("speed", playerCar.speed, "angle", playerCar.angle)

        # Check for collision
        for nc in rNpcCar:
            bCrash = isCollision(nc, playerCar)
            #if bCrash:
                #bGame = False
        #print("playerCar", playerCar.rect, playerCar.angle, f"(x,y): ({playerCar.x},{playerCar.y})")


        # Check for Parked
        # print("Player Car - x:", playerCar.goal_x, "y:", playerCar.goal_y)
        # print("Player Car - x: ", playerCar.x, "y: ", playerCar.y, "rect: ", playerCar.rect, "surface: ", playerCar.surface, "angle:", playerCar.angle, "height:",playerCar.height,"width:",playerCar.width)

        for ps in rParkingSpot:
            # print("Parking Spot - x:", ps.x, "y: ", ps.y, "rect: ",ps.rect, "surface: ",ps.surface)
            bParked = isParked(ps.rect, playerCar.rect)
            #if bParked:
                #bGame = False

        # draw game
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        for ps in rParkingSpot:
            rotated, topleft = ps.draw()
            screen.blit(rotated, topleft)
        rotated, topleft = playerCar.draw()
        screen.blit(rotated, topleft)
        for nc in rNpcCar:
            rotated, topleft = nc.draw()
            screen.blit(rotated, topleft)
        # screen.blit(imgParkingSpot,(imgParkingSpot_xpos,imgParkingSpot_ypos))
        pygame.display.flip()
        clock.tick(60)

        # player_xpos = min(max(player_xpos + player_xpos_change, 0), nScreenW - playerCarImgW)
        # player_ypos = min(max(player_ypos + player_ypos_change, 0), nScreenH - playerCarImgH)
        # player_pos(player_xpos, player_ypos)

        # Update Game
        # pygame.display.update()

# End Game
pygame.quit()
```
