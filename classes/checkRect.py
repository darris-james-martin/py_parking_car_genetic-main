import math


def isCollision(npcCar, playCar):
    # print("npcCar",npcCar.rect, npcCar.angle%45, "playCar", playCar.rect,playCar.angle%45)
    nc_rect = npcCar.rect
    nc_rect.width = nc_rect.width * 0.65
    nc_rect.height = nc_rect.height * 0.65

    doCollide = nc_rect.colliderect(playCar.rect)
    # print("doCollide",doCollide)
    if doCollide:
        print("npcCar", npcCar.rect, npcCar.angle, "playCar", playCar.rect, playCar.angle)
        npcCar.x += playCar.speed * math.sin(math.radians(playCar.angle)) * 30
        npcCar.y += playCar.speed * math.cos(math.radians(-playCar.angle)) * 30
        print("CRASH!!!")
        return True


def isParked(ps_rect, car_rect):
    # print("ps_rect", ps_rect, "car_rect", car_rect)
    doParked = ps_rect.contains(car_rect)
    if doParked:
        print("Parked!!!")
        return True


def DistToSpot(rPlayCar, rParkSpot):
    print("playerCar, Parking Spot: ",rPlayCar,rParkSpot)
    nPlayerX = rPlayCar.x
    nPlayerY = rPlayCar.y
    nParkSpotX = rParkSpot.x
    nParkSpotY = rParkSpot.y

    nDist = math.sqrt((nPlayerX - nParkSpotX) ** 2 + (nPlayerY - nParkSpotY) ** 2)
    return nDist
