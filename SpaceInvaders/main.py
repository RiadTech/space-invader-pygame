
from time import sleep
import pygame
from sys import exit
import random
from pygame import mixer
pygame.init()
mixer.init()
SCREEN_HEIGHT=600

SCREEN_WIDTH=700

clock=pygame.time.Clock()


screen=pygame.display.set_mode((SCREEN_HEIGHT,SCREEN_WIDTH))
#Define Images

ship_image=pygame.image.load("assets/images/Ship.png")

bullet_image=pygame.image.load("assets/images/Bullet.png")
barrier_image_left=pygame.image.load("assets/images/WeakBlock.png")
barrier_image_right=pygame.image.load("assets/images/WeakBlock.png")
#Define Colors

BLACK=(0,0,0)
WHITE=(255,255,255)
#Define fonts
FONT1=pygame.font.Font("assets/fonts/unifont.ttf",28)
#Game Variables
random_number=[6,7,8,9,10]
VEL=5

LIFES=3
SCORE=0
HOW_MANY_ALIENS=25
rows = 5
cols = 5
alien_bullets_num=6
#Create barrier class
class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = barrier_image_left
        self.rect = self.image.get_rect()
        
        self.rect.center = (x, y)
    def update(self):
        if pygame.sprite.spritecollide(self, alien_bullet_group, True):
            self.kill()
        if pygame.sprite.spritecollide(self, bullet_group, True):
            self.kill()

        

#Create Bullet Class

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        
        self.rect.center = (x, y)
    def update(self):
        global SCORE , HOW_MANY_ALIENS
        self.rect.y -= int(2.5)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            SCORE+=random.choice(random_number)
            HOW_MANY_ALIENS-=1
            #mixer.music.load("assets/sounds/InvaderHit.wav")
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('assets/sounds/InvaderHit.wav'))
            mixer.music.play()
#Create Player Class

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(ship_image, (45, 45))
        
        self.width = 45

        self.height = 45

        self.rect = pygame.Rect(0, 0, self.width,self.height)
        
        self.rect.center = (x, y)
        
        self.last_shot = pygame.time.get_ticks()
    def draw(self):
        screen.blit(self.image,self.rect.topleft)
        
    def move(self):
        keys=pygame.key.get_pressed()
        time_now = pygame.time.get_ticks()
        speed = 8
        cooldown = 800
        if keys[pygame.K_LEFT] and self.rect.x - VEL > 0:

            self.rect.x-=3
        if keys[pygame.K_RIGHT] and self.rect.x + VEL + self.rect.width < SCREEN_WIDTH - 100:

            self.rect.x+=3
        if keys[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            
            bullet_group.add(bullet)
            self.last_shot = time_now
            mixer.music.load("assets/sounds/ShipBullet.wav")
            mixer.music.play()
    def player_stuff(self):
        global LIFES,ship_image
        if LIFES==2:
            self.image=pygame.image.load("assets/images/ShipCrushedLeft.png")
        
#Create Alien Class
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/Invader" + str(random.randint(1, 6)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
bullet_speed=2
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/images/BulletA.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        global LIFES
        self.rect.y += bullet_speed
        
        if self.rect.top > SCREEN_HEIGHT + 81:
            self.kill()
        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            self.kill()
            LIFES-=1
            #mixer.music.load("assets/sounds/ShipHit.wav")
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/sounds/ShipHit.wav'))
            #pygame.mixer.Channel(1).play(pygame.mixer.Sound('sound\enemy_hit.wav'))
            mixer.music.play()

            

ship = Player(270 , 600)
player_group = pygame.sprite.Group() 
player_group.add(ship)
bullet_group = pygame.sprite.Group() 
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
barrier_left=Barrier(80,500)
barrier_right=Barrier(520,500)
barrier_group = pygame.sprite.Group()
barrier_group.add(barrier_left)
barrier_group.add(barrier_right)
#Functions
def create_aliens():
    #generate aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 60 -70)
            alien_group.add(alien)

create_aliens()
def draw_text(text,x,y):
    draw_text = FONT1.render(text, 1, (255, 255, 255))
    screen.blit(draw_text , (x , y))
def cheaty_cheat():
    pass


def reset_enemies():
    global HOW_MANY_ALIENS, alien_bullets_num,bullet_speed
    if HOW_MANY_ALIENS == 0:
        
        create_aliens()
        HOW_MANY_ALIENS = 25
        alien_bullets_num+=3
        alien_bullet_group.empty()
        bullet_group.empty()
        bullet_speed+=1
        random_number.append(12)


def main():
    alien_cooldown = 1000#bullet cooldown in milliseconds
    last_alien_shot = pygame.time.get_ticks()

    while True:
        FPS=60
        clock.tick(FPS)  
        screen.fill(BLACK)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x , y = pygame.mouse.get_pos()
                barrier=Barrier(x,y)
                barrier_group.add(barrier)
            #shoot
        time_now = pygame.time.get_ticks()
        if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < alien_bullets_num and len(alien_group) > 0:
            attacking_alien = random.choice(alien_group.sprites())
            alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_bullet_group.add(alien_bullet)
            last_alien_shot = time_now
            
        ship.move()
        ship.draw()
        #ship.player_stuff()
        bullet_group.draw(screen)
        bullet_group.update()
        alien_group.draw(screen)
        alien_group.update()
        alien_bullet_group.update()
        alien_bullet_group.draw(screen)
        barrier_group.draw(screen)
        barrier_group.update()
        draw_text(f"Score = {SCORE}",30 , 650)
        draw_text(f"{LIFES}",550, 650)
        reset_enemies()
        if LIFES <= 0:
            lost_menu(screen)
        pygame.display.update()
    
def main_menu(surface):
    FONT2=pygame.font.Font("assets/fonts/unifont.ttf",50)
    FONT3=pygame.font.Font("assets/fonts/unifont.ttf",18)
    effect=pygame.image.load("assets/images/Invader7.png")
    run = True
    while run:
        surface.fill((0,0,0))
        title_label = FONT2.render("Space Invaders", 1, (255,255,255))
        creator_label=FONT3.render("Created By Riad", 1, (255,255,255))
        surface.blit(title_label, (150,80))
        surface.blit(creator_label, (430,130))
        surface.blit(effect,(520,99))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()
def lost_menu(surface):
    FONT2=pygame.font.Font("assets/fonts/unifont.ttf",50)
    FONT3=pygame.font.Font("assets/fonts/unifont.ttf",18)
    effect=pygame.image.load("assets/images/Invader7.png")
    
    run = True
    while run:
        LIFES=3
        surface.fill((0,0,0))
        title_label = FONT2.render("Ded", 1, (255,255,255))
        creator_label=FONT3.render("Play Again", 1, (255,255,255))
        surface.blit(title_label, (150,80))
        surface.blit(creator_label, (430,130))
        surface.blit(effect,(520,99))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    
        pygame.display.update()
    pygame.quit()
main_menu(screen)
    
    
    