import pygame
import time
import random
import os
import math



pygame.init()
print(os.path.abspath(os.getcwd()))
path = os.path.abspath(os.getcwd())

MAXX = 4000
MAXY = 4000
X= 800
Y= 600
player_width = 50
player_height = 50
tile_size = 50
friction = 10
player_vmax = 500
tick = 64
bullet_size = {
  "pistol": (20,20)
}

f = {
	"aW" : 0,
	"aWD" : 45,
	"aD" : 90,
	"aSD" : 135,
	"aS" : 180,
	"aSA" : 225,
	"aA" : 270,
	"aWA" : 315,
	"zilch" : 999
}
screen = pygame.display.set_mode((X,Y))
pygame.display.set_caption('Game')
wall = pygame.image.load('./wallpaper.png')
menu = pygame.image.load('./menu.png')
menubutton = pygame.image.load('./menubutton.png')
player = pygame.image.load('./ball.png')
player = pygame.transform.scale(player,(player_width,player_height))
tile = pygame.image.load('./tile.png')
tile = pygame.transform.scale(tile,(tile_size,tile_size))
star = pygame.image.load('./star.png')
star = pygame.transform.scale(star,(tile_size,tile_size))
gold = pygame.image.load('./gold.png')
gold = pygame.transform.scale(gold,(tile_size,tile_size))
hp = pygame.image.load('./hp.png')
hp = pygame.transform.scale(hp,(tile_size,tile_size))


bullet = pygame.image.load('./bullet.png')
bullet = pygame.transform.scale(bullet,bullet_size["pistol"])
crate = pygame.image.load('./crate.png')
crate = pygame.transform.scale(crate,(tile_size,tile_size))
grenade = pygame.image.load('./grenade.png')
grenade = pygame.transform.scale(grenade,(30,30))

ak47 = pygame.image.load('./ak47.png')
ak47 = pygame.transform.scale(ak47,(60,60))

font = pygame.font.Font('freesansbold.ttf', 32)

pygame.Surface.set_colorkey(menubutton,[255,255,255])
pygame.Surface.set_colorkey(bullet,[255,255,255])
pygame.Surface.set_colorkey(player,[255,255,255])
pygame.Surface.set_colorkey(ak47,[255,255,255])
pygame.Surface.set_colorkey(grenade,[255,255,255])
pygame.Surface.set_colorkey(star,[255,255,255])
pygame.Surface.set_colorkey(gold,[255,255,255])
pygame.Surface.set_colorkey(hp,[255,255,255])
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

# sound
pygame.mixer.music.load(path + "\\bg.mp3")
pygame.mixer.music.set_volume(.3)
pygame.mixer.music.play(-1)

shootsound=pygame.mixer.Sound(path+"\\ak47.mp3")
shootsound.set_volume(.15)

grenadesound=pygame.mixer.Sound(path+"\\grenade.mp3")
grenadesound.set_volume(.035)

collectsound=pygame.mixer.Sound(path+"\\collect.mp3")
collectsound.set_volume(.035)

class Camera:
  def __init__(self, x, y) -> None:
    self.x = x
    self.y = y
  def checkObjectInCam(self, x, y):
    dx = x - self.x
    dy = y - self.y
    if dx < 0 or dy < 0: return False
    if dx > 1000 or dy > 800: return False
    return True

class Tile:
  def __init__(self, x, y, type ="tile") -> None:
    self.x = x
    self.y = y
    self.type = type
    self.hitpoint = 4
    self.hidden = False
  def checkCollide(self, o, size):
    dx = abs(self.x - o.x)
    dy = abs(self.y - o.y)
    if dx < tile_size/2 + size/2 and dy < tile_size/2 + size/2:
      return (dx-dy)
    return False

  def playerCollide(self, o, size):
    if self.checkCollide(o,size):
      # o.vD = abs(o.vD + 180) % 360
      # o.v = 25
      if type(o) == Ballistic and o.grenade:
        pass
      else:
        o.vD = 999
      dx = self.x - o.x
      dy = self.y - o.y
      if abs(dx) > abs(dy):
        if dx >= 0: o.x = o.x - 1
        else: o.x = o.x + 2
      else:
        if dy >= 0: o.y = o.y - 1
        else: o.y = o.y + 2
  def draw(self, cam):
    dx = self.x - cam.x
    dy = self.y - cam.y
    if dx < -50 or dy < -50: return False
    if dx > 850 or dy > 650: return False
    if self.type == "tile":
      screen.blit(tile, (dx-tile_size/2,dy-tile_size/2))
    else:
      screen.blit(crate, (dx-tile_size/2,dy-tile_size/2))
    
class Ballistic:
  def __init__(self,x , y, v, vD, o,bullet, grenade = False, dmg = 30) -> None:
    self.x = x
    self.y = y
    self.v = v
    self.vD = vD
    self.img = rot_center(bullet, -vD)
    self.owner = o
    self.grenade = grenade
    self.timer = time.time()
    self.hidden = False
    self.exploded = False
    self.explosionChecked = False
    self.dmg = dmg
  def bounce(self,o):
    pass

  def move(self):
    if self.explosionChecked: self.exploded = True
    if self.vD == 999: return
    tickV = self.v/tick
    a = math.radians(self.vD)
    dx = self.x + math.sin(a)*tickV
    dy = self.y - math.cos(a)*tickV
    self.x = dx
    self.y = dy
    if self.grenade and self.v != 0: 
      self.v = self.v - 10
    
    if self.x < 0 or self.x > MAXX or self.y < 0 or self.y > MAXY: self.vD = 999
  
  def checkCollide(self, o, size):
    dx = (self.x - o.x) 
    if dx < 0: dx = abs(dx)
    else: dx = dx + 7
    dy = (self.y - o.y) 
    if dy < 0: dy = abs(dy)
    else: dy = dy + 7
    if dx <  size and dy <  size:
      if self.grenade:
        self.v = 0
        if type(o) == Tile:
          o.playerCollide(self,30)
        return
      self.vD = 999
      if type(o) == Tile and o.type == "crate":
        o.hitpoint = o.hitpoint - 1
        if o.hitpoint < 0: o.hidden = True
      if type(o) == Character: o.hitpoint = o.hitpoint - self.dmg
      return True
    return False

  def checkExplode(self, o,t):
    
    if t - self.timer < 3: return
    grenadesound.play()
    if type(o) != Character and type(o) != Tile: return
    self.explosionChecked = True
    dx = abs(self.x - o.x)
    dy = abs(self.y - o.y)
    d = math.sqrt(dx*dx+dy*dy)

    if d <  100 :
      if type(o) == Character: o.hitpoint = o.hitpoint - 30
      if type(o) == Tile and o.type == 'crate':
        o.hidden = True
    if d <  70 :
      if type(o) == Character: o.hitpoint = o.hitpoint - 40

    if d <  40 :
      if type(o) == Character: o.hitpoint = o.hitpoint - 50

      return True
    return False

  def checkHit(self, a,t):
    if self.hidden == True: self.vD =999
    if self.exploded: return
    if type(a) == list and len(a)!=0:
      if type(a[0]) == Tile:
        for i in a:
          if self.grenade: 
            self.checkExplode(i,t)
          if self.checkCollide(i,tile_size): return
      if type(a[0]) == Character:
        for i in a:
          if self.grenade: 
            self.checkExplode(i,t)
          if not self.grenade and self.owner != i.type:
            if self.checkCollide(i,player_height): return
    else:
      if self.grenade: self.checkExplode(a,t)
      if type(a) == Character and self.owner != a.type:
        if self.checkCollide(a,player_height): return


  def draw(self,cam):
    
    dx = self.x - cam.x
    dy = self.y - cam.y
    if dx < -50 or dy < -50: return False
    if dx > 850 or dy > 650: return False
    screen.blit(self.img, (dx,dy))
    if time.time() - self.timer > 3 and self.grenade:
      pygame.draw.circle(screen,[255,255,255],(dx,dy),100)
      if time.time() - self.timer > 3.2:
        self.hidden = True

class Item:
  def __init__(self,x,y, name, state) -> None:
    self.name = name
    self.state = state
    self.x = x
    self.y = y
  def draw(self, cam):
    if (self.state==False): return
    dx = self.x - cam.x
    dy = self.y - cam.y
    if dx < -50 or dy < -50: return False
    if dx > 850 or dy > 650: return False
    if self.name == "star":
      screen.blit(star, (dx-tile_size/2,dy-tile_size/2))
    elif self.name == "gold":
      screen.blit(gold, (dx-tile_size/2,dy-tile_size/2))
    else:
      screen.blit(hp, (dx-tile_size/2,dy-tile_size/2))
  def checkCollide(self,o):
    dx = abs(self.x - o.x)
    dy = abs(self.y - o.y)
    if dx < tile_size/2 and dy < tile_size/2:
      self.state=False
      if self.name=="star": o.dmg=o.dmg+50
      elif self.name=="gold": o.gold= o.gold+1
      else: o.hitpoint=o.hitpoint+50

class Character:
  def __init__(self, x, y, t, w,hitpoint = 100) -> None:
    self.x = x
    self.y = y
    self.m = False
    self.angle = 999
    self.vD = 999
    self.d = 0
    self.f = False
    self.v = 100
    self.weapon = w
    self.face = 0
    self.hitpoint = hitpoint
    self.type = t
    self.shooting = False
    self.lastshot = 0
    self.recoil = 0
    self.ammo = [0,0,0]
    self.loadedAmmo = [0,0,0]
    self.grenade = False
    self.gold=0
    self.dmg=50
    

  def attack(self,o):
    if self.type == "player": return
    if self.type == "enemy1":
      dx = self.x - o.x
      dy = self.y - o.y
      if math.sqrt(dx*dx + dy*dy) < 250:
        self.vD = self.getDirection((o.x,o.y))
      else:
        self.vD = 999
    if self.type == "enemy2":
      dx = self.x - o.x
      dy = self.y - o.y

      if math.sqrt(dx*dx + dy*dy) < 350 and  time.time() - self.lastshot > 2:
        self.lastshot =  time.time()
        p = self.getDirection((o.x,o.y))
        temp = Ballistic(self.x,self.y,500, p+1, "enemy2",bullet, False, 15 )
        temp1 = Ballistic(self.x,self.y,500, p-1, "enemy2",bullet, False,15 )
        b.append(temp)
        b.append(temp1)
      else:
        self.vD = 999
  def update(self):
    if not self.shooting and self.recoil != 0 and time.time() - self.lastshot > 1:
      self.recoil = 0
    if self.vD == 999: return
    tickV = self.v/tick
    a = math.radians(self.vD)
    dx = self.x + math.sin(a)*tickV
    dy = self.y - math.cos(a)*tickV
    if dx >= 400: self.x = dx
    if dy >= 300: self.y = dy
  
  def getDirectionMouse(self, pos):
    dx =  400 - pos[0]
    dy =  300 - pos[1]
    d = math.sqrt(dx*dx + dy*dy)
    aX = math.degrees(math.asin(abs(dx)/d))

    p = 0
    if dy >= 0:
      if dx > 0:
        p = 360 - aX
      else:
        p = aX
    else:
      if dx > 0:
        p = 180 + aX
      else:
        p = 180 - aX
    return p
  def getDirection(self, pos):
    dx =  self.x - pos[0]
    dy =  self.y - pos[1]
    d = math.sqrt(dx*dx + dy*dy)
    aX = math.degrees(math.asin(abs(dx)/d))

    p = 0
    if dy >= 0:
      if dx > 0:
        p = 360 - aX
      else:
        p = aX
    else:
      if dx > 0:
        p = 180 + aX
      else:
        p = 180 - aX
    return p
  

  def drawGun(self, pos, g):
    if self.weapon == None: return
    dx =  400 - pos[0]
    dy =  300 - pos[1]
    d = abs(dx) + abs(dy)
    dir = self.getDirectionMouse(pos)
    gun = rot_center(g,-dir)
    
    screen.blit(gun,(400-dx/d*25 -player_height/2,300-dy/d*25-player_height/2))

  def draw(self, pos):
    if self.type == "player": 
      body = rot_center(player,-self.getDirectionMouse(pos))
      screen.blit(body,(400-player_height/2,300-player_height/2))
      if self.grenade:
        self.drawGun(pos, grenade)
      else:
        self.drawGun(pos, ak47)
    else:
      self.drawEnemy(pos)
    
  def drawEnemy(self, cam):
    dx = self.x - cam.x
    dy = self.y - cam.y
    if dx < -50 or dy < -50: return False
    if dx > 850 or dy > 650: return False
    screen.blit(player, (dx-player_height/2,dy-player_height/2))

  def playerCollide(self, e):
    for i in e:
      d = math.sqrt((self.x - i.x)*(self.x - i.x) + (self.y - i.y)*(self.y - i.y))
      if d < player_height:
        dir = (self.getDirection((i.x,i.y)) + 180) % 360
        self.vD = dir
        self.hitpoint = self.hitpoint - 30
        
  def shoot(self,pos, b):
    if not self.shooting: return
    # grenade
    if self.grenade:
      if time.time() - self.lastshot  > 2:
        self.lastshot = time.time()
        # grenadesound.play()
        p = self.getDirectionMouse(pos) 
        temp = Ballistic(self.x,self.y,900, p, "player",grenade, True )
        b.append(temp)
    else:
      shootsound.play()
      if time.time() - self.lastshot  > .15:
        self.lastshot = time.time()
        p = self.getDirectionMouse(pos) + random.randint(-self.recoil,self.recoil)
        
        temp = Ballistic(self.x,self.y,2000, p, "player",bullet,False, self.dmg )
        b.append(temp)

        if self.recoil < 8: self.recoil = self.recoil + 3  

  def keyDown(self, key):
    if key[pygame.K_2] :
      self.grenade = True
      # self.lastshot = 2
    if key[pygame.K_1] :
      self.grenade = False
      # self.lastshot = 2
      print(self.grenade)
    if key[pygame.K_a] :
      if self.angle == f["zilch"]: self.angle = f["aA"]
      if self.angle == f["aD"]: self.angle = f["aA"]
      if self.angle == f["aS"]: self.angle = f["aSA"]
      if self.angle == f["aW"]: self.angle = f["aWA"]
      if self.angle == f["aWD"]: self.angle = f["aWA"]
      if self.angle == f["aSD"]: self.angle = f["aSA"]
    if key[pygame.K_d] :
      if self.angle == f["zilch"]: self.angle = f["aD"]
      if self.angle == f["aA"]: self.angle = f["aD"]
      if self.angle == f["aS"]: self.angle = f["aSD"]
      if self.angle == f["aW"]: self.angle = f["aWD"]
      if self.angle == f["aWA"]: self.angle = f["aWD"]
      if self.angle == f["aSA"]: self.angle = f["aSD"]
    if key[pygame.K_w] :
      if self.angle == f["zilch"]: self.angle = f["aW"]
      if self.angle == f["aS"]: self.angle = f["aW"]
      if self.angle == f["aA"]: self.angle = f["aWA"]
      if self.angle == f["aD"]: self.angle = f["aWD"]
      if self.angle == f["aSA"]: self.angle = f["aWD"]
      if self.angle == f["aSD"]: self.angle = f["aWD"]
    if key[pygame.K_s] :
      if self.angle == f["zilch"]: self.angle = f["aS"]
      if self.angle == f["aW"]: self.angle = f["aS"]
      if self.angle == f["aA"]: self.angle = f["aSA"]
      if self.angle == f["aD"]: self.angle = f["aSD"]
      if self.angle == f["aWA"]: self.angle = f["aSD"]
      if self.angle == f["aWD"]: self.angle = f["aSD"]
    self.vD = self.angle
    self.v = player_vmax
  def keyUp(self, key):
    if key == pygame.K_a:
      if self.angle == f["aA"]: self.angle = f["zilch"]
      if self.angle == f["aWA"]: self.angle = f["aW"]
      if self.angle == f["aSA"]: self.angle = f["aS"]
    if key == pygame.K_d:
      if self.angle == f["aD"]: self.angle = f["zilch"]
      if self.angle == f["aWD"]: self.angle = f["aW"]
      if self.angle == f["aSD"]: self.angle = f["aS"]
    if key == pygame.K_w:
      if self.angle == f["aW"]: self.angle = f["zilch"]
      if self.angle == f["aWD"]: self.angle = f["aD"]
      if self.angle == f["aWA"]: self.angle = f["aA"]
    if key == pygame.K_s:
      if self.angle == f["aS"]: self.angle = f["zilch"]
      if self.angle == f["aSD"]: self.angle = f["aD"]
      if self.angle == f["aSA"]: self.angle = f["aA"]
    self.vD = self.angle
    self.v = player_vmax
p = Character(450,550, "player","ak47")

def cameraMove():
  nx = p.x - 400
  ny = p.y - 300
  if nx < 0: nx = 0
  if ny < 0: ny = 0
  camera.x = nx
  camera.y = ny
camera = Camera(0,0)

e =[]
t = []
b = []
item =[]
def initGame(e,t,b,item):
  for i in range(2):
    temp = Character(800+i*100, 1000,"enemy1",None)
    temp2 = Character(1100+i*100, 1300,"enemy2",None)
    e.append(temp2)
    e.append(temp)

  #build wall
  for i in range(80): 
      
    if (i>6 and i<74):
      wall_ver1 = Tile( (i+1)*tile_size, 250)
      wall_ver5 = Tile( (i+1)*tile_size, 3700)
      t.append(wall_ver1)
      t.append(wall_ver5)
      if (i!=15 and i!=16 and i!=25 and i!=24 and i!=35 and i!=36 and i!=46 and i!=47 and i!=57 and i!=58):
        wall_ver2 = Tile( (i+1)*tile_size, 1000)
        wall_ver3 = Tile( (i+1)*tile_size, 2000)
        wall_ver4 = Tile( (i+1)*tile_size, 2800)
        t.append(wall_ver2)
        t.append(wall_ver3)
        t.append(wall_ver4)
    
    if (i>3 and i<77):
      wall_hor1 = Tile(350,  (i)*tile_size)
      wall_hor5 = Tile(3600,  (i)*tile_size)
      t.append(wall_hor1)
      t.append(wall_hor5)
      if (i!=15 and i!=16 and i!=23 and i!=24 and i!=35 and i!=36 and i!=46 and i!=47 and i!=57 and i!=58):
        wall_hor2 = Tile(1200,  (i)*tile_size)
        wall_hor3 = Tile(2000,  (i)*tile_size)
        wall_hor4 = Tile(2800,  (i)*tile_size)
        t.append(wall_hor2)
        t.append(wall_hor3)
        t.append(wall_hor4)
    # room 1:
    if (i>=10 and i<=12):
      wall1= Tile(750,i*tile_size)
      t.append(wall1)
      wall1= Tile(850,i*tile_size)
      t.append(wall1)
  wall1= Tile(800,500)
  t.append(wall1)
  wall1= Tile(800,600)
  t.append(wall1)
  box1=Tile(800,550,'crate')
  # temp2= Item(900,950,"gold",True)
  # item.append(temp2)
  t.append(box1)
  wall1= Tile(750,800)
  t.append(box1)
  wall1= Tile(750,850)
  t.append(box1)
  wall1= Tile(750,900)
  t.append(box1)
    
  temp1 = Tile(1000, 1000,'crate')
  t.append(temp1)

  # item =[]
  temp= Item(900,900,"hp",True)
  temp1= Item(950,900,"star",True)
  temp2= Item(900,950,"gold",True)
  item.append(temp)
  item.append(temp1)
  item.append(temp2)
  
  p.x=500
  p.y=450
  
    
def resetGame(e,t,b,item):
  e = []
  t = []
  b = []
  item = []
  # initGame(e,t,b,item)
  

clock = pygame.time.Clock()
running = True
menubar = True
gameOver=False

while(running):
  clock.tick(60)
  pygame.display.flip() 
  if (menubar):
    screen.blit(menu,(0,0))
    for i in pygame.event.get():
      # if i.type == pygame.MOUSEBUTTONDOWN:
      #   menubar=True
      if i.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        #newgame
        if (pos[0]>=340 and pos[0]<=550 and pos[1]>=240 and pos[1]<=310): 
          initGame(e,t,b,item)
          for i in e:
            print(i.type)
          menubar = False
        #cont
        if (pos[0]>=340 and pos[0]<=550 and pos[1]>=350 and pos[1]<=420): 
          if (e!=[]): 
            menubar = False
            # print(menubar)
          # else: 
        #exit
        if (pos[0]>=520 and pos[0]<=720 and pos[1]>=470 and pos[1]<=550): 
          running = False
        # about
        if (pos[0]>=520 and pos[0]<=720 and pos[1]>=470 and pos[1]<=550): 
          about=True
      if i.type == pygame.QUIT:
        running = False
  else: 
    clock.tick(60)
    
    if p.hitpoint <= 0:
      gameOver=True
    pos = pygame.mouse.get_pos()
    # if (pos[0]<100 and pos[1]<50): 
    #   menubar=True
    #   pass
    # check tile
    for i in t:
      i.playerCollide(p,player_height)
      for j in e:
        i.playerCollide(j,player_height)
    p.playerCollide(e)
    p.update()
    p.shoot(pos,b)
    for i in e:
      if i.hitpoint <=0:
        e.remove(i)
        del i
        continue
      i.attack(p)
      i.update()
    # check bullet
    for i in b:
      timex = time.time()
      i.checkHit(t,timex)
      i.checkHit(p,timex)
      i.checkHit(e,timex)
      i.move()
      
    cameraMove()
    
    # text = font.render("Gold: ", True, green, blue)
    # screen.blit(text,(10,10))
    
    screen.blit(wall,(0,0),(camera.x,camera.y,800,600))
    
    
    for i in e:
      i.draw(camera)
    p.draw(pos)
    # draw tile/bullet
    for i in t:
      if i.hidden:
        t.remove(i)
        del i
        continue
      i.draw(camera)

    
    for i in item:
      i.checkCollide(p)
      
      if i.state==False: 
        item.remove(i)
      else: 
        i.draw(camera)
    for i in b:
      i.draw(camera)

      if i.vD == 999: 
        b.remove(i)
        del i
    # renderitem

    # pygame.display.flip()
    
    for i in pygame.event.get():
      if i.type == pygame.MOUSEBUTTONDOWN:
        p.shooting = True
      if i.type == pygame.MOUSEBUTTONUP:
        click=pygame.mouse.get_pos()
        if (click[0]<100 and click[1]<50): 
          menubar=True
          pass
        p.shooting = False
        
      key = pygame.key.get_pressed()
      p.keyDown(key)

      if i.type == pygame.KEYUP:
        p.keyUp(i.key)
      if i.type == pygame.QUIT:
        running = False
    screen.blit(menubutton,(0,0))
pygame.quit()
