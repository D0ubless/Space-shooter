from pygame import *
from random import randint
from time import time as timer


#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')



#шрифты и надписи
font.init()
font2 = font.SysFont('Arial', 36)


#нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # враг
img_asteroid = 'asteroid.png' # метеорит
img_bullet = 'bullet.png' # пуля


score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
lifes = 3 #жизни
rel_time = False #перезарядка идёт? нет
quality_shots = 0 #нужно для перезарядки, если равно пяти переменная обнуляется, а функция стрельбы засыпает на 3 секунды

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, ship.rect.centerx, ship.rect.top, 20, 25, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

#создание окна
win_width = 800
win_height = 600
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# создание спрайта игрока
ship = Player(img_hero, 5, win_height - 100, 100, 120, 15)

# группы спрайтов
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
playerr = sprite.Group()
playerr.add(ship)

# появление инопланетян и метеоритов
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 90, 60, randint(1, 5))
    monsters.add(monster)

for i in range(1, 3):
            asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 90, 60, randint(3, 7))
            asteroid.add(asteroids)

#переменные за счёт которых живёт игровой цикл
finish = False
run = True 

while run: # игровой цикл
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN: 
            if e.key == K_SPACE:
                if quality_shots < 7 and rel_time == False:
                    quality_shots += 1
                    fire_sound.play()
                    ship.fire()
                if quality_shots >= 7 and rel_time == False:
                    start_timer = timer()
                    rel_time = True

        
    if finish != True:
        window.blit(background,(0,0))

        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lost = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lost, (10, 50))
        text_lost = font2.render("Жизни: " + str(lifes), 1, (255, 255, 255))
        window.blit(text_lost, (680, 20))

        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        sprites_list1 = sprite.groupcollide(asteroids, playerr, True, False)
        sprites_list2 = sprite.groupcollide(monsters, playerr, True, False)
        
        for c in sprites_list:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 90, 60, randint(1, 5))
            monsters.add(monster)

        quality_asteroids = len(asteroids)

        if quality_asteroids == 1:
            asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 90, 60, randint(3, 7))
            asteroid.add(asteroids)

        sprite.groupcollide(asteroids, bullets, False, True)

        for c in sprites_list1:
            lifes -= 1
        for c in sprites_list2:
            lifes -= 1
        
        # перезарядка
        if rel_time == True:
            fix_time = timer()
            if fix_time - start_timer < 3:
                text_lost = font2.render("ПЕРЕЗАРЯДКА", 1, (255, 255, 255))
                window.blit(text_lost, (300, 500))
            else:
                quality_shots = 0
                rel_time = False

        # условия проигрыша/победы
        if lifes == 0:
            text_lost = font2.render("ТЫ ПРОИГРАЛ!", 1, (255, 255, 255))
            window.blit(text_lost, (275, 250))
            run = False
        
        if score >= 50:
            text_lost = font2.render("ТЫ ВЫЙГРАЛ!", 1, (255, 255, 255))
            window.blit(text_lost, (275, 250))
            run = False

        if lost >= 5:
            text_lost = font2.render("ТЫ ПРОИГРАЛ!", 1, (255, 255, 255))
            window.blit(text_lost, (275, 250))
            run = False

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        
        ship.reset()

        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        display.update()
        
    time.delay(30)