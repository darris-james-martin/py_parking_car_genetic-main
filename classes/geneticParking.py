import random

import pygame

from classes.checkRect import DistToSpot
from classes.createBoard import createParkingSpots, createPlayerCar, createNPCCars

# global variables
nPopSize = 1
nParents = 1
nGenSize = 1


# This will return a Score based on how well the car performed
def fitness(moves, rParkingSpot, playerCar, rNpcCar):
    # Score will be based on 0 - 1, score increases the closer it gets to
    rGoalSpot = []
    for ps in rParkingSpot:
        print("ps:",ps.bGoalSpot)
        if ps.bGoalSpot:
            rGoalSpot = ps
            break

    nDist = DistToSpot(playerCar, rGoalSpot)
    print(nDist)


# Creates population of Cars then sends them to the Genetic Algorithm
def createPop(rParkingSpot, playerCar, rNpcCar):
    # create a bunch of random moves
    rPopulation = []
    global nPopSize
    for _ in range(nPopSize):
        rCarMoves = []
        for _ in range(nParents):
            nMove = random.randrange(0, 3)  # 0 - F, 1 - R, 2 - L, 3 - R
            nTurnCupple = random.randrange(0, 1)  # 0 - F, 1 - R

            rMoves = [(1.5, 0), (-1.5, 0), (1.5, 0.9), (1.5, -0.9), (-1.5, 0.9), (-1.5, -0.9)]

            if nMove == 0:
                rCarMoves.append(rMoves[0])
            elif nMove == 1:
                rCarMoves.append(rMoves[1])
            elif nMove == 2:
                if nTurnCupple == 0:
                    rCarMoves.append(rMoves[2])
                else:
                    rCarMoves.append(rMoves[4])
            elif nMove == 3:
                if nTurnCupple == 0:
                    rCarMoves.append(rMoves[3])
                else:
                    rCarMoves.append(rMoves[5])

            rPopulation.append(rCarMoves)
    # print("rPopulation:", rPopulation)

    # print(rQueenPop)
    return geneticAlgorithm(rPopulation, rParkingSpot, playerCar, rNpcCar)


def geneticAlgorithm(rPopulation, rParkingSpot, playerCar, rNpcCar):
    global nGenSize
    nTotalRun = nGenSize
    for i in range(nTotalRun):
        rRankedAnswers = []
        for moves in rPopulation:
            # print("moves",moves)
            nScore = fitness(moves, rParkingSpot, playerCar, rNpcCar)
            print("Score:", nScore)


# createPop(0, 0, 0)
# pygame.init()
# rParkingSpot = createParkingSpots()
# playerCar = createPlayerCar()
# rNpcCar = createNPCCars(rParkingSpot)
#
# fitness(0, rParkingSpot, playerCar, rNpcCar)
