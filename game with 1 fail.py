import pygame
from sys import exit
import numpy as np
pygame.init()

def times(sta):
    currently = pygame.time.get_ticks()
    text_sur = text_go.render(f" {currently- sta} ",False,'black').convert_alpha()
    text_rec = text_sur.get_rect(topleft = (350,50))
    pygame.draw.rect(screen,'#d12e4c',text_rec,4,4,4,4)
    screen.blit(text_sur,text_rec)
    return currently
    


pygame.display.set_caption('джиджа')
scr_weig , scr_hei = 800,600
tut_y = np.random.randint(100,250)
game_act = True
gravity = 0

screen = pygame.display.set_mode((scr_weig,scr_hei))

clock = pygame.time.Clock()
surface_t = pygame.Surface((100,200))
surface_t.fill('Red')

stra_time = pygame.time.get_ticks()

sky_surf = pygame.image.load('sky.jpg').convert()            # convert просто оптимизация
ground_surf = pygame.image.load('ground.jpg').convert()
      
text_go = pygame.font.Font('pixel-operator.ttf', 40)  

turt = pygame.image.load('tut.png').convert_alpha()     
turt = pygame.transform.rotozoom(turt,0,0.5)     
rec_tut = turt.get_rect(midbottom = (1000,tut_y))

player = pygame.image.load('hero.png').convert_alpha()
rec_pl = player.get_rect(midbottom = (20,420) )


hei  = sky_surf.get_height()
wei  = sky_surf.get_width()
sky_scl = pygame.transform.scale(sky_surf,(wei*2,hei*2))

hei  = player.get_height()
wei  = player.get_width()
player = pygame.transform.scale(player,(wei*0.2,hei*0.2))
rec_pl = player.get_rect(bottomleft = (20,420) )

text_go_sur = text_go.render("GAME OVER",False,'blue').convert_alpha()
text_go_sur = pygame.transform.rotozoom(text_go_sur ,0,3)
text_go_sur_rec= text_go_sur.get_rect(topleft = (150,50))

text_press = text_go.render("Press enter to restart ",False,'white').convert_alpha()
text_press_sur = pygame.transform.rotozoom(text_press ,0,1)
text_press_sur_rec= text_press_sur.get_rect(topleft = (225,450))


ground_scl = pygame.transform.scale(ground_surf,(ground_surf.get_width()*0.7,ground_surf.get_height()*0.7 ))    

stat = 0

tut_x = 600

ded = pygame.image.load('ded.png')
ded = pygame.transform.rotozoom(ded,0,0.2)
ded_rec = ded.get_rect(center = (400,300) )



while True:
      
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            
            pygame.quit() 
            exit()


        if game_act:
            if even.type == pygame.MOUSEBUTTONDOWN and  rec_pl.bottom >=220:
                if rec_pl.collidepoint(even.pos):
                    gravity = -20

            if even.type == pygame.KEYDOWN and  rec_pl.bottom >=420:
                if even.key == pygame.K_SPACE:
                    gravity = -20

        else:            
            if  even.type == pygame.KEYDOWN and  not game_act :
                if even.key == pygame.K_SPACE:
                    game_act = True

        
    if game_act:
    
        if rec_tut.centerx > -turt.get_width() :
            rec_tut.centerx-=9
        else:
            rec_tut.centerx = scr_weig + turt.get_width()
            rec_tut.centery = np.random.randint(100,200)

    
        screen.blit(sky_scl , (0,0))
        screen.blit(ground_scl , (0,420)) 
        
        

        if rec_pl.colliderect(rec_tut): print('game over')    

        screen.blit(turt , rec_tut)

        times(stat)

        gravity += 1
        rec_pl.centery += gravity
        if rec_pl.bottom >= 420: rec_pl.bottom =420
        screen.blit(player,rec_pl)

        if rec_tut.colliderect(rec_pl):
            game_act = False
            stat = times(0)
        pygame.display.update()
        clock.tick(60)    



    else:
        screen.fill('#0B0C0C') # navy
        screen.blit(ded,ded_rec)
        pygame.draw.rect(screen,'#0069BF',text_go_sur_rec,6,6,8,8)
        screen.blit(text_go_sur, text_go_sur_rec )
        
        
        screen.blit(text_press_sur, text_press_sur_rec )

        rec_tut.centerx = 900     
        rec_tut.centery = np.random.randint(0,250)
        
        # второя фотка ставится поверх первой 
        # и перекрывает первою , любопытно
        pygame.display.update()
        clock.tick(60)





