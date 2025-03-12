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
high_score = 0

screen = pygame.display.set_mode((720, 480))
clock = pygame.time.Clock()
running = True

# Load background image
background = pygame.image.load('./flappy-bird-assets/sprites/background-day.png')
def rn():
    empt_list.clear()
    u=random.randrange(150,350)
    empt_list.append(u)
    return u
    
    
empt_list=[]
score_list=[]
point_sound=pygame.mixer.Sound("./flappy-bird-assets/audio/point.wav")
hit_sound=pygame.mixer.Sound("./flappy-bird-assets/audio/hit.wav")
rn()

score=0
# Create a sprite class for the pipe

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,score=0,  y=empt_list[0]):
        super().__init__()
        self.image = pygame.image.load('./flappy-bird-assets/sprites/pipe-green.png')
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
            
        if self.rect.x==12:
            self.score+=1
            
            score_list.append(self.score)
            pygame.mixer.Sound.play(point_sound)
            
        
class GameOver(pygame.sprite.Sprite):
    def __init__(self, x=270, y=200):
        super().__init__()
        self.image = pygame.image.load('./flappy-bird-assets/sprites/gameover.png')
        self.rect = self.image.get_rect(topleft=(x, y))
        
        
            
class Pipe_Up(Pipe):
    def __init__(self,x,y=random.randrange(200,300)-430):
        super().__init__(x)
        
        self.image=pygame.transform.rotate(self.image, 180)
        
        self.rect.y=self.rect.y-430
        self.counter=self.counter-430


class FlappyBird(pygame.sprite.Sprite):
    
    def __init__(self, x, y,image,collider=False):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collider=collider
    def set_collide(self):
        self.collider==True
    
    def update(self):
        self.rect.y+=4
        
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.rect.y-=15
            
        if self.image==pygame.image.load(r'./flappy-bird-assets/sprites/bluebird-upflap.png'):
            self.image=pygame.image.load(r'./flappy-bird-assets/sprites/bluebird-midflap.png')
            
        if self.image==pygame.image.load(r'./flappy-bird-assets/sprites/bluebird-midflap.png'):
            self.image=pygame.image.load(r'./flappy-bird-assets/sprites/bluebird-downflap.png')
            
        if self.image==pygame.image.load(r'./flappy-bird-assets/sprites/bluebird-downflap.png'):
            self.image=pygame.image.load(r'./flappy-bird-assets/sprites/bluebird-midflap.png')
            
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

bird=FlappyBird(50,200,pygame.image.load('./flappy-bird-assets/sprites/bluebird-midflap.png'))




gameover=GameOver()

all_sprites.add(bird)
all_sprites.add(pipe_1)
all_sprites.add(pipe_2)
all_sprites.add(pipe_3)

all_sprites.add(pipe_1_u)
all_sprites.add(pipe_2_u)
all_sprites.add(pipe_3_u)

def game_over():
    all_sprites.remove(pipe_1)
    all_sprites.remove(pipe_2)
    all_sprites.remove(pipe_3)
    
    all_sprites.remove(pipe_1_u)
    all_sprites.remove(pipe_2_u)
    all_sprites.remove(pipe_3_u)
    all_sprites.remove(bird)
    
    
    all_sprites.add(gameover)


score_file=['0','1','2','3','4','5','6','7','8','9']
score_str='./flappy-bird-assets/sprites/0.png'

# Main game loop


while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #Game Logic

    rn()
    if pygame.sprite.collide_rect(pipe_1,bird):
        
        game_over()
        
    if pygame.sprite.collide_rect(pipe_2,bird):
        game_over()
    if pygame.sprite.collide_rect(pipe_3,bird):
        game_over()
    if pygame.sprite.collide_rect(pipe_1_u,bird):
        game_over()
    if pygame.sprite.collide_rect(pipe_2_u,bird):
        game_over()
    if pygame.sprite.collide_rect(pipe_3_u,bird):
        game_over()
        
    
    if bird.alive()==False:
       game_over()
       
    

    # Update sprites
    all_sprites.update()
    screen.blit(background, (0, 0))
    screen.blit(background, (240, 0))
    screen.blit(background, (480, 0))
    
    
    if len(score_list)==0:
        
        text_surface = my_font.render('0', False, (0, 0, 0))
    
    elif len(score_list)>0:
        ac_dict={}
        ac_score=str(len(score_list)//2)
        ac_score_lis=[]
       
        for a in ac_score:
            ac_score_lis.append(str(a))
            
        keys=range(len(ac_score_lis))
        
        for i in keys:
            ac_dict[i]=ac_score_lis[i]
        
       
        
        for key,i in ac_dict.items():
            if i in score_file and bird.alive()==True:
                index_=ac_score_lis.index(i)
                
                screen.blit(pygame.image.load('./flappy-bird-assets/sprites/'+str(i)+'.png'),(360+20*key,0))
                
            if bird.alive()==False:
                
                screen.blit(pygame.image.load('./flappy-bird-assets/sprites/'+str(i)+'.png'),(360+16*key,250))
                
    

    
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()
    pygame.display.update()

    # Limit the frame rate to 60 FPS
    clock.tick(50)
    

# Quit Pygame
pygame.quit()
sys.exit()
