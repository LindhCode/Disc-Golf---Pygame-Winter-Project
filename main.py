import pygame
import math
import time

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Button(pygame.sprite.Sprite):
    def __init__(self, x,y,image,scale):
        super().__init__
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    
    def draw(self):
        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mourseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                return True
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Disc():
    def __init__(self,x,y,image,distance,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.circle = self.image.get_rect()
        self.circle.topleft = (x,y)
        #Power rectangle
        self.clicked = False
        self.start_width = None
        self.start_height = None
        self.x = x
        self.y = y
        #Shooting the disc
        self.power = 0    
    def draw(self):
        '''Creating the power rectangle for the disc'''
        #get mouse position
        pos = pygame.mouse.get_pos()
        if self.circle.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                if self.clicked == False:
                    self.start_height = pos[1]
                    self.start_width = pos[0]
                self.clicked = True
        if self.clicked:
            #rectangle surface
            dx = pos[0] - (self.start_width)
            dy = pos[1] - self.start_height
            rect_width = 25
            rect_height = math.hypot(dx,dy)
            rect_color = math.hypot(dx,dy) + 100
            if rect_height < abs(dx):
                rect_height = abs(dx)
            if rect_height > 150:
                rect_height = 150
                rect_color = 250
            # Power variable
            self.power = rect_height

            surf_w = rect_width
            surf_h = rect_height * 2
            rect_surf = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
            pygame.draw.rect(rect_surf, (rect_color,0,0), (0,0, rect_width, rect_height))
            
            #rectangle angle
            angle = math.degrees(math.atan2(-dy, dx))

            #rotate the surface
            rotated_surf = pygame.transform.rotate(rect_surf, angle-90)
            rotated_rect = rotated_surf.get_rect(center=(self.x + 30, self.start_height))
            screen.blit(rotated_surf, rotated_rect)

        if pygame.mouse.get_pressed()[0] == False:
            self.clicked = False
        screen.blit(self.image, (self.circle.x, self.circle.y))
        return self.power

    def shoot(self):
        pos = pygame.mouse.get_pos()
        if self.circle.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]:
                if self.clicked == False:
                    print("Vi förbereder skott!")
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == False:
            print("Skott!")
            self.clicked = False
        screen.blit(self.image, (self.circle.x, self.circle.y))
scene = {
    "main_menu" : True,
    "level_1" : False
}
'''MAIN MENU SCENE'''
power_button_img = pygame.image.load("power-button.png").convert_alpha()
power_button = Button(100,200,power_button_img, 2)

'''LEVEL 1 SCENE'''
disc_img = pygame.image.load("disc.png").convert_alpha()
disc = Disc(200,300,disc_img,"midrange", 2)

'''TIME'''
prev_time = time.time()

run = True
while run:
    # Limit frame rate to 60 fps
    pygame.time.Clock().tick(60)
    '''Time'''
    now = time.time()
    dt = now - prev_time
    prev_time = now
    #print(now)



    if scene["main_menu"]:
        screen.fill((220,220,220))
        if power_button.draw() == True:
            scene["level_1"] = power_button.draw()
            scene["main_menu"] = False
        

    if scene["level_1"]:
        screen.fill((202,228,241))
        disc.draw()
        if disc.power > 0 and disc.clicked == False:
            print("Skott!")


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()



