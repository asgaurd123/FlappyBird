import pygame
import sys
import random

# Pygame setup
pygame.init()
pygame.font.init() 
pygame.mixer.init()


my_font = pygame.font.SysFont('Comic Sans MS', 30)

# Global variables
score = 0


screen = pygame.display.set_mode((720, 480))
clock = pygame.time.Clock()
running = True
swoosh_sound=pygame.mixer.Sound('./audio/swoosh.wav')
wing_sound=pygame.mixer.Sound('./audio/wing.wav')

background = pygame.image.load('./sprites/background-day.png')
def rn():
    empt_list.clear()
    u=random.randrange(200,350)
    empt_list.append(u)
    return u
    
    
empt_list=[]
score_list=[]
point_sound=pygame.mixer.Sound("./audio/point.wav")
hit_sound=pygame.mixer.Sound("./audio/hit.wav")
die_sound=pygame.mixer.Sound("./audio/die.wav")
rn()

score=0
# Create a sprite class for the pipe

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,score=0,  y=empt_list[0]):
        super().__init__()
        self.image = pygame.image.load('./sprites/pipe-green.png')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.counter=0
        self.score=score
    
    def update(self):
        global score_list
        self.rect.x -= 4
        
        if self.rect.right < 0: 
            self.rect.x=720
            self.rect.y=empt_list[0]+self.counter
            
            empt_list.append(self.rect.y)
            
        if self.rect.x==0:
            self.score+=1
            
            score_list.append(self.score)
            pygame.mixer.Sound.play(point_sound)
            
        
class GameOver(pygame.sprite.Sprite):
    def __init__(self, x=270, y=200):
        super().__init__()
        self.image = pygame.image.load('./sprites/gameover.png')
        self.rect = self.image.get_rect(topleft=(x, y))
        
        
            
class Pipe_Up(Pipe):
    def __init__(self,x,y=random.randrange(200,300)-480):
        super().__init__(x)
        
        self.image=pygame.transform.rotate(self.image, 180)
        
        self.rect.y=self.rect.y-480
        self.counter=self.counter-480


class FlappyBird(pygame.sprite.Sprite):
    
    def __init__(self, x, y,collider=False):
        super().__init__()
        self.sprites=['./sprites/bluebird-upflap.png','./sprites/bluebird-midflap.png','./sprites/bluebird-downflap.png']
        self.setPos=0
        
        self.image = pygame.image.load(self.sprites[self.setPos])
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collider=collider

    import time
    def update(self):
        self.rect.y+=4
        self.setPos+=0.2
        if self.setPos<len(self.sprites):
            self.image=pygame.image.load(self.sprites[int(self.setPos)])
        if self.setPos>len(self.sprites):
            self.setPos=0

        
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.rect.y-=15
            
        if self.image==pygame.image.load(r'./sprites/bluebird-upflap.png'):
            self.image=pygame.image.load(r'./sprites/bluebird-midflap.png')
            
        if self.image==pygame.image.load(r'./sprites/bluebird-midflap.png'):
            self.image=pygame.image.load(r'./sprites/bluebird-downflap.png')
            
        if self.image==pygame.image.load(r'./sprites/bluebird-downflap.png'):
            self.image=pygame.image.load(r'./sprites/bluebird-midflap.png')
            
        if self.collider==True:
            pygame.mixer.Sound.play(hit_sound)
        
        if self.rect.y>430:
        	self.kill()


        
# Create a sprite group and add a pipe

all_sprites = pygame.sprite.Group()

pipe_1 = Pipe(720,len(score_list))  # Position the pipe at the right edge of the screen
pipe_2 = Pipe(480,len(score_list))  # Position the pipe at the right edge of the screen
pipe_3 = Pipe(240,len(score_list))  # Position the pipe at the right edge of the screen

pipe_1_u = Pipe_Up(720)  # Position the pipe at the right edge of the screen
pipe_2_u = Pipe_Up(480)  # Position the pipe at the right edge of the screen
pipe_3_u = Pipe_Up(240) 

bird=FlappyBird(50,200)




gameover=GameOver()

all_sprites.add(bird)
all_sprites.add(pipe_1)
all_sprites.add(pipe_2)
all_sprites.add(pipe_3)

all_sprites.add(pipe_1_u)
all_sprites.add(pipe_2_u)
all_sprites.add(pipe_3_u)

gameOver=False

def game_over():
    all_sprites.remove(pipe_1)
    all_sprites.remove(pipe_2)
    all_sprites.remove(pipe_3)
    
    all_sprites.remove(pipe_1_u)
    all_sprites.remove(pipe_2_u)
    all_sprites.remove(pipe_3_u)
    all_sprites.remove(bird)
    
    
    all_sprites.add(gameover)
    pygame.mixer.stop()


score_file=range(10)

score_str='./sprites/0.png'
content=''
# Main game loop
scoreboard=pygame.image.load('./sprites/scoreboard.png')
scoreboard=pygame.transform.scale(scoreboard,(200,100))
medal='./sprites/medal_bronze.png'
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Game Logic

    rn()
    if pygame.sprite.collide_rect(pipe_1,bird) or pygame.sprite.collide_rect(pipe_2,bird) or pygame.sprite.collide_rect(pipe_3,bird) or  pygame.sprite.collide_rect(pipe_1_u,bird) or pygame.sprite.collide_rect(pipe_2_u,bird) or pygame.sprite.collide_rect(pipe_3_u,bird):
        
        bird.kill()
        
    import time
    
    if bird.alive()==False and gameOver==False:
       pygame.mixer.Sound.play(hit_sound)
       gameOver=True
       time.sleep(1)
       
       pygame.mixer.Sound.play(die_sound)
       time.sleep(1)
       
       
       game_over()
    if bird.alive()==False and gameOver==True:
        game_over()
       
    # Update sprites
    all_sprites.update()
    screen.blit(background, (0, 0))
    screen.blit(background, (240, 0))
    screen.blit(background, (480, 0))
    
    if gameOver==True:
        screen.blit(scoreboard,(260,280))
    

    ac_dict={}
    ac_score=str(len(score_list)//2)
    ac_score_lis=[]
       
    for a in ac_score:
        ac_score_lis.append(str(a))
            
    keys=range(len(ac_score_lis))
        
    for i in keys:
        ac_dict[i]=ac_score_lis[i]
        
       
        
    for key,i in ac_dict.items():
        if bird.alive()==True:
                
            screen.blit(pygame.image.load('./sprites/'+str(i)+'.png'),(360+20*key,0))
                
        if bird.alive()==False:

            score_img=pygame.image.load('./sprites/number_middle_'+str(i)+'.png')
            if int(len(score_list)/2)>0 and int(len(score_list)/2)<10:
                medal='./sprites/medal_bronze.png'
               
        
                
            if int(len(score_list)/2)>=10 and int(len(score_list)/2)<20:
                medal='./sprites/medal_silver.png'
                
        
                
            if int(len(score_list)/2)>=20 and int(len(score_list)/2)<30:
                medal='./sprites/medal_gold.png'
                

                
            if int(len(score_list)/2)>30:
                medal='./sprites/medal_bronze.png'
                

            screen.blit(pygame.image.load('./sprites/number_middle_'+str(i)+'.png'),(415+10*key,310))
            medal_sprite=pygame.image.load(medal)
            medal_sprite=pygame.transform.scale(medal_sprite,(36,36))
            screen.blit(medal_sprite,(284,320))
                
            with open('highscore.txt','a+') as fil:
                
                fil.seek(0)
                content=fil.read()
                
                if int(content)<int(len(score_list)/2):
                    fil.truncate(0)
                    fil.write(str(int(len(score_list)/2)))
                    
    high_score_lis=[]
    high_score_dict={}
       
    for a in content:
        high_score_lis.append(str(a))
            
    keys_high=range(len(high_score_lis))
        
    for i in keys_high:
        high_score_dict[i]=high_score_lis[i] 
    
        
    for key,item in high_score_dict.items():
        screen.blit(pygame.image.load('./sprites/number_middle_'+item+'.png'),(415+10*key,350))
                    
                
                
    

    
    all_sprites.draw(screen)
    all_sprites.update()

    # Update the display
    pygame.display.flip()
    pygame.display.update()

    # Limit the frame rate to 60 FPS
    clock.tick(50)
    

# Quit Pygame
pygame.quit()
sys.exit()
