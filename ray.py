import math
import pygame

# Todo:
# Different wall heights

################################

# Window screen size
windowWidth = 620
windowHeight = 500

# Set player starting position in map
StartingXCoordinate = 1.5
StartingYCoordinate = 3.5

# This is the size of the game screen INSIDE the window screen
screenWidth = windowWidth
screenHeight = windowHeight

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

# Get map tile
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
# main

def main():

  hfov = player.fov / 2
  distanceToPlane = (screenWidth/2) / tan(hfov)

  while update(): # loop until we quit

    ray = Rays(player.dir - hfov)
    
    # loop through all columns casting rays
    for x in range(0, screenWidth):
      
      # correct fisheye effect
      ray.distance *= cos(player.dir - ray.angle)
      
      # get wall height
      wallHeight = math.ceil(blockSize / ray.distance * distanceToPlane)
      
      # get block color
      color = (255,255,255)
      if ray.block == 2:
        color = (0,0,255)
      elif ray.block == 3:
        color = (0,255,0)
      elif ray.block == 4:
        color = (0,127,180)
      
      # Y position of where to start the wall
      screenYpos = screenHeight/1.75
      # draw column
      pygame.draw.line(screen, color, (x, screenYpos-(wallHeight/2)), (x, screenYpos+(wallHeight/2)))
      
      # Trace next ray
      ray.next()

################################
# Handle player

class Player():

  def __init__(self, playerXcoor, playerYcoor):
  
    ## set player starting attributes

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
  
  # Move player
  def update(self):
  
    keys = pygame.key.get_pressed()
    
    # turn player
    if keys[pygame.K_RIGHT]:
      self.dir += self.TurnSpeed
      if self.dir > 360:
        self.dir -= 360
    elif keys[pygame.K_LEFT]:
      self.dir -= self.TurnSpeed
      if self.dir < 0:
        self.dir += 360
    
    # create test position
    X_temp = self.XPos
    Y_temp = self.YPos
    
    if keys[pygame.K_UP]:
      X_temp += cos(self.dir) * self.WalkSpeed
      Y_temp -= sin(self.dir) * self.WalkSpeed
    elif keys[pygame.K_DOWN]:
      X_temp -= cos(self.dir) * self.WalkSpeed
      Y_temp += sin(self.dir) * self.WalkSpeed
    
    # if we would be in a wall don't put the player there
    if not MapTile(X_temp, self.YPos):
      self.XPos = X_temp

    if not MapTile(self.XPos, Y_temp):
      self.YPos = Y_temp
      

################################
# Handles all rays

class Rays:

  ## init (also cast the first ray)
  def __init__(self, startingAngle):
    
    if startingAngle < 0:
      startingAngle += 360
    
    self.angle = startingAngle
    
    # This is the distance to the wall the ray is touching
    self.distance = 0

    # This is the block the ray is touching
    self.block = 0
    
    self.Cast()
  
  ## Cast next ray
  def next(self):
    
    angleBetweenColumns = player.fov/screenWidth
    self.angle += angleBetweenColumns
    
    if self.angle > 360:
      self.angle -= 360 
      
    self.Cast() 
   
  ## Ray tracing routine
  def Cast(self):
    
    # Horizontal and vertical intersections are checked seperately
    # Remeber X increase to the right and Y increase DOWN *not* up
    
    # Setup for checking horizontal intersections
    if self.angle > 0 and self.angle < 180:
      HorzYpos = math.floor(player.YPos/blockSize) * blockSize - 1 # Y pos of ray
      HorzYinc = -blockSize # amount to increase Y pos by to get to next block
    else:
      HorzYpos = math.floor(player.YPos/blockSize) * blockSize + blockSize
      HorzYinc = blockSize
    
    HorzXpos = player.XPos + (player.YPos - HorzYpos)/tan(self.angle) # x pos of ray
    HorzXinc = (-HorzYinc) / tan(self.angle) # amount to increase X position by to get to next block
  
    # Vertical check
    if self.angle < 90 or self.angle > 270:
      VertXpos = math.floor(player.XPos/blockSize) * blockSize + blockSize
      VertXinc = blockSize
    else:
      VertXpos = math.floor(player.XPos/blockSize) * blockSize - 1
      VertXinc = -blockSize
    
    VertYpos = player.YPos + (player.XPos - VertXpos)*tan(self.angle)
    VertYinc = (-VertXinc) * tan(self.angle)
    
    ## Now we loop and check for contact with walls
    
    # record seperate distances and blocks hit for each intersections
    distanceX = 0
    distanceY = 0
    
    blockX = 0
    blockY = 0
    
    # Loop until both checks hit a wall
    while (blockX == 0) or (blockY == 0):
    
      if (blockX == 0):
        
        # Make sure the ray is within the map
        # alternative to try/except would be:
        # HorzX/blockSize * HorzY/blockSize < mapSize
        try:
          blockX = MapTile(HorzXpos, HorzYpos)
          if blockX: distanceX = math.fabs( (player.XPos-HorzXpos)/cos(self.angle) )
        except:
          blockX = 1
          distanceX = 9999
            
        HorzXpos += HorzXinc
        HorzYpos += HorzYinc
      
      # Stop if we already hit a wall on this intersection
      if (blockY == 0):
      
          try:
            blockY = MapTile(VertXpos, VertYpos)
            if blockY: distanceY = math.fabs( (player.XPos-VertXpos)/cos(self.angle) )
          except:
            blockY = 1
            distanceY = 9999
          
          VertXpos += VertXinc
          VertYpos += VertYinc
    
    # Use whichever wall is closer
    if distanceX < distanceY:
      self.distance = distanceX
      self.block = blockX
    else:
      self.distance = distanceY
      self.block = blockY
           
#
################################
# update screen

def update():

    player.update()
    pygame.display.flip()
    screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                return False
    # keep running
    return True

################################
# init

pygame.init()
pygame.display.set_caption("Raycaster")
screen = pygame.display.set_mode((windowWidth, windowHeight))

# create a player
player = Player(StartingXCoordinate, StartingYCoordinate)

main() # run main
pygame.quit()
