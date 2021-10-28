import pygame, random

from classes.sprites import Sprite


def createParkingSpots():
    # Create Parking Spots
    rParkingSpotImg = pygame.image.load('graphics/parking spot/parkingSpot.png')
    nParkingSpotW = 95
    nParkingSpotH = 105

    rParkSpot_pos = [
        (8, 50, 0), (98, 50, 0), (188, 50, 0), (278, 50, 0), (368, 50, 0), (458, 50, 0), (548, 50, 0), (638, 50, 0),
        # Right Side Right
        # (652,150,-90), (652,240,-90), (652,330,-90),
        # Right Side Left
        # (405, 240, 90), (405, 330, 90), (405, 420, 90),
        # Left Side Right
        # (210,240,-90), (210,330,-90), (210,420,-90),
        # Left Side Left
        (5, 240, 90), (5, 330, 90), (5, 420, 90)
    ]

    nAvailParking = random.randrange(0, len(rParkSpot_pos) - 1)

    rParkingSpot = []
    for i, ps_pos in enumerate(rParkSpot_pos):
        # find Goal Spot
        bGoalSpot = False
        if i == nAvailParking:
            bGoalSpot = True

        rParkingSpot.append(Sprite(ps_pos, nParkingSpotH, nParkingSpotW, rParkingSpotImg, bGoalSpot))

    return rParkingSpot


def createPlayerCar():
    # Create Main Car
    playerCarImg = pygame.image.load('graphics/cars/car1.png')
    playerCarImgW = 60
    playerCarImgH = 100
    playerRandom_PosX = random.randrange(513, 588)
    player_pos = (playerRandom_PosX, 500, 0)
    playerCar = Sprite(player_pos, playerCarImgH, playerCarImgW, playerCarImg)

    return playerCar


def createNPCCars(rParkingSpot):
    # Create NPC1 Car
    rnpcCarImg = [pygame.image.load('graphics/cars/car2.png'), pygame.image.load('graphics/cars/car3.png')]
    npcCarImgW = 60
    npcCarImgH = 100

    npc_pos = []
    for i, ps in enumerate(rParkingSpot):
        # print("i:", i, "ps", ps, "ps.pos", ps.pos, "ps.pos[0]", ps.pos[0])
        pos = (ps.pos[0] + random.randrange(5, 30), ps.pos[1], ps.pos[2])
        # ps.pos[0] += random.randrange(15,20)
        if not rParkingSpot[i].bGoalSpot:
            npc_pos.append(pos)

    rNpcCar = []
    for i, n_pos in enumerate(npc_pos):
        rNpcCar.append(Sprite(n_pos, npcCarImgH, npcCarImgW, rnpcCarImg[i % 2]))

    return rNpcCar
