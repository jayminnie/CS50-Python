import pygame

pygame.init()
width,height = 1345,739
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

white = (255,255,255)
black = (0,0,0)
grey = (230,230,230)

def Text(size,str,center,x,y):
    font = pygame.font.Font("main_font.ttf",size)
    text = font.render(str,True,(0,0,0))
    text_rect = text.get_rect()
    if center == True:
        text_rect.center = (x,y)
    elif center == False:
        text_rect = x,y
    screen.blit(text,text_rect)
    return text,text_rect

def Instructions():
    instruction = True
    while instruction:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                instruction = False                
                        
        pygame.draw.rect(screen,grey,(width//2-420,height//2-300,850,600))
        pygame.draw.rect(screen,black,(width//2-420,height//2-300,850,600),5)
        Text(70,"About:",True,width//2, height//2-200)
        Text(50,"1. Press A to move left",True,width//2, height//2-130)
        Text(50,"2. Press D to move right",True,width//2, height//2-90)
        Text(50,"3. Avoid the red birds",True,width//2, height//2-50)
        Text(50,"4. Avoid falling from the screen",True,width//2, height//2-10)
        Text(50,"Grab as many coins for higher score",True,width//2, height//2+80)
        Text(50,"Click the volume button to stop/play music",True,width//2, height//2+120)
        Text(50,"Press any key to continue",True,width//2, height//2+200)
        pygame.display.update()
        clock.tick(5)

def Loss(score,high_score,account_name):
    pygame.mixer.Channel(0).stop()
    pygame.mixer.Channel(3).play(pygame.mixer.Sound('losing_sound.wav'))
    pygame.draw.rect(screen,grey,(width//2-300,height//2-105,600,300))
    pygame.draw.rect(screen,black,(width//2-300,height//2-105,600,300),5)
    Text(80,f"Game Over {account_name}!",True,width//2, height//2-10)
    Text(50,"Score: " + str(score),True,width//2-10, height//2+40)
    Text(50,"Press SPACE to restart",True,width//2, height//2+120)
    if account_name != "unknown":
        Text(50,"High Score: " + str(high_score),True,width//2, height//2+70)
    return score

def img_rect(img,x_value,y_value,center):
    image = img
    image_rect = image.get_rect()
    if center == True:
        image_rect.center = x_value,y_value
    else:
        image_rect.x = x_value
        image_rect.y = y_value
    return image_rect
