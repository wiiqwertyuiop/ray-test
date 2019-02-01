import math
import pygame

windowWidth = 500
windowHeight = 420

################################

map = [
 [1,1,2,1,1,2,1,1,1],
 [1,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,4,0,0,1],
 [1,0,4,4,4,3,0,0,1],
 [1,0,0,0,0,4,0,0,3],
 [1,0,0,0,0,4,0,0,1],
 [1,1,2,1,1,1,2,1,1]
]

hmap = [
 [1,1,2,1,-0.1,3,0.05,1,1],
 [1,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,7,0,0,1],
 [1,0,0.5,1,3,2,0,0,1],
 [1,0,0,0,0,1,0,0,5],
 [1,0,0,0,0,2,0,0,1],
 [1,1,2,1,1,1,2,1,1]
]

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
  
def main(screen):
  
  screenYpos = screenHeight/2
  
  while event_loop():
    
    for x in range(0, screenWidth):
    
      cameraX = 2 * x / screenWidth - 1
      rayDirX = player.dirX + player.planeX * cameraX
      rayDirY = player.dirY + player.planeY * cameraX
      
      mapX = int(player.Xpos)
      mapY = int(player.Ypos)
      
      sideDistX = 0
      sideDistY = 0
      
      deltaDistX = math.fabs(1 / (rayDirX + 0.00001) )
      deltaDistY = math.fabs(1 / (rayDirY + 0.00001) )
      
      stepX = 0
      stepY = 0

      # calculate step and initial sideDist
      if (rayDirX < 0):
        stepX = -1
        sideDistX = (player.Xpos - mapX) * deltaDistX
      else:
        stepX = 1
        sideDistX = (mapX + 1.0 - player.Xpos) * deltaDistX
      
      if (rayDirY < 0):
        stepY = -1
        sideDistY = (player.Ypos - mapY) * deltaDistY
      else:
        stepY = 1
        sideDistY = (mapY + 1.0 - player.Ypos) * deltaDistY
      
      tallestH = None
      
      # Loop through map
      while True:
      
        if (sideDistX < sideDistY):
          sideDistX += deltaDistX
          mapX += stepX
          side = 0
        else:
          sideDistY += deltaDistY
          mapY += stepY
          side = 1
        
        # If we go past the map stop looping
        if (mapY < 0 or mapX < 0): break
        try: hit = map[mapY][mapX]
        except: break
        if not hit: continue # if we have not hit anything loop until we do

        # Calculate distance projected on camera direction (Euclidean distance will give fisheye effect!)
        if (side == 0): perpWallDist = (mapX - player.Xpos + (1 - stepX) / 2) / (rayDirX+ 0.00001)
        else:           perpWallDist = (mapY - player.Ypos + (1 - stepY) / 2) / (rayDirY+ 0.00001)
        
        # use wall distance to calculate lighting
        lighting = perpWallDist
        lighting -= 3 # this is when to start darkening
        if (lighting < 0): lighting = 0
        lighting /= 0.4 # this is how fast to start changing
        lighting *= 15 # this is by how much to change it
        
        c1 = (255 - lighting)
        if (c1 <= 69): break # If the wall is too far away don't even bother drawing it
        c2 = c1
        c3 = c1
        
        # Calculate height of line to draw on screen
        lineHeight = int(screenHeight / (perpWallDist+0.00001))/2
        
        # calculate top pixel for column
        scale = hmap[mapY][mapX]
        drawStart = int(screenYpos - (lineHeight)*scale)    
        if(drawStart < 0): drawStart = 0
        
        if (tallestH != None): # if we have a record of a tallest wall it means we hit a wall behind that one
          if(drawStart >= tallestH): continue # if you can't see this wall behind the wall in front of it, then don't bother drawing it
          drawEnd = tallestH # if we can see this wall, then set the end pixel to the pixel above the wall in front of us
        else:               
          # calculate last pixel in column
          drawEnd = int(screenYpos + lineHeight)
          if(drawEnd >= screenHeight): drawEnd = screenHeight
          
        tallestH = drawStart # remeber the tallest height
        
        # do different colored walls
        if(hit == 2): c1 = 0; c2 = 0
        if(hit == 3): c2 = 0
        if(hit == 4): c3 = 0; c1 = 0        
        if(side == 0): c1 /= 1.05; c2 /= 1.05; c3 /= 1.05 # darken side of block
        
        # finally the draw line
        color = (int(c1), int(c2), int(c3))
        pygame.draw.line(screen, color, (x, drawStart), (x, drawEnd))
        
        # If we drew a column with the size of the whole screen height stop looping
        if (drawStart == 0): break
        
    # update screen
    player.update()
    pygame.display.flip()
    screen.fill((0,0,0))
    

# Event loop
def event_loop():
  
  for event in pygame.event.get():
    if (event.type == pygame.QUIT): 
      return False            
  return True


################################
# Handle player

class Player():

  def __init__(self):
  
    # set player starting attributes
    self.Xpos = 2
    self.Ypos = 2
    
    self.dirX = -1
    self.dirY = 0
    
    self.planeX = 0
    self.planeY = 0.66
    
    self.WalkSpeed = 0.01
    self.TurnSpeed = 0.3
  
  # Move player
  def update(self):
  
    keys = pygame.key.get_pressed()

    # turn player
    if keys[pygame.K_RIGHT]:
    
      # both camera direction and camera plane must be rotated
      oldDirX = self.dirX
      self.dirX = self.dirX * cos(-self.TurnSpeed) - self.dirY * sin(-self.TurnSpeed)
      self.dirY = oldDirX * sin(-self.TurnSpeed) + self.dirY * cos(-self.TurnSpeed)
      oldPlaneX = self.planeX
      self.planeX = self.planeX * cos(-self.TurnSpeed) - self.planeY * sin(-self.TurnSpeed)
      self.planeY = oldPlaneX * sin(-self.TurnSpeed) + self.planeY * cos(-self.TurnSpeed)
      
    elif keys[pygame.K_LEFT]:

      oldDirX = self.dirX;
      self.dirX = self.dirX * cos(self.TurnSpeed) - self.dirY * sin(self.TurnSpeed);
      self.dirY = oldDirX * sin(self.TurnSpeed) + self.dirY * cos(self.TurnSpeed);
      oldPlaneX = self.planeX;
      self.planeX = self.planeX * cos(self.TurnSpeed) - self.planeY * sin(self.TurnSpeed);
      self.planeY = oldPlaneX * sin(self.TurnSpeed) + self.planeY * cos(self.TurnSpeed);
    
    if keys[pygame.K_UP]:
      if( map[int(self.Ypos)][int(self.Xpos + self.dirX * self.WalkSpeed)] == 0): 
        self.Xpos += self.dirX * self.WalkSpeed         
      if( map[int(self.Ypos + self.dirY * self.WalkSpeed)][int(self.Xpos)] == 0):
        self.Ypos += self.dirY * self.WalkSpeed 
        
    elif keys[pygame.K_DOWN]:
      if( map[int(self.Ypos)][int(self.Xpos - self.dirX * self.WalkSpeed)] == 0): self.Xpos -= self.dirX * self.WalkSpeed 
      if( map[int(self.Ypos - self.dirY * self.WalkSpeed)][int(self.Xpos)] == 0): self.Ypos -= self.dirY * self.WalkSpeed 
    
    
################################

screenWidth = windowWidth
screenHeight = windowHeight

pygame.init()
pygame.display.set_caption("Raycaster")

player = Player()

main( pygame.display.set_mode((windowWidth, windowHeight)) )

print("Done.")
pygame.quit()
