import pygame,random,math,sys,csv,os,re
from gui import Text,Instructions,Loss,img_rect

class Lives:
    def __init__(self,lives=[]):
        self.lives = lives

    def withdraw(self,n):
        self.lives = []
        for i in range(n):
            self.lives.append(pygame.image.load("heart.png"))
        return self.lives

class Cat(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.velocity = 0
        self.image = pygame.image.load("cat.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        scroll = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5

        self.velocity += gravity
        self.rect.y += (self.velocity + scroll)

        for block in block_group:
            if block.rect.colliderect(self.rect.x,self.rect.y+self.velocity,self.rect.w,self.rect.h):
                if self.rect.bottom < block.rect.centery:
                    if self.velocity > 0:
                        self.rect.bottom = block.rect.top
                        self.velocity = -21

        if self.rect.top <= scroll_thresh:
            if self.velocity <= 0:
                scroll = -self.velocity

        return scroll

class Blocks(pygame.sprite.Sprite):
    def __init__(self,x,y,width,move):
        super().__init__()
        self.image = pygame.image.load("grass.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.w = width
        self.move = move
        self.speed = random.choice([1,2])
        self.dir = random.choice([-1,1])
        self.counter = random.randint(0,50)

    def update(self,scroll):
        if self.move == True:
            self.rect.x += self.dir
            self.counter += 1

        if self.counter >= 150 or self.rect.left <= 372 or self.rect.right >= 972:
            self.dir *= -1
            self.counter = 0

        self.rect.y += scroll
        if self.rect.top > height:
            self.kill()

        return self.counter,self.dir

class Enemy(pygame.sprite.Sprite):
    def __init__(self,enemy_image,x_pos,y_pos):
        super().__init__()
        self.rect = pygame.Rect(x_pos,y_pos,100,53)
        self.direction = random.choice([1,-1])

        if self.direction == 1:
            self.flip = False
            self.rect.x = x_pos
        elif self.direction == -1:
            self.flip = True
            self.rect.x = width

        image_load = pygame.image.load(enemy_image)
        image = pygame.transform.flip(image_load,self.flip,False)
        self.image = image

    def update(self,scroll):
        self.rect.x += self.direction * 3
        self.rect.y += scroll
        if self.rect.right < 0 or self.rect.left > width or self.rect.top > height:
            self.kill()

class Coins(pygame.sprite.Sprite):
    def __init__(self,x,y,move):
        super().__init__()
        self.sprites = []
        self.is_animating = False
        self.move = move

        for i in range(6):
            self.sprites.append(pygame.image.load(f"coin{i}.png"))

        self.frame = 0
        self.image = self.sprites[self.frame]

        self.rect = self.image.get_rect()
        self.rect.center = x,y

    def animate(self):
        self.is_animating = True

    def update(self,scroll):
        if self.is_animating == True:
            self.frame += 0.2

            if self.frame >= len(self.sprites):
                self.frame = 0

            self.image = self.sprites[int(self.frame)]

        self.rect.y += scroll

scroll_thresh = 300
gravity = 1
width,height = 1345,739
white = (255,255,255)
black = (0,0,0)
grey = (230,230,230)

def main():
    global scroll,login,block_group
    while True:
        try:
            exist = input('Hi, enter "N" if you are new, "E" if you have an existing account, or press [ENTER] to start straightaway: ')
            if exist.strip(' ') == "N":
                while True:
                    try:
                        new_user = input("Create your username: ")
                        if valid_name(new_user) == True:
                            account_name = new_user
                            password = input("Create your password: ")
                            p_counter = 3
                            while valid_password(password,p_counter) != True:
                                print(valid_password(password,p_counter))
                                password = input("Create your password: ")
                                p_counter -= 1
                            user_login(account_name,password)
                            print(f"Welcome {account_name}. Click the cat's face to start.")
                            break
                    except NameError:
                        print("Only numbers, lowercase-letters and underscores can be used.")
                        print("Username should have min. 4 characters & max. 6.")
                        pass
                    except ValueError:
                        print("Username taken. Try again")
                        pass
            elif exist.strip(' ') == "E":
                e_counter = 2
                while True:
                    try:
                        account_name = input("Type in your username: ")
                        account_pass = input("Type in your password: ")
                        is_account = account_login(account_name,account_pass)
                        if exist_account(e_counter,is_account) == True:
                            print(f"Welcome back {account_name}. Click the cat's face to start")
                            break
                    except ValueError:
                        print(f"Wrong username or password. You have {e_counter} more tries.")
                        e_counter -= 1
                        pass
            elif exist == '':
                account_name = "unknown"
                print("Click the cat's face to start the game. Your score will not be recorded.")
                break
            else:
                print("Unknown input. Try again.")
                sys.exit()
        except KeyError:
            pass
        except EOFError:
            sys.exit("\nBye!")
        else:
            break

    pygame.init()
    lives = Lives()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Jumpy Kitty")
    icon = pygame.image.load("caticon.png")
    backg = pygame.image.load("background.png").convert_alpha()
    pygame.display.set_icon(icon)

    mark_image = pygame.image.load("help.png")
    on_image = pygame.image.load("von.png")
    off_image = pygame.image.load("voff.png")
    start_image = pygame.image.load("start.png")
    quit_image = pygame.image.load("quit.png")

    on_rect = on_image.get_rect()
    off_rect = off_image.get_rect()

    max_blocks = 20
    block_group = pygame.sprite.Group()
    block = Blocks(width/2,height-100,80,False)
    block_group.add(block)
    tiles = math.ceil(width / width) + 1

    coin_group = pygame.sprite.Group()

    cat = Cat(width/2,height-200)
    cat_group = pygame.sprite.Group()
    cat_group.add(cat)

    max_enemies = 5
    enemy_image = ("enemy.png")
    enemy_group = pygame.sprite.Group()

    positions = []
    scroll = 0
    cat_health = 5
    bg_scroll = 0
    seconds = 0
    score = 0
    volume = True
    game_over = False
    login = True

    pygame.mixer.Channel(0).play(pygame.mixer.Sound('8bit_sound.mp3'),-1)
    start_rect = img_rect(start_image,width//2 - 250,height//2 + 50,False)
    quit_rect = img_rect(quit_image,width//2 + 50,height//2 + 50,False)
    mark_image_rect= img_rect(mark_image,40,700,True)

    running = True
    while running:
        clock.tick(60)
        if game_over == False and login == False:
            a = 0
            seconds += (1/60)

            scroll = cat.update()

            screen.blit(backg,(0,0 + bg_scroll))
            screen.blit(backg,(0,-height + bg_scroll))
            if bg_scroll < height:
                bg_scroll = 0
            else:
                bg_scroll += scroll

            if len(block_group) < max_blocks:
                for block in block_group:
                    pos_w = block.rect.w
                    pos_x = random.randint(372,972-pos_w)
                    pos_y =  block.rect.y - random.randint(80,95)
                    num = random.randint(1,3)
                    if num == 3 and score > 50:
                        b_move = True
                    else:
                        b_move = False

                coin = Coins(pos_x+40,pos_y-20,b_move)
                block = Blocks(pos_x,pos_y,pos_w,b_move)
                block_group.add(block)
                coin_group.add(coin)

            if len(enemy_group) < max_enemies:
                enemy = Enemy(enemy_image,0,random.randint(100,700))
                enemy_group.add(enemy)

            Text(50,"Lives left:",False,20,20)
            #IMPLEMENT SCORE ONLY WHEN COLLIDING ON FURTHER TILES
            size = 50
            if score >= 100000:
                size = 45

            Text(50,"Score: ",False,1120,20)
            Text(size,str(math.ceil(score)),False,1240,20)

            hearts = lives.withdraw(cat_health)

            for life in hearts:
                a += 70
                screen.blit(life,(150 + a,20))

            if pygame.sprite.groupcollide(cat_group,enemy_group,False,True):
                cat_health -= 1
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('ouch.mp3'))

            if pygame.sprite.groupcollide(cat_group,coin_group,False,True):
                score += 5
                pygame.mixer.Channel(2).play(pygame.mixer.Sound('beep.mp3'))

            block_group.update(scroll)
            coin_group.update(scroll)
            cat_group.draw(screen)
            block_group.draw(screen)
            coin_group.draw(screen)
            coin.animate()

            if score >= 150:
                enemy_group.draw(screen)
                enemy_group.update(scroll)
            cat_group.update()

            if seconds < 1:
                pygame.draw.rect(screen,grey,(width//2-300,height//2-40,600,80))
                pygame.draw.rect(screen,black,(width//2-300,height//2-40,600,80),4)
                Text(50,"CLICK ? FOR HELP",True,width//2,height//2)

            for block in block_group:
                if cat.rect.bottom == block.rect.top or cat.rect.colliderect(block.rect):
                    positions.append(block.rect)

            if cat_health <= 0:
                game_over = True
                if account_name != "unknown":
                    high_score = score_counter(account_name,math.ceil(score))
                else:
                    high_score = 0
                Loss(math.ceil(score),high_score,account_name)

            if volume == True:
                off_rect.center = (0,0)
                on_rect.center = (120,700)
                screen.blit(on_image,on_rect)
            elif volume == False:
                on_rect.center = (0,0)
                off_rect.center = (120,700)
                screen.blit(off_image,off_rect)
            screen.blit(mark_image,mark_image_rect)

            if cat.rect.top >= height and cat_health > 0:
                cat_health -= 1
                pygame.mixer.Channel(1).play(pygame.mixer.Sound('ouch.mp3'))
                cat.rect.center = (positions[-1].x,positions[-1].y-100)

        elif game_over == False and login == True:
            for i in range(0,tiles):
                screen.blit(backg,(i*width + scroll,0))

            scroll -= 5
            if abs(scroll) >= width:
                scroll = 0

            screen.blit(start_image,start_rect)
            screen.blit(quit_image,quit_rect)
            Text(100,"Welcome to Jumpy Kitty",True,width//2,height//2-150)
            Text(50,"Click [START] to begin",True,width//2,height//2-80)
            Text(50,"About & Instructions",False,mark_image_rect.x+70,mark_image_rect.y)
            screen.blit(mark_image,mark_image_rect)

        elif game_over == True and login == False:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound('8bit_sound.mp3'),-1)
                game_over = False
                cat_health = 5
                volume = True
                score = 0
                scroll = 0
                cat.rect.center = (width/2,height-200)
                block_group.empty()
                block = Blocks(width/2,height-100,80,False)
                block_group.add(block)
                enemy_group.empty()
                coin_group.empty()

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_rect.collidepoint(event.pos):
                    running = False
                if start_rect.collidepoint(event.pos):
                    login = False
                if mark_image_rect.collidepoint(event.pos):
                    Instructions()
                if on_rect.collidepoint(event.pos):
                    volume = False
                    pygame.mixer.Channel(0).pause()
                elif off_rect.collidepoint(event.pos):
                    volume = True
                    pygame.mixer.Channel(0).unpause()

        pygame.time.delay(20)
        pygame.display.update()

    pygame.quit()
    sys.exit()

def valid_name(name):
    if matches := re.fullmatch(r"[a-z0-9_]{4,6}",name):
        availability_n = name_available(name)
        if availability_n == False:
            raise ValueError
        else:
            return True
    else:
        raise NameError

def score_counter(acc_n,score):
    file_exists = os.path.isfile('scores.csv')
    with open('scores.csv','a+') as csvfile:
        fieldnames = ['username','score']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({'username':acc_n,'score':score})

    scores = []
    with open("scores.csv","r") as csvfile:
        lines = csv.DictReader(csvfile)
        for row in lines:
            if acc_n == row['username']:
                scores.append(int(row['score']))

    return max(scores)

def valid_password(passw,p_counter):
    if matches := re.search(r".{7,}",passw):
        return True
    if p_counter == 0:
        raise KeyError
    else:
        message = f"Your password should have at least 7 characters."
        return message

def name_available(name):
    file_exists = os.path.isfile('users.csv')
    available = True
    if file_exists:
        with open('users.csv','r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if name == row['usernames']:
                    available = False
            return available
    else:
        return available

def account_login(acc_name,acc_pass):
    file_exists = os.path.isfile('users.csv')
    account = False
    if file_exists:
        with open('users.csv','r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if acc_name == row['usernames']:
                    if acc_pass == row['keys']:
                        account = True
            return account
    else:
        return account

def exist_account(e_counter,is_account):
    if is_account == True:
        return True
    elif e_counter > 0:
        raise ValueError
    else:
        raise KeyError

def user_login(name,passw):
    file_path = os.path.isfile('users.csv')
    with open('users.csv','a+') as csvfile:
        fieldnames = ['usernames','keys']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_path:
            writer.writeheader()
        writer.writerow({'usernames':name,'keys':passw})

if __name__ == "__main__":
    main()