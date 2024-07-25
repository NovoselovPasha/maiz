# Разработай свою игру в этом файле!
from pygame import*

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('Maze (Лабиринт)')

class GameSprite(sprite.Sprite):
    def __init__(self, image_name, x, y, width, height):
        super().__init__()
        img = image.load(image_name)
        self.image = transform.scale(img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self, image_name, x, y, width, height, speed_x, speed_y):
        super().__init__(image_name, x, y, width, height)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def move(self):
        ''' перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость'''
        # сначала движение по горизонтали
        if self.rect.x <= win_width-80 and self.speed_x > 0 or self.rect.x >= 0 and self.speed_x < 0:
            self.rect.x += self.speed_x
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.speed_x > 0: # идем направо, правый край персонажа - вплотную к левому краю стены
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) # если коснулись сразу нескольких, то правый край - минимальный из возможных
        elif self.speed_x < 0: # идем налево, ставим левый край персонажа вплотную к правому краю стены
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) # если коснулись нескольких стен, то левый край - максимальный
        if self.rect.y <= win_height-80 and self.speed_y > 0 or self.rect.y >= 0 and self.speed_y < 0:
            self.rect.y += self.speed_y
        # если зашли за стенку, то встанем вплотную к стене
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.speed_y > 0: # идем вниз
            for p in platforms_touched:
                self.speed_y = 0
                # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.speed_y < 0: # идем вверх
            for p in platforms_touched:
                self.speed_y = 0  # при столкновении со стеной вертикальная скорость гасится
                self.rect.top = max(self.rect.top, p.rect.bottom) # выравниваем верхний край по нижним краям стенок, на которые наехали

    def fire(self):
        bullet = Bullet('free-icon-bullet-5322239.png',
                        x = self.rect.right,
                        y = self.rect.centery,
                        width=15,
                        height = 15,
                        speed= 1)
        bullets.add(bullet)

class Bullet(GameSprite):
    def __init__(self, image_name, x, y, width, height, speed):
        super().__init__(image_name, x, y, width, height)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width:
            self.kill()

class Enemy(GameSprite):
    def __init__(self, image_name,x, y, width, height, speed):
        super().__init__(image_name, x, y, width, height)
        self.speed = speed
        self.direction = 'left'
    def update(self):
        if self.rect.x > 650:
            self.direction = 'left'
        elif self.rect.x < 400:
            self.direction = 'right'
        
        if self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
     


bullets = sprite.Group()
barriers = sprite.Group()



background =GameSprite('photo_2024-07-04_13-02-06.jpg',
                       0,
                       0,
                       win_width,
                       win_height)

winground = GameSprite('free-icon-trophy-1961429.png',
                        0,
                        0,
                        win_width,
                        win_height)

loseground = GameSprite('free-icon-lose-4372342.png',
                        0,
                        0,
                        win_width,
                        win_height)

    
platform1 = GameSprite('free-icon-brick-wall-2139359.png',
                        200,
                        200,
                        100,
                        200)
barriers.add(platform1)




main_hero = Player('free-icon-character-15532214.png', 
                35,
                400,
                50,
                60,
                0,
                0)


enemy = Enemy('free-icon-death-3330575.png',
                500,
                400,
                50,
                60,
                3)


finish = GameSprite('free-icon-finish-783756.png',
                    500,
                    50,
                    60,
                    60)
clock = time.Clock()
FPS = 60


run = True
end = False


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_DOWN:
                main_hero.speed_y = 5
            elif e.key == K_UP:
                main_hero.speed_y = -5
            elif e.key == K_RIGHT:
                main_hero.speed_x = 5
            elif e.key == K_LEFT:
                main_hero.speed_x = -5
            elif e.key == K_SPACE:
                main_hero.fire() 
        elif e.type == KEYUP:
            if e.key == K_DOWN:
                main_hero.speed_y = 0
            elif e.key == K_UP:
                main_hero.speed_y = 0
            elif e.key == K_RIGHT:
                main_hero.speed_x = 0
            elif e.key == K_LEFT:
                main_hero.speed_x = 0
    if not end:
        background.draw()
        platform1.draw()
        main_hero.draw()
        bullets.draw(window)
        bullets.update()
        enemy.draw()
        finish.draw()
        main_hero.move()
        enemy.update()

        # keys = key.get_pressed()
        # if keys[K_LEFT] and main_hero.rect.x >= 1:
        #     main_hero.rect.x -= main_hero.speed_x
        # elif keys[K_RIGHT] and main_hero.rect.x <= 699:
        #     main_hero.rect.x += main_hero.speed_x
        # elif keys[K_UP] and main_hero.rect.y >= 1:
        #     main_hero.rect.y -= main_hero.speed_y
        # elif keys[K_DOWN] and main_hero.rect.y <= 440:
        #     main_hero.rect.y += main_hero.speed_y
        # elif keys[K_SPACE]:
        #     main_hero.fire()

        if main_hero.rect.colliderect(enemy.rect):
            loseground.draw()
            end = True
        elif main_hero.rect.colliderect(finish.rect):
            winground.draw()
            end = True
        
        if sprite.spritecollide(enemy, bullets, True):
            enemy.rect.x = 1000
            enemy.rect.y = 1000
            enemy.kill()
            display.update()

        sprite.spritecollide(platform1, bullets, True)




            
            


        display.update()
        clock.tick(FPS)    