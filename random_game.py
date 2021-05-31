from pygame import *
from random import *
init()

w = 800
h = 600
speed =  3
size = 16
enemy_count = 1
win = display.set_mode((w,h))
display.set_caption("random_game")
font = font.SysFont("consolas", 15)
end = "Game over"

class GameSprite(sprite.Sprite):
    def __init__(self,x,y,speed,size):
        sprite.Sprite.__init__(self)
##########################################################################
# Image from file
#        self.image = transform.scale(image.load(filename),(width,height))
# Square
        self.image = Surface((size,size))
        self.image.fill((255,255,255))
# Circle
#       self.skin = draw.circle(self.image,(255,0,0),(size//2,size//2),size//2)
##########################################################################
        self.rect = self.image.get_rect(center=(x,y))
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size

#class Bullet

class Player(GameSprite):
    nose = Surface((4,4))
    nose.fill((255,255,255))
    look_up = False
    look_down = False
    look_left = False
    look_right = True
    up = False
    down = False
    left = False
    right = False
    shooting = False
    stop_shooting = False
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and  self.rect.y > 0:
            self.up = True
            self.down = False
            self.left = False
            self.right = False
        elif keys[K_DOWN] and self.rect.y < h - self.size:
            self.up = False
            self.down = True
            self.left = False
            self.right = False
        elif keys[K_LEFT] and self.rect.x > 0:
            self.up = False
            self.down = False
            self.left = True
            self.right = False
        elif keys[K_RIGHT] and self.rect.x < w - self.size:
            self.up = False
            self.down = False
            self.left = False
            self.right = True
        else:
            self.up = False
            self.down = False
            self.left = False
            self.right = False
        if keys[K_SPACE]:
            self.shooting = True
        else:
            self.stop_shooting = False
            self.shooting = False
##########################################
        if self.up:
            self.look_up = True
            self.look_down = False        
            self.look_left = False        
            self.look_right = False
            self.rect.y = self.rect.y - self.speed
        elif self.down:
            self.look_up = False
            self.look_down = True
            self.look_left = False        
            self.look_right = False
            self.rect.y = self.rect.y + self.speed
        elif self.left:
            self.look_up = False
            self.look_down = False
            self.look_left = True
            self.look_right = False
            self.rect.x = self.rect.x - self.speed
        elif self.right:
            self.look_up = False
            self.look_down = False        
            self.look_left = False
            self.look_right = True
            self.rect.x = self.rect.x + self.speed
        if self.shooting and self.stop_shooting == False:
            self.shoot()
            self.stop_shooting = True
    def shoot(self):
        if self.look_up:
            projectiles.append(Bullet(self.rect.x+size/2,self.rect.y-2,speed+1,4,"player",'up'))
        elif self.look_down:
            projectiles.append(Bullet(self.rect.x+size/2,self.rect.y+size+2,speed+1,4,"player",'down'))
        elif self.look_left:
            projectiles.append(Bullet(self.rect.x-2,self.rect.y+size/2,speed+1,4,"player",'left'))
        elif self.look_right:
            projectiles.append(Bullet(self.rect.x+size+2,self.rect.y+size/2,speed+1,4,"player",'right'))
    def reset(self):
        win.blit(self.image,self.rect)
        if self.look_up:
            win.blit(self.nose,(self.rect.x+size/2-2,self.rect.y-4))
        elif self.look_down:
            win.blit(self.nose,(self.rect.x+size/2-2,self.rect.y+size))
        elif self.look_left:
            win.blit(self.nose,(self.rect.x-4,self.rect.y+size/2-2))
        elif self.look_right:
            win.blit(self.nose,(self.rect.x+size,self.rect.y+size/2-2))
class Enemy(GameSprite):
    spawning = True
    distance_x = 0
    distance_y = 0
    yshoot = False
    xshoot = False
    shoot_count = 0
    rand = randint(0, 1)
    rand_count = 32
    def spawn(self):
        if self.rect.x >= w-self.size:
                self.rect.x -= self.speed
        elif self.rect.x <= 0:
            self.rect.x += self.speed
        elif self.rect.y >= h-self.size:
            self.rect.y -= self.speed
        elif self.rect.y <= 0:
            self.rect.y += self.speed
        else:
            self.spawning = False
    def update(self):
        if self.spawning:
            self.spawn()
        else:
            self.distance_x = player.rect.x-self.rect.x
            self.distance_y = player.rect.y-self.rect.y
            if self.rand_count <= 0:
                self.rand = randint(0, 1)
                self.rand_count = 16
            if abs(self.distance_x) > abs(self.distance_y):
                if self.rand == 1:
                    if self.distance_y > 0+speed//2:
                        self.rect.y += self.speed
                    elif self.distance_y < 0-speed//2:
                        self.rect.y -= self.speed
                    elif self.shoot_count <= 0:
                        self.xshoot = True
                        self.yshoot = False
                        self.shoot()
                        self.shoot_count = 32
                else:
                    if self.distance_x > 0+speed//2:
                        self.rect.x += self.speed
                    elif self.distance_x < 0-speed//2:
                        self.rect.x -= self.speed
            else:
                if self.rand == 1:
                    if self.distance_x > 0+speed//2:
                        self.rect.x += self.speed
                    elif self.distance_x < 0-speed//2:
                        self.rect.x -= self.speed
                    elif self.shoot_count <= 0:
                        self.xshoot = False
                        self.yshoot = True
                        self.shoot()
                        self.shoot_count = 32
                else:
                    if self.distance_y > 0+speed//2:
                        self.rect.y += self.speed
                    elif self.distance_y < 0-speed//2:
                        self.rect.y -= self.speed
            self.rand_count -= 1
            self.shoot_count -= 1
    def shoot(self):
        if self.yshoot:
            if player.rect.y < self.rect.y:
                projectiles.append(Bullet(self.rect.x+size/2,self.rect.y-2,speed+1,4,"enemy",'up'))
            else:
                projectiles.append(Bullet(self.rect.x+size/2,self.rect.y+size+2,speed+1,4,"enemy",'down'))
        elif self.xshoot:
            if player.rect.x > self.rect.x:
                projectiles.append(Bullet(self.rect.x-2,self.rect.y+size/2,speed+1,4,"enemy",'right'))
            else:
                projectiles.append(Bullet(self.rect.x+size+2,self.rect.y+size/2,speed+1,4,"enemy",'left'))
    def reset(self):
        win.blit(self.image,self.rect)

class Bullet(GameSprite):
    def __init__(self,x,y,speed,size,team,direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.team = team
        self.direction = direction
        self.image = Surface((size,size))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(center=(x,y))
    def update(self):
        if self.direction == "up":
            self.rect.y = self.rect.y - self.speed
        elif self.direction == "down":
            self.rect.y = self.rect.y + self.speed
        elif self.direction == "left":
            self.rect.x = self.rect.x - self.speed
        elif self.direction == "right":
            self.rect.x = self.rect.x + self.speed
    def reset(self):
        win.blit(self.image,self.rect)

def drawtext(title, x, y):
    text = font.render(title, True, (0,255,0))
    wtext = text.get_width()
    htext = text.get_height()
    win.blit(text, (x, y))

game = True
live = True

while game:
    menu = True
    projectiles = []
    enemies = []
    enemy_count = 1
    player = Player(w/2,h/2,speed,size)
    while live:
        time.delay(15)
        for i in event.get():
            if i.type == QUIT:
                game = False
                live = False
                menu = False

        win.fill((00,00,00))
        drawtext("score: " + str(enemy_count - 1), 0, 0)
        player.update()
        player.reset()
        if len(enemies) < enemy_count:
            if randint(0,1) == 0:
                enemies.append(Enemy(randrange(-size,w+1+2*size,size*2+w),randint(0,h-size),speed-1,size))
            else:
                enemies.append(Enemy(randint(0,w-size),randrange(-size,h+1+2*size,h+2*size),speed-1,size))
        for i in enemies:
            i.update()
            i.reset()
        for indexi,i in enumerate(projectiles):
            i.update()
            i.reset()
            if sprite.collide_rect(i,player) and i.team == "enemy":
                live = False
            for indexj,j in enumerate(enemies):
                if sprite.collide_rect(i,j) and i.team == "player":
                    projectiles.pop(indexi)
                    enemies.pop(indexj)
                    enemy_count += 1
        display.update()
    win.fill((0,0,0))
    text = font.render(end, True, (0,255,0))
    wtext = text.get_width()
    htext = text.get_height()
    drawtext(end, (w-wtext)//2, (h-htext)//2 + htext)
    display.update()
    while menu:
        for i in event.get():
            if i.type == QUIT:
                menu = False
                game = False
        keys = key.get_pressed()
        if keys[K_ESCAPE]:
            menu = False
            game = False
        elif keys[K_SPACE]:
            menu = False
            live = True

quit()
