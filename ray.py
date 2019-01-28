import math
import pygame

windowWidth = 500
windowHeight = 420

screenWidth = windowWidth
screenHeight = windowHeight

pygame.init()
pygame.display.set_caption("Raycaster")

map = [
 [1,1,2,1,1,1,2,1,1],
 [1,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,0,0,0,1],
 [1,0,0,0,0,4,0,0,1],
 [1,0,4,4,4,2,0,0,1],
 [1,0,0,0,0,4,0,0,3],
 [1,0,0,0,0,4,0,0,1],
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
      perpWallDist = 0
      
      stepX = 0
      stepY = 0
      
      hit = 0
      side = 0

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
      
      while hit == 0:
      
        if sideDistX < sideDistY:
          sideDistX += deltaDistX
          mapX += stepX
          side = 0
        else:
          sideDistY += deltaDistY
          mapY += stepY
          side = 1
        
        hit = map[mapY][mapX]

      # Calculate distance projected on camera direction (Euclidean distance will give fisheye effect!)
      if (side == 0): perpWallDist = (mapX - player.Xpos + (1 - stepX) / 2) / (rayDirX+ 0.00001)
      else:           perpWallDist = (mapY - player.Ypos + (1 - stepY) / 2) / (rayDirY+ 0.00001)
    
      # Calculate height of line to draw on screen
      lineHeight = int(screenHeight / (perpWallDist+0.00001))
      
      #print( screenHeight / lineHeight )
      
      # calculate lowest and highest pixel to fill in current stripe
      drawStart = int(-lineHeight / 2 + screenHeight / 2)
      
      if(hit == 2): drawStart = int(-lineHeight + screenHeight / 2)
      
      if(drawStart < 0): drawStart = 0
      drawEnd = int(lineHeight / 2 + screenHeight / 2)
      if(drawEnd >= screenHeight): drawEnd = screenHeight - 1
     
      c1 = (255 - 9.5*math.fabs(perpWallDist/0.5)) 
      c2 = c1
      c3 = c1
      
      if(hit == 2): c2 = 0
      if(hit == 3): c1 = 0
      if(hit == 4): c3 = 0
      
      if(side == 0): 
        c1 /= 1.05
        c2 /= 1.05
        c3 /= 1.05
      
      color = (c1, c2, c3)
      try:    
        pygame.draw.line(screen, color, (x, drawStart), (x, drawEnd))
      except:
        print(perpWallDist)
        input("Error")
    
    player.update()
    pygame.display.flip()
    screen.fill((0,0,0))
    



# Event loop
def event_loop():
  
  for event in pygame.event.get():
          if event.type == pygame.QUIT:
                  return False
            
            
  return True


################################
# Handle player

class Player():

  def __init__(self):
  
    ## set player starting attributes

    self.Xpos = 2
    self.Ypos = 2
    
    self.dirX = -1
    self.dirY = 0
    
    self.planeX = 0
    self.planeY = 0.66
    
    self.WalkSpeed = 0.01
    self.TurnSpeed = 0.2
  
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
        #print(self.Xpos)
        
      if( map[int(self.Ypos + self.dirY * self.WalkSpeed)][int(self.Xpos)] == 0):
        self.Ypos += self.dirY * self.WalkSpeed 
        
    elif keys[pygame.K_DOWN]:
      if( map[int(self.Ypos)][int(self.Xpos - self.dirX * self.WalkSpeed)] == 0): self.Xpos -= self.dirX * self.WalkSpeed 
      if( map[int(self.Ypos - self.dirY * self.WalkSpeed)][int(self.Xpos)] == 0): self.Ypos -= self.dirY * self.WalkSpeed 
    
    #print(map[int(self.Ypos)][ int(self.Xpos + self.dirX * self.WalkSpeed) ])
    
    
################################

player = Player()

main( pygame.display.set_mode((windowWidth, windowHeight)) )

print("Done.")
pygame.quit()