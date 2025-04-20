import pygame
from sys import exit
import numpy as np
import copy
pygame.init()

def flip():
    global hero_animation ,player_jump, player_stay
    hero_animation= [pygame.transform.flip(img,1,0) for img in hero_animation]
    player_stay = pygame.transform.flip(player_stay ,1,0) 
    player_jump = pygame.transform.flip(player_jump,1,0) 

    
    
stra_time = 0


class Object(pygame.sprite.Sprite):


    def __init__(self, image_path,rect,  tran = 0):
        super().__init__()
        
        self.image_path = image_path
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.tran = tran
        if self.tran:
            self.image = pygame.transform.rotozoom(self.image,0,self.tran)
            self.rect = self.image.get_rect(midbottom = rect)
        else:
            self.rect = self.image.get_rect(midbottom = rect)
    def speed(self,sped): 
            self.rect.centerx += sped     

    def clone(self):
        tut_y = 420
        if self.image_path == 'tut.png':
            tut_y = np.random.randint(200,250)

        return Object(image_path = self.image_path, rect = (np.random.randint(900,1050,), tut_y), tran = self.tran)

    def draw(self):
        screen.blit(self.image,self.rect)


    #player_animation


def player_animation():
    global rec_pl , player ,ind ,hero_animation, speed
    
    if rec_pl.y < 310:
        player = player_jump
    if speed !=0 and rec_pl.y >200:
        player = hero_animation[int(ind)]
        print()
        if ind <1.9:ind+=0.1
            

        else: ind = 0
    if speed == 0 and rec_pl.y >= 310 :    player = player_stay  


def times(sta):  
    currently = pygame.time.get_ticks()
    text_sur = text_go.render(f" {((currently - stra_time )//1000)} ",False,'black').convert_alpha()
    text_rec = text_sur.get_rect(topleft = (350,50))
    pygame.draw.rect(screen,'#d12e4c',text_rec,4,4,4,4)
    screen.blit(text_sur,text_rec)
    return currently
    
ind = 0
def obs_mov(obs_list) :
    if obs_list:
        for obj in obs_list:
            obj.speed(-7)  # у мобов ускорение
            screen.blit(obj.image, obj.rect)

        obs_list = [obj for obj in obs_list  if obj.rect.x > -100 ]
           
        return obs_list
    else : return []   


def colis(obj_list1):
    global obj_list
    if obj_list1:
        for obj in obj_list1:
            if obj.rect.colliderect(rec_pl):
                obj_list =[]
                
                return False

    return True        


pygame.display.set_caption('джиджа')
scr_weig , scr_hei = 800,600
tut_y = np.random.randint(100,250)
game_act = True
gravity = 0

screen = pygame.display.set_mode((scr_weig,scr_hei))

clock = pygame.time.Clock()
surface_t = pygame.Surface((100,200))
surface_t.fill('Red')


stop =False

text_go = pygame.font.Font('pixel-operator.ttf', 40)  

# timer




# player

player_stay = pygame.image.load('mario/hero.png').convert_alpha()
player_jump = pygame.image.load('mario/mario_jmp.png').convert_alpha()
player = pygame.image.load('mario/hero.png').convert_alpha()
player_2 = pygame.image.load('mario/mario2.png').convert_alpha()
player_1 = pygame.image.load('mario/mario1.png').convert_alpha()
hero_animation = [player_1,player_2]

ind=0

rec_pl = player.get_rect(midbottom = (20,420) )



#  animals (enemy)
turt = Object('tut.png',(1000,tut_y),0.5)
gumba = Object('gumba.png', (1200,420),0.5)
obj_list = []

# transformation


hei  = player.get_height()
wei  = player.get_width()

rec_pl = player.get_rect(bottomleft = (20,420) )


# text

text_go_sur = text_go.render("GAME OVER",False,'blue').convert_alpha()
text_go_sur = pygame.transform.rotozoom(text_go_sur ,0,3)
text_go_sur_rec= text_go_sur.get_rect(topleft = (150,50))

text_press = text_go.render("Press enter to restart ",False,'white').convert_alpha()
text_press_sur = pygame.transform.rotozoom(text_press ,0,1)
text_press_sur_rec= text_press_sur.get_rect(topleft = (225,450))

tut_x = 600
# places

sky_surf = pygame.image.load('sky.jpg').convert()            # convert просто оптимизация
ground_surf = pygame.image.load('ground.jpg').convert()
      
ground_scl = pygame.transform.scale(ground_surf,(ground_surf.get_width()*0.7,ground_surf.get_height()*0.7 ))    

hei  = sky_surf.get_height()
wei  = sky_surf.get_width()
sky_scl = pygame.transform.scale(sky_surf,(wei*2,hei*2))


stat = 0



ded = pygame.image.load('ded.png')
ded = pygame.transform.rotozoom(ded,0,0.2)
ded_rec = ded.get_rect(center = (400,300) )

trans= False

# other
speed = 0

# timer
obs_tim = pygame.USEREVENT + 1
timer = pygame.time.set_timer(obs_tim,900) 


list_obg = [gumba,turt]
left = False
while True:  
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            
            pygame.quit() 
            exit()

        
        if even.type == obs_tim and game_act:
            enemy = np.random.choice(list_obg)
        
            obj_list.append(enemy.clone())
            print(obj_list)
            

        if game_act:
            if even.type == pygame.MOUSEBUTTONDOWN and  rec_pl.bottom >=220:
                if rec_pl.collidepoint(even.pos):
                    gravity = -20
                    print(stra_time)


            if even.type == pygame.KEYDOWN and  rec_pl.bottom >=420:
                if even.key == pygame.K_SPACE:
                    gravity = -20
                   
            

            #
        else:        
            rec_pl.centerx = player.get_width()                                                
            if  even.type == pygame.KEYDOWN and  not game_act :
                if even.key == pygame.K_SPACE:
                    game_act = True
    
    keys = pygame.key.get_pressed()    
    # #    
    # # movement
    # #
    if keys[pygame.K_a]:
        rec_pl.centerx -= 6
        speed =1
        if not left:
            flip()
            left = True

    elif keys[pygame.K_d]:
        rec_pl.centerx += 6
        speed =1
        if left:
            left = False
            flip()
    else: speed = 0
    if game_act:
        
    
        game_act = colis(obj_list)      
        screen.blit(sky_scl , (0,0))
        screen.blit(ground_scl , (0,420)) 
     

        obj_list =obs_mov(obj_list)    
        times(stra_time) #

    
        gravity += 1.2
        rec_pl.centery += gravity
        if rec_pl.bottom >= 420: 
            rec_pl.bottom =420
        player_animation()
        screen.blit(player,rec_pl)
        
        
        # if rec_tut.colliderect(rec_pl):
        #     game_act = False
        #     #  = times(stra_time)
        #     gumba_rec.centerx = 1200
        #     rec_tut.centerx = 1100 
        pygame.display.update()
        clock.tick(60)    



    else:
        screen.fill('#0B0C0C') # navy
        screen.blit(ded,ded_rec)
        pygame.draw.rect(screen,'#0069BF',text_go_sur_rec,6,6,8,8)
        screen.blit(text_go_sur, text_go_sur_rec )
        
        
        screen.blit(text_press_sur, text_press_sur_rec )

        # rec_tut.centerx = 900     
        # rec_tut.centery = np.random.randint(0,250)
        
        # второя фотка ставится поверх первой 
        # и перекрывает первою , любопытно
        pygame.display.update()
        clock.tick(60)
        stra_time = pygame.time.get_ticks()





