import pygame
import numpy as np
from sys import exit

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 1
JUMP_VELOCITY = -21
OBSTACLE_SPEED = 7
SPAWN_INTERVAL = 900  # milliseconds

left = False
class Player(pygame.sprite.Sprite):
    """Игровой герой с возможностью прыжка и перемещения"""
    def __init__(self, image_path, position,animatuon_path = [] ,scale=0.2):
        super().__init__()
        self.stay= pygame.image.load(image_path).convert_alpha()
        self.jump = pygame.image.load('mario/mario_jmp.png').convert_alpha()
        self.ind = 0
        self.image = self.stay
        self.rect = self.image.get_rect(topleft=position)
        self.velocity_y = 0
        self.speed_x = 0
        if animatuon_path:
            self.run = [pygame.image.load(anime).convert_alpha() for anime in animatuon_path ]
            # self.run_revers = [ pygame.transform.flip(anime,1,0) for anime in animatuon_path ]


    def handle_input(self, events, keys):
        # Горизонтальное движение
        global left
        self.speed_x = 0
        if self.ind<= 1.9: self.ind+=0.05
            
        else: self.ind = 0
            
        if self.speed_x == 0:
            if left: 
                self.image = pygame.transform.flip(self.stay,1,0)

            else:  self.image = self.stay


        if  self.rect.y <270 and not left:
            self.image = self.jump
        if  self.rect.y <270 and  left:
            self.image = pygame.transform.flip(self.jump,1,0)



        if keys[pygame.K_d] :
            if self.rect.x <SCREEN_WIDTH- self.image.get_width():
                self.speed_x = 6
            if self.rect.y >225:
                self.image = self.run[int(self.ind)]
            left= False

        if keys[pygame.K_a]:
            if self.rect.x >0:
                self.speed_x = -6
            if self.rect.y >225:
                self.image = pygame.transform.flip(self.run[int(self.ind)],True,0) #self.run_revers[int(self.ind)]
            left= True
        # Прыжок мышью
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.bottom >= 420:
                if self.rect.collidepoint(event.pos):
                    self.velocity_y = -20
            if event.type == pygame.KEYDOWN and self.rect.bottom >= 420:
                if event.key == pygame.K_SPACE:
                    self.velocity_y = JUMP_VELOCITY

    def update(self, keys, events):
        # Обработка ввода
        self.handle_input(events, keys)
        # Плавное снижение скорости (имитация трения)
        self.speed_x /= (0.905 + 1 / (abs(self.speed_x) + 10))
        self.rect.x += self.speed_x
        # Применение гравитации
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        # Ограничение пола
        if self.rect.bottom >= 420:
            self.rect.bottom = 420
            self.velocity_y = 0

class Obstacle(pygame.sprite.Sprite):
    """Препятствие, движущееся слева направо"""
    def __init__(self, image, position, speed=OBSTACLE_SPEED , animation = []):
        super().__init__()

        self.animation = animation
        self.image = image
        self.rect = self.image.get_rect(bottomright=position)
        self.speed = speed
        self.index = 0

    def update(self):
        
        self.rect.x -= self.speed

        
        if self.index <= 1.9: self.index += 0.1 # у всех гумб разный момент анимации если сделать через global то они сенхронизируются 
            
        # if self.index >1:
        #     self.rect.y=400    
        else: self.index = 0    

        if self.animation :
            self.image = self.animation[int(self.index)]
        
        # Если ушло за экран, удалить
        if self.rect.right < 0:
            self.kill()

class Timer:
    """Отсчет времени от старта игры"""
    def __init__(self, font, position):
        self.font = font
        self.position = position
        self.start_ticks = pygame.time.get_ticks()

    def draw(self, surface):
        global OBSTACLE_SPEED # 
        current = pygame.time.get_ticks()
        seconds = (current - self.start_ticks) // 1000
        OBSTACLE_SPEED +=seconds/1000  #  трол мод
        text = self.font.render(f"{seconds}", False, 'black').convert_alpha()
        rect = text.get_rect(topleft=self.position)
        pygame.draw.rect(surface, '#d12e4c', rect, 4, border_radius=4)
        surface.blit(text, rect)
        return current

class Game:
    def __init__(self):
        global OBSTACLE_SPEED
        pygame.init()
        pygame.display.set_caption('Джиджа full ООП')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.load_assets()
        OBSTACLE_SPEED = 7
        
        self.reset_game()
        # Событие спавна препятствий
        self.SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_EVENT, SPAWN_INTERVAL)

    def load_assets(self):
        # Фон
        sky = pygame.image.load('sky.jpg').convert()
        ground = pygame.image.load('ground.jpg').convert()
        self.bg_sky = pygame.transform.scale(sky, (sky.get_width() * 2, sky.get_height() * 2))
        self.bg_ground = pygame.transform.scale(ground, (int(ground.get_width() * 0.7),
                                                        int(ground.get_height() * 0.7)))
        # Текстовые поверхности
        self.font = pygame.font.Font('pixel-operator.ttf', 40)
        self.game_over_surf = pygame.transform.rotozoom(
            self.font.render("GAME OVER", False, 'blue').convert_alpha(), 0, 3)
        self.game_over_rect = self.game_over_surf.get_rect(topleft=(150, 50))
        self.restart_surf = self.font.render("Press SPACE to restart", False, 'white').convert_alpha()
        self.restart_rect = self.restart_surf.get_rect(topleft=(225, 450))
        # Спрайты препятствий
        gumba = pygame.image.load('gumba.png').convert_alpha()
        gumba1 = pygame.image.load('gumba2w.png').convert_alpha()
        gumba1 = pygame.transform.rotozoom(gumba1, 0, 0.15)
        gumba = pygame.transform.rotozoom(gumba, 0, 0.5)
        self.gumba_list = [gumba,gumba1]


        turt = pygame.image.load('tut.png').convert_alpha()
        

        turt = pygame.transform.rotozoom(turt, 0, 0.5)
        self.names = ['gumba.png','tut.png']
        self.obstacle_images = {
            'gumba.png':gumba,
            'tut.png':turt
        }
        # Спрайт игрока
        self.player_image = 'mario/hero.png'
        self.pos = (0,0)

    def reset_game(self):
        self.game_active = True
        # Группа спрайтов
        
        self.player = Player(self.player_image, position=(20, 300),animatuon_path=['mario/mario1.png','mario/mario2.png'])
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.obstacle_group = pygame.sprite.Group()
        # Таймер
        self.timer = Timer(self.font, position=(350, 50))

    def spawn_obstacle(self):

        image = np.random.choice(self.names)
        if image == 'tut.png':
            self.pos = (np.random.randint(SCREEN_WIDTH + 100, SCREEN_WIDTH + 300), np.random.randint(150,240))
            obstacle = Obstacle(self.obstacle_images[image], self.pos,OBSTACLE_SPEED,)
        if image=='gumba.png' :
            self.pos = (np.random.randint(SCREEN_WIDTH + 100, SCREEN_WIDTH + 300), 420)
            obstacle = Obstacle(self.obstacle_images[image], self.pos,OBSTACLE_SPEED,self.gumba_list)
        # dd
        self.obstacle_group.add(obstacle)
  
    def handle_events(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == self.SPAWN_EVENT and self.game_active:
                self.spawn_obstacle()
            if not self.game_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.reset_game()
        # Передаем события игроку
        self.player_group.sprite.handle_input(events, keys)
        return events, keys

    def update(self, events, keys):
        global OBSTACLE_SPEED
        if self.game_active:
            # Обновление спрайтов
            self.player_group.update(keys, events)
            self.obstacle_group.update()
            
            
            # self.image = self.obstecals
            # Проверка коллизий
            if pygame.sprite.spritecollide(self.player, self.obstacle_group, dokill=True):
                self.game_active = False
                OBSTACLE_SPEED = 7

                # Сброс времени
                self.timer.start_ticks = pygame.time.get_ticks()


    def flip():
        global hero_animation ,player_jump, player_stay
        hero_animation= [pygame.transform.flip(img,1,0) for img in hero_animation]
        player_stay = pygame.transform.flip(player_stay ,1,0) 
        player_jump = pygame.transform.flip(player_jump,1,0) 

    def draw(self):
        if self.game_active:
            self.screen.blit(self.bg_sky, (0, 0))
            self.screen.blit(self.bg_ground, (0, 420))
            self.obstacle_group.draw(self.screen)
            self.player_group.draw(self.screen)
            self.timer.draw(self.screen)
        else:
            self.screen.fill('#0B0C0C')
            self.screen.blit(self.game_over_surf, self.game_over_rect)
            pygame.draw.rect(self.screen, '#0069BF', self.game_over_rect, 6, border_radius=8)
            self.screen.blit(self.restart_surf, self.restart_rect)
        pygame.display.update()

    def run(self):
        while True:
            events, keys = self.handle_events()
            self.update(events, keys)
            self.draw()
            self.clock.tick(60)


Game().run()
