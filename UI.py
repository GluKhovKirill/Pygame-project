import os
import pygame
import sys
from random import shuffle
from lab import Transform


#screen's size
size = WIDTH, HEIGHT = 1152, 720
#Tiles' sizes
SIDE = 50
#Player's characteristics
JUMP_K = 2
STEP = 10
#Start_Sreen FPS
FPS = 50
TEXT_COLOR = "#2F17C7"
ATTEMPTS_COLOR = "#900000"
#Timers' IDs
CHANGE_SHEET_ID = 30
STABLE_ID = 31
# Time coeffficients
STABLE_T = 250
CHANGE_T = 150
#music volume
volume = 0.3
 
pygame.init()
pygame.key.set_repeat(70, 70)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        #default type == grass type
        add = tiles_group
        if tile_type == "wall":
            add = walls_group
        elif tile_type == "empty":
            #grass type
            add = tiles_group
        elif tile_type == "hole":
            #death tile type
            add = hole_group
        elif tile_type == "exit":
            add = exit_group
        elif tile_type == "check":
            add = tiles_group
        
        super().__init__(add, all_sprites)
        image = tile_images[tile_type]
        if type(image) == type([]):
            #set random texture
            shuffle(image)
            self.image = image[0]
        else:
            self.image = image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
    pass
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        #Different frames for different states
        stay_frames = self.cut_sheet(player_stay_image, 10, 1)
        right_frames = self.cut_sheet(player_right_image, 10, 1)
        left_frames = self.cut_sheet(player_left_image, 10, 1)
        self.all_frames = [right_frames, left_frames, stay_frames]
        
        self.stable_frames = 0
        self.staying = False
        self.last_dir_was_right = False
        
        self.current_frames = self.all_frames[0]
        self.image = self.current_frames[0]
        self.current_frame = 0
        self.last_direction = [0, 0]
        self.rect = self.image.get_rect().move(pos_x + 15, pos_y + 5)
        
    def cut_sheet(self, sheet, columns, rows):
        #Cutting image into frames
        frames = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            st = -1
            for i in range(columns):
                st += 1
                frame_location = ((self.rect.w * i)+st, self.rect.h * j)
                image = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                frames.append(image)
        return frames
    
    def update(self, change_image=False, direction=None, stay=None):
        if stay:
            #If player doesn't move
            self.current_frames = self.all_frames[2]
            self.image = self.current_frames[0]
            self.direction = [0, 0]
        if direction and self.last_direction != direction:
            #If player move and player changed his direction
            if self.last_direction[0] > 0:
                self.last_dir_was_right = True
            elif self.last_direction[0] < 0:
                self.last_dir_was_right = False
            self.current_frame = 0
            if (direction[0] > 0) or (direction[1] != 0 and self.last_dir_was_right):
                #vertivcal - right
                self.last_dir_was_right = True
                self.current_frames = self.all_frames[0]
            else:
                #vertical - left
                self.last_dir_was_right = False
                self.current_frames = self.all_frames[1]
            
            self.image = self.current_frames[0]
            self.mask = pygame.mask.from_surface(self.image)
            self.last_direction = direction
        if change_image:
            self.current_frame = (self.current_frame + 1) % len(self.current_frames)
            self.image = self.current_frames[self.current_frame]
            pass
    pass


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
            
    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)
           
        
def load_image(name, colorkey=None, add_data=True):
    #Loading one image
    fullname = name
    try:
        if add_data:
            fullname = os.path.join('data', name)
        image = pygame.image.load(fullname)
        
    except pygame.error as message:
        raise SystemExit(name)
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
        image = image.convert()
    else:
        image = image.convert_alpha()
    return image 


def load_dir(path, colorkey=None, count=-1):
    #Loading random files from dir (all if count==-1)
    try:
        path = os.path.join('data', path)
        files = os.listdir(path)
        files = map(lambda x: path+"\\"+x, files)
        files = list(filter(lambda x: ".png" in x or ".jpg" in x, files))
    except BaseException as e:
        print("Cannot open dir:", path)
        files = []
    shuffle(files)
    if count != -1:
        files = files[0:count]
    images = []

    try:
        for image_name in files:
            image = load_image(image_name, colorkey, False)
            images.append(image)
    except SystemExit as name:
        print('Cannot load image:', name)
    if len(images) == 1:
        images = images[0]
    return images


def generate_level(MAP):
    #Drawing level
    new_player, total_x, total_y = None, set(), set()
    for room in MAP:
        for strip in room:
            for block in strip:
                x, y, tile_type = block
                total_x.add(x)
                total_y.add(y)
                if tile_type == 'grass':
                    Tile('empty', x, y)
                elif tile_type == 'wall':
                    Tile('wall', x, y)
                elif tile_type == "hole":
                    Tile("hole", x, y)
                elif tile_type == "exit":
                    Tile('empty', x, y)
                    Tile("exit", x, y)
                elif tile_type == 'player':
                    Tile('empty', x, y)
                    new_player = Player(x, y)
                else:
                    Tile("hole", x, y)            
    return new_player, len(total_x), len(total_y)
 
 
def terminate():
    #Exit
    pygame.quit()
    sys.exit()
 
 
def start_screen(count=0):
    #Intro screen
    intro_text = ["Управление:",
                  "WASD/стрелки - перемещение",
                  "SPACE - прыжок",
                  "K - самоубийство",
                  "[ ], P - громкость, отключение/включение музыки",
                  "Попыток совершено: "+str(count)]
 
    bg = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = HEIGHT//2
    for i in range(len(intro_text)):
        if i == len(intro_text)-1:
            string_rendered = font.render(intro_text[i], 1, pygame.Color(ATTEMPTS_COLOR))
        else:
            string_rendered = font.render(intro_text[i], 1, pygame.Color(TEXT_COLOR))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
 
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  
        pygame.display.flip()
        clock.tick(FPS)
    pass

  
def new_game(count):
    #initializing a new game
    global running, camera, X, Y
    camera = Camera()
    running = True
    
    # sprites
    global all_sprites, tiles_group, walls_group, hole_group, player_group, exit_group
    all_sprites = pygame.sprite.Group()
    #Grass group
    tiles_group = pygame.sprite.Group()
    #Walls group
    walls_group = pygame.sprite.Group()
    #Death Tiles group
    hole_group = pygame.sprite.Group()
    #Player's group
    player_group = pygame.sprite.Group()
    #Exit group
    exit_group = pygame.sprite.Group()
    
    global player
    player = None
    
    try:
        player, X, Y = generate_level(Transform().trans(Transform().Transformer()))
        start_screen(count)
    except Exception as e:
        print("Error....", e)
        running = False
    pass


def music():
    #Loading and playing music
    if not pygame.mixer.get_busy():
        path = os.path.abspath(os.curdir)+"\\data\\sound.mp3"
        print(path)
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
    pass


#Tiles' textures
tile_images = {
    'wall': load_dir('wall', count=1),
    'empty': load_dir("ground", count=1),
    "hole": load_dir("hole"),
    "exit": load_image("exit.png"),
    "check": load_image("check.jpg")
}

#Different player's animations
player_stay_image = load_image("player\\player_stay.png")
player_left_image = load_image("player\\player_left.png")
player_right_image = load_image("player\\player_right.png")
 
count = 0 # number of attemps
new_game(count)
last_direction = [0, 0]


music()
pygame.time.set_timer(CHANGE_SHEET_ID, CHANGE_T)
pygame.time.set_timer(STABLE_ID, STABLE_T)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
        elif event.type == CHANGE_SHEET_ID or player.last_direction != last_direction:
            player_group.update(True, last_direction)
        elif event.type == STABLE_ID:
            player_group.update(False, None, True)
        elif event.type == pygame.KEYDOWN:
            if event.key == 275 or event.key == 100:
                #right
                pygame.time.set_timer(STABLE_ID, STABLE_T)
                player.rect.x += STEP
                last_direction = [STEP, 0]
            elif event.key == 276 or event.key == 97:
                #left
                pygame.time.set_timer(STABLE_ID, STABLE_T)
                player.rect.x -= STEP
                last_direction = [-STEP, 0]
            if event.key == 274 or event.key == 115:
                #bottom
                pygame.time.set_timer(STABLE_ID, STABLE_T)
                player.rect.y += STEP
                last_direction = [0, STEP]
            elif event.key == 273 or event.key == 119:
                #top
                pygame.time.set_timer(STABLE_ID, STABLE_T)
                pygame.time.set_timer(CHANGE_SHEET_ID, CHANGE_T)
                player.rect.y -= STEP
                last_direction = [0, -STEP]   
            else:
                if event.key == 107: 
                    #suicide ('K" button)
                    running = False
                    print("You killed yourself\nCongradulations!")
                    count += 1
                    new_game(count)
                elif event.key == 93:
                    #Increase music ("]" button)
                    volume = (volume+0.1)%1
                    pygame.mixer.music.set_volume(volume)
                    pass
                elif event.key == 91:
                    #Reduce music ("[" button")
                    volume = (volume-0.1)%1
                    pygame.mixer.music.set_volume(volume)                
                    pass
                elif event.key == 112:
                    #Mute/unmute ("P" button)
                    if pygame.mixer.music.get_volume():
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(volume)
                elif event.key == 32:
                    #jump
                    if last_direction[0]:
                        player.rect.x += int((last_direction[0]//abs(last_direction[0])) * SIDE)
                        if pygame.sprite.spritecollideany(player, walls_group):
                            player.rect.x -= int((last_direction[0]//abs(last_direction[0])) * SIDE)
                        else:
                            player.rect.x += int((last_direction[0]//abs(last_direction[0])) * SIDE * (JUMP_K-1))
                            last_direction[0] = int((last_direction[0]//abs(last_direction[0])) * SIDE * JUMP_K)
                    if last_direction[1]:
                        player.rect.y += int((last_direction[1]//abs(last_direction[1])) * SIDE)
                        if pygame.sprite.spritecollideany(player, walls_group):
                            player.rect.y -= int((last_direction[1]//abs(last_direction[1])) * SIDE)
                        else:
                            player.rect.y += int((last_direction[1]//abs(last_direction[1])) * SIDE * (JUMP_K-1))
                            last_direction[1] = int((last_direction[1]//abs(last_direction[1])) * SIDE * JUMP_K)
                        
            if pygame.sprite.spritecollideany(player, walls_group):
                player.rect.x -= last_direction[0]
                player.rect.y -= last_direction[1]
            if pygame.sprite.spritecollideany(player, hole_group):
                running = False
                print("Game Over")
                count += 1
                new_game(count)
                pass
            if pygame.sprite.spritecollideany(player, exit_group) or not pygame.sprite.spritecollideany(player, tiles_group):
                running = False
                count += 1
                print("FINISHED", "COUNTS: "+str(count), sep="\n")

            
    screen.fill(pygame.Color("black"))     
    all_sprites.update()
    player_group.update(False, last_direction)
    camera.update(player)
    
    for sprite in all_sprites:
        camera.apply(sprite)
        
    tiles_group.draw(screen)
    walls_group.draw(screen)
    hole_group.draw(screen)
    exit_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    pass

    
pygame.quit()