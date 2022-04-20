import pygame
import random

pygame.init()
L = 960
H = 540
win = pygame.display.set_mode((L,H))
pygame.display.set_caption("Game 1")
run = True
touch = False
pos = 0
clock = pygame.time.Clock()


class pg(object):
    def __init__(self,x,y,width,height,speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.jump = False
        self.floor = True
        self.jumpCount = 15
        self.fallCount = 1
        self.HP = 100
        self.bull = False
        self.bang = False
        self.damage = 5
        self.dir = 1
        self.bullet = 0
        self.score = 0
        
    def draw(self, win):
        pygame.draw.rect(win, (255,0,0),(self.x,self.y,self.width,self.height))

    def shot(self):
        if self.bull == False:
            self.bullet = Bullet(self.x,self.y+int(self.height/2),10,5,(255,117,20),20,self.dir,self.damage,Sas)
            self.bull = True
        self.bang = True
        self.bullet.shot(win,Giotto)
        if self.bullet.x <= -self.bullet.width or self.bullet.x >= L:
            self.bang = False
            self.bull = False

class enemy(object):
    def __init__(self,x,y,width,height,speed,damage,HP):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.jump = False
        self.floor = False
        self.jumpCount = 15
        self.fallCount = 1
        self.actions = True
        self.can = True
        self.mov = 1
        self.point = 0
        self.near = 5
        self.ult = False
        self.bull = False
        self.Bullet = 0
        self.dir = 0
        self.bang = False
        self.damage = damage
        self.HP = HP
        self.buff = 0

    def draw(self, win):
        pygame.draw.rect(win, (255,0,255),(self.x,self.y,self.width,self.height))

    def move(self):
        if self.actions  == True:
            if self.can == True:
                self.mov = random.randint(1,5)
            if self.mov == 1:
                if self.can == True:
                    self.point = random.randrange(100, 900,self.speed)
                if self.x < self.point:
                    self.x += self.speed
                    self.can = False
                    self.mov = 1
                    self.dir = 1
                elif self.x > self.point:
                    self.x -= self.speed
                    self.can = False
                    self.mov = 1
                    self.dir = -1
                else:
                    self.can = True
            elif self.mov == 2:
                if self.jump == False and self.floor == True:
                    self.jump = True
                    self.jumpCount = 15
            elif self.mov == 3:
                if self.x < Giotto.x and self.near != 0:
                    self.x += self.speed
                    self.can = False
                    self.mov = 3
                    self.near -= 1
                    self.dir = 1
                elif self.x > Giotto.x and self.near != 0:
                    self.x -= self.speed
                    self.can = False
                    self.mov = 3
                    self.near -= 1
                    self.dir = -1
                else:
                    self.near = 5
                    self.can = True
            elif self.mov == 4 and self.dir != 0:
                self.bang = True
                
            elif self.mov == 5 and self.ult == False:
                self.jumpCount *= 3
                self.damage *= 2
                self.ult = True

    def shot(self):
        if self.bull == False:
            self.bullet = Bullet(self.x,self.y+int(self.height/2),10,5,(255,117,20),20,self.dir,self.damage, Giotto)
            self.bull = True
        self.bang = True
        self.bullet.shot(win,Sas)
        if self.bullet.x <= -self.bullet.width or self.bullet.x >= L:
            self.bang = False
            self.bull = False

    def death(self):
        Giotto.score += 100
        self.buff += 10
        

class Bullet(object):
    def __init__(self,x,y,width,height,color,speed,direction,damage,target):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.direction = direction
        self.damage = damage
        self.target = target

    def shot(self, win, champ):
        if self.x >= -self.width and self.x <= L:
            if self.direction == 1:
                self.x += self.speed
            elif self.direction == -1:
                self.x -= self.speed

            if Hitbox(self,self.target):
                self.target.HP -= self.damage
                champ.bull = False
                champ.bang = False
                
            pygame.draw.rect(win, self.color,(self.x,self.y,self.width,self.height))
        
class button(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self, win):
        pygame.draw.rect(win, (128,128,128),(self.x,self.y,self.width,self.height))

class ground(object):
    def __init__(self,x,y,width,height,color,speed,direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.direction = direction
        

    def move(self, win, x0, x1, champ):
        self.x0 = x0
        self.x1 = x1
        if self.direction == 1:
            if self.x + self.speed <= self.x1:
                self.x += self.speed
                if self == Hbox(champ) and champ.floor == True and champ.jump == False and self.x != self.x1:
                    champ.x += self.speed
                    champ.fallCount = 1
                if self.x == self.x1:
                    if self == Hbox(champ):
                        champ.fallCount = 1
                        
                        champ.x -= self.speed
                    self.direction = -1
        elif self.direction == -1:
            if self.x - self.speed >= self.x0:
                self.x -= self.speed
                if self == Hbox(champ) and champ.floor == True and champ.jump == False and self.x != self.x0:
                    champ.x -= self.speed
                    champ.fallCount = 1
                if self.x == self.x0:
                    if self == Hbox(champ):
                        champ.fallCount = 1
                        champ.x += self.speed
                    self.direction = 1

        pygame.draw.rect(win, self.color,(self.x,self.y,self.width,self.height))
        
    
    def draw(self, win):
        pygame.draw.rect(win, self.color,(self.x,self.y,self.width,self.height))

class Bar(object):
    def __init__(self,x,y,width,height,life):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.life = life

    def draw(self, win, life,x,y):
        self.x = x
        self.y = y
        self.life = life
        if self.life > 0:
            pygame.draw.rect(win, (0,255,0),(self.x,self.y,self.life,self.height))
        if self.width != self.life and self.life > 0:
            pygame.draw.rect(win, (255,0,0),(self.x+self.life,self.y,self.width-self.life,self.height))

def Hbox(champ):
    G = [Grass, Block1, Block2, Block3, Block4]
    F1, F2 = [], []
    for g in G:
        if (champ.x < g.x+g.width and champ.x+champ.width > g.x) and (g.y-champ.y >= champ.height):
            F1.append(g)
            F2.append(g.y - champ.y)
    try:
        f2 = F2.index(min(F2))
        f1 = F1[f2]
    except:
        f1 = Grass
    return f1

def Hitbox(champ1, champ2):
    if (champ1.x <= champ2.width+champ2.x and champ1.x >= champ2.x) and ((champ1.y <= champ2.height+champ2.y and champ1.y >= champ2.y) or (champ1.y+champ1.height <= champ2.height+champ2.y and champ1.y+champ1.height >= champ2.y)):
        return True
    elif (champ1.x+champ1.width <= champ2.width+champ2.x and champ1.x++champ1.width >= champ2.x) and ((champ1.y <= champ2.height+champ2.y and champ1.y >= champ2.y) or (champ1.y+champ1.height <= champ2.height+champ2.y and champ1.y+champ1.height >= champ2.y)):
        return True
    else:
        return False
        
def Selection(run, touch):
    Pause = True
    while Pause:
        clock.tick(27)
        Resume.draw(win)
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch = True
            if event.type == pygame.MOUSEBUTTONUP:
                touch = False
            if event.type == pygame.QUIT:
                run = False
        if run == False:
            pygame.quit()
        if touch == True:
            pos = pygame.mouse.get_pos()
            if pos[0]<=Resume.x+Resume.width and pos[0]>=Resume.x and pos[1]<=Resume.y+Resume.height and pos[1]>=Resume.y:
                Pause = False
    return run, touch


def redraw():
    win.fill((0,0,0))
    Giotto.draw(win)
    Sas.draw(win)
    Jump.draw(win)
    Left.draw(win)
    Right.draw(win)
    Shoot.draw(win)
    Menu.draw(win)
    Grass.draw(win)
    Block1.draw(win)
    Block2.draw(win)            
    Block3.draw(win)
    Block4.move(win,400,850,Giotto)
    if Sas.bang == True:
        Sas.shot()
    if Giotto.bang == True:
        Giotto.shot()
    Baz.draw(win,Giotto.HP,10,10)
    Bas.draw(win,Sas.HP,Sas.x-5-int(Sas.buff/2),Sas.y-10)
    if Sas.HP <= 0:
        Sas.death()
        Sas.x = L - 40
        Sas.y = H - 70
        Sas.HP = 50 + Sas.buff
        Bas.life = Sas.HP
        Bas.width = Sas.HP
    
    font = pygame.font.Font(None, 36)
    text = font.render("Score: "+str(Giotto.score), 1, (255, 255, 255))
    win.blit(text, (L-190,10))
    
    pygame.display.update()
    if Giotto.HP <= 0:
        Restart()

def Restart():
    start = True
    touch = False
    while start:
        tart = True
        clock.tick(27)
        Retry.draw(win)
        Quit.draw(win)
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch = True
            if event.type == pygame.MOUSEBUTTONUP:
                touch = False
            if event.type == pygame.QUIT:
                tart = False
        if tart == False:
            pygame.quit()
            quit()
        if touch == True:
            pos = pygame.mouse.get_pos()
            if pos[0]<=Retry.x+Retry.width and pos[0]>=Retry.x and pos[1]<=Retry.y+Retry.height and pos[1]>=Retry.y:
                Giotto.x = 0
                Giotto.y = H-50
                Giotto.jump = False
                Giotto.HP = 100
                Giotto.score = 0
                Giotto.bullet = 0
                Giotto.bang = 0
                Baz.life = Giotto.HP
                Sas.x = L - 40
                Sas.y = H - 70
                Sas.HP = 50
                Sas.buff = 0
                Sas.jump = False
                Sas.floor = True
                Sas.ult = False
                Sas.bull = False
                Sas.Bullet = 0
                Sas.bang = False
                Sas.damage = 5
                Sas.jumpCount = 15
                Bas.life = Sas.HP
                Bas.width = Sas.HP
                Block4.x = int(L/2)

                start = False
            
            if pos[0]<=Quit.x+Quit.width and pos[0]>=Quit.x and pos[1]<=Quit.y+Quit.height and pos[1]>=Quit.y:
                pygame.quit()
                quit()


Giotto = pg(0, H-50, 60, 40, 10)
Baz = Bar(10, 10, Giotto.HP, 15, Giotto.HP)
Sas = enemy(L-40, H-70, 40, 60, 10, 5, 50)
Bas = Bar(Sas.x-5,Sas.y-10,Sas.HP,5,Sas.HP)
Jump = button(L-120, H-110, 50, 50)
Left = button(10, H-110, 50, 50)
Right = button(70, H-110, 50, 50)
Shoot = button(L-60, H-110, 50, 50)
Menu = button(L-50,10,40,40)
Resume = button(int(L/2)-50,50,100,40)
Retry = button(int(L/2)-50,int(H/2)-50,100,40)
Quit = button(int(L/2)-50,int(H/2)+50,100,40)
Grass = ground(0, H-10, L, 10,(0,255,0),0,0)
Block1 = ground(200, H-100, 100, 10,(0,128,255),0,0)
Block2 = ground(L-300, H-100, 100, 10,(0,128,255),0,0)
Block3 = ground(150, H-200, 100, 10,(0,128,255),0,0)
Block4 = ground(int(L/2), H-200, 100, 10,(0,128,255),5,1)

Champions = [Giotto, Sas]


while run:
    clock.tick(27)
    
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            touch = True
        if event.type == pygame.MOUSEBUTTONUP:
            touch = False
        if event.type == pygame.QUIT:
            run = False
#    keys = pygame.key.get_pressed()
#    if keys[pygame.K_LEFT]:
#        if Giotto.x>0:
#            Giotto.x -= Giotto.speed
#            Giotto.dir = -1
#            if Giotto.jump == False:
#                Giotto.floor = False
#    if keys[pygame.K_RIGHT]:
#        if Giotto.x<L-Giotto.width:
#            Giotto.x += Giotto.speed
#            Giotto.dir = 1
#            if Giotto.jump == False:
#                Giotto.floor = False
#    if keys[pygame.K_UP]:
#        Giotto.jump = True
#        Giotto.jumpCount = 15
#    if keys[pygame.K_DOWN] and Giotto.dir != 0:
#        Giotto.bang = True
    
    if touch == True:
        pos = pygame.mouse.get_pos()

        if pos[0]<=Menu.x+Menu.width and pos[0]>=Menu.x and pos[1]<=Menu.y+Menu.height and pos[1]>=Menu.y:
            Sel = Selection(run, touch)
            run = Sel[0]
            touch = Sel[1]
                
        if pos[0]<=Left.x+Left.width and pos[0]>=Left.x and pos[1]<=Left.y+Left.height and pos[1]>=Left.y:
            if Giotto.x>0:
                Giotto.x -= Giotto.speed
                Giotto.dir = -1
                if Giotto.jump == False:
                    Giotto.floor = False
                
        if pos[0]<=Right.x+Right.width and pos[0]>=Right.x and pos[1]<=Right.y+Right.height and pos[1]>=Right.y:
            if Giotto.x<L-Giotto.width:
                Giotto.x += Giotto.speed
                Giotto.dir = 1
                if Giotto.jump == False:
                    Giotto.floor = False
                
        if pos[0]<=Jump.x+Jump.width and pos[0]>=Jump.x and pos[1]<=Jump.y+Jump.height and pos[1]>=Jump.y and Giotto.jump == False and Giotto.floor == True:
            Giotto.jump = True
            Giotto.jumpCount = 15
        if pos[0]<=Shoot.x+Shoot.width and pos[0]>=Shoot.x and pos[1]<=Shoot.y+Shoot.height and pos[1]>=Shoot.y:
            Giotto.bang = True
            
    Sas.move()
            
    for champ in Champions:
        if champ.jump == True:
            champ.floor = False
            champ.fallCount = 1
            if champ.y >= champ.jumpCount:
                champ.y -= champ.jumpCount
            else:
                champ.jumpCount = 0
            champ.jumpCount -= 1
            if champ.jumpCount == -1:
                champ.jump = False
                    
        if (champ.x+champ.width < Hbox(champ).x)or(champ.x > Hbox(champ).x+Hbox(champ).width):
            champ.floor = False
            champ.fallCount = 1
                
        if champ.floor == False or champ.y+champ.height != Hbox(champ).y:      
            if champ.y < Hbox(champ).y-champ.height-champ.fallCount:
                champ.y += champ.fallCount
                champ.fallCount += 1
            else:
                champ.y = Hbox(champ).y-champ.height
                champ.floor = True
                champ.fallCount = 1
    redraw()

pygame.quit()

    
