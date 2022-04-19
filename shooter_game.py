from pygame import *
from random import randint, uniform
from time import sleep
mixer.init()
font.init()

score = 0

win_width = 700
win_height = 500
mw = display.set_mode((win_width, win_height))
backround =  transform.scale(image.load('galaxy.jpg'), (win_width,win_height))
mw.blit(backround, (0,0))
clock = time.Clock()

mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load( player_image), (w,h))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

    
class Player(GameSprite):
    def move(self):
        key_p = key.get_pressed()
        if key_p[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        if key_p[K_RIGHT] and self.rect.x < 640:
            self.rect.x += self.speed

        if key_p[K_SPACE] :
            fire.play()
            p.fire()

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x + 32 , self.rect.y, 15, 10, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost 
        self.rect.y += self.speed
        if self.rect.y >= 500:
            lost += 1
            self.speed = uniform(1.0, 3.5)
            self.rect.y = -80
            self.rect.x = randint(0, win_width-65)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -5:
            self.kill()

bullets = sprite.Group()

  
monsters = sprite.Group()
for i in range(5):
    e1 = Enemy('ufo.png', randint(0, win_width-65), -80, uniform(1.0, 3.5), 85, 55) 
    monsters.add(e1)            

p = Player('rocket.png', 0, 415, 10, 65, 85)

lost = 0
game_false = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
    mw.blit(backround, (0,0))
    if score == 10:
        game_false = True
        win_txt = font.Font(None, 60).render('You Win!', True, (255,255,255))
        mw.blit(win_txt, (win_width/2 - 100, win_height/2 - 10))

    if lost >= 1:
        game_false = True
        lose_txt = font.Font(None, 60).render('YOU LOSE', True, (255, 255, 255))
        mw.blit(lose_txt, (win_width/2 - 100, win_height/2 - 10))
    
    lost_txt = font.Font(None, 36).render('Lost: ' + str(lost), True, (255, 255, 255))
    score_txt = font.Font(None, 36).render('Score: ' + str(score), True, (255, 255, 255))
    mw.blit(score_txt, (10, 40))
    mw.blit(lost_txt, (10,10))
    monsters.draw(mw)
    bullets.draw(mw)
    p.move()
    p.reset()
    monsters.update()
    bullets.update()
    
    collides = sprite.groupcollide(monsters, bullets, True, True)
        
    for c in collides:
        score += 1
        e1 = Enemy('ufo.png', randint(0, win_width-65), -80, uniform(1.0, 3.5), 85, 55) 
        monsters.add(e1)

        

    display.update()
    clock.tick(60)
    if game_false:
        game = False
sleep(5)