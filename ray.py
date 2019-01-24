import math
import pygame

# Todo:
# Combined ray intersection functions
# Different wall heights

################################

# Window screen size
screen = pygame.display.set_mode((520, 400))

# Set player starting position in map
StartingXCoordinate = 1.5
StartingYCoordinate = 3.5

# This is the size of the game screen INSIDE the window screen
screenWidth = 520
screenHeight = 400

################################
# Map

# Make sure map has equal number of columns
map = [
 [1,1,2,1,1,1,2,1,1],
 [1,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,4,0,0,1],
 [1,0,4,4,4,4,0,0,1],
 [1,0,0,0,0,4,0,0,3],
 [1,0,0,0,0,4,0,0,1],
 [1,1,2,1,1,1,2,1,1]
]

################################

mapHeight = len(map)
mapWidth = len(map[0])
mapSize = mapHeight*mapWidth

blockSize = 64

def MapTile(X, Y): 
  return map[ math.floor(Y/blockSize) ] [ math.floor(X/blockSize) ]
  
################################

def sin(angle):
  angle += 0.00001
  return math.sin( math.radians(angle) )
  
def cos(angle):
  angle += 0.00001
  return math.cos( math.radians(angle) )
  
def tan(angle):
  angle += 0.00001
  return math.tan( math.radians(angle) )


################################
# Player attributes

class Player():

  def __init__(self, playerXcoor, playerYcoor):

    # 0-63 is first block
    # 64-128 is second block etc.

    self.XPos = blockSize*playerXcoor
    self.YPos = blockSize*playerYcoor

    # X increase right & decreases left
    # Y increases DOWN & decreases UP
    # Degrees is normal
    
    self.dir = 275
    
    self.WalkSpeed = 2
    self.TurnSpeed = 0.5
    
    self.fov = 60
    
  def update(self):
  
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_RIGHT]:
      self.dir += self.TurnSpeed
      if self.dir > 360:
        self.dir -= 360
    elif keys[pygame.K_LEFT]:
      self.dir -= self.TurnSpeed
      if self.dir < 0:
        self.dir += 360
    
    X_temp = self.XPos
    Y_temp = self.YPos
    
    if keys[pygame.K_UP]:
      X_temp += cos(self.dir) * self.WalkSpeed
      Y_temp -= sin(self.dir) * self.WalkSpeed
    elif keys[pygame.K_DOWN]:
      X_temp -= cos(self.dir) * self.WalkSpeed
      Y_temp += sin(self.dir) * self.WalkSpeed
    
    if MapTile(X_temp, self.YPos) == 0:
      self.XPos = X_temp

    if MapTile(self.XPos, Y_temp) == 0:
      self.YPos = Y_temp
      


################################
#

def CheckHorz(rayAngle):
    
  if rayAngle > 0 and rayAngle < 180:
    HorzY = math.floor(player.YPos/blockSize) * blockSize - 1
    Ya = -blockSize
  else:
    HorzY = math.floor(player.YPos/blockSize) * blockSize + blockSize
    Ya = blockSize
  
  HorzX = player.XPos + (player.YPos - HorzY)/tan(rayAngle)
  
  Xa = (-Ya) / tan(rayAngle)
  
  while True:
    
    # alternative to try/except would be:
    # HorzX/blockSize * HorzY/blockSize < mapSize
    try:
      # Make sure the ray is within the map
      tile = MapTile(HorzX, HorzY)
    except:
      return 9999, 0
    
    if (tile != 0):
      return math.fabs( (player.XPos-HorzX)/cos(rayAngle) ), tile
        
    HorzX += Xa
    HorzY += Ya
    

def CheckVert(rayAngle):
  
  # Remeber X increase to the right and Y increase DOWN *not* up
  if rayAngle < 90 or rayAngle > 270:
    VertX = math.floor(player.XPos/blockSize) * blockSize + blockSize
    Xa = blockSize
  else:
    VertX = math.floor(player.XPos/blockSize) * blockSize - 1
    Xa = -blockSize
  
  VertY = player.YPos + (player.XPos - VertX)*tan(rayAngle)
  Ya = (-Xa) * tan(rayAngle)  # note: this is fucking stupid how Y decrease as we go up. Change this in the future
  
  while True:
    
    try:
      tile = MapTile(VertX, VertY)
    except:
      return 9999, 0
    
    if (tile != 0):
      return math.fabs( (player.XPos-VertX)/cos(rayAngle) ), tile
    
    VertX += Xa
    VertY += Ya
    
def TraceRay(rayAngle):

  distanceX, blockX = CheckHorz(rayAngle)
  distanceY, blockY = CheckVert(rayAngle)
  
  if distanceX < distanceY:
    return distanceX, blockX
  else:
    return distanceY, blockY
  
        
#
################################

pygame.init()
pygame.display.set_caption("Raycaster")

################################
# main
 
player = Player(StartingXCoordinate, StartingYCoordinate)

hfov = player.fov / 2
distanceToPlane = (screenWidth/2) / tan(hfov)
angleBetweenColumns = player.fov/screenWidth

done = False
while not done:

  rayAngle = player.dir - hfov
  if rayAngle < 0:
    rayAngle += 360
  
  for x in range(0, screenWidth):
     
    distance, block = TraceRay(rayAngle)
    
    # correct fisheye effect
    distance *= cos(player.dir - rayAngle)
    wallHeight = math.ceil(blockSize / distance * distanceToPlane)
    
    color = (255,255,255)
    if block == 2:
      color = (0,0,255)
    elif block == 3:
      color = (0,255,0)
    elif block == 4:
      color = (0,127,180)
    
    # Y position of where to start the wall
    screenYpos = screenHeight/1.75
    
    pygame.draw.line(screen, color, (x, screenYpos-(wallHeight/2)), (x, screenYpos+(wallHeight/2)))
    
    rayAngle += angleBetweenColumns
    if rayAngle > 360:
      rayAngle -= 360    
  
  
  player.update()
  pygame.display.flip()
  screen.fill((0,0,0))
  
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
              done = True
            

################################

pygame.quit()
