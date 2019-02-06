import os
import pygame
import sys
from random import shuffle
sys.argv.append("ex2.txt") #TODO: REMOVE


pygame.init()
pygame.key.set_repeat(70, 70)
size = WIDTH, HEIGHT = 400, 350
SIDE = 50
JUMP_K = 2
STEP = 10
CHANGE_SHEET_ID = 30
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
 

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        add = tiles_group
        if tile_type == "wall":
            add = walls_group
        elif tile_type == "empty":
            add = tiles_group
        elif tile_type == "hole":
            add = hole_group
        elif tile_type == "exit":
            add = exit_group
        
        super().__init__(add, all_sprites)
        image = tile_images[tile_type]
        if type(image) == type([]):
            shuffle(image)
            self.image = image[0]
        else:
            self.image = image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
    pass
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        down_frames = self.cut_sheet(player_down_image, 15, 1)
        up_frames = self.cut_sheet(player_up_image, 15, 1)
        right_frames = self.cut_sheet(player_right_image, 12, 1)
        left_frames = self.cut_sheet(player_left_image, 12, 1)
        
        self.all_frames = [down_frames, up_frames,
                           right_frames, left_frames] #down, up, right, left
        self.current_frames = self.all_frames[0]
        self.image = self.current_frames[0]
        self.current_frame = 0
        self.last_direction = [0, 0]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        
    def cut_sheet(self, sheet, columns, rows):
        frames = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        print("SIZE",sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                image = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                #print(self.rect.size)
                #image = pygame.transform.chop(image, (35, 38, 40, 40))
                frames.append(image)
        return frames
    
    def update(self, change_image=False, direction=None):
        if direction and self.last_direction != direction:
            self.current_frame = 0
            self.last_direction = direction
            if (self.last_direction[1] > 0) or self.last_direction == [0, 0]: #down
                self.current_frames = self.all_frames[0]
            elif self.last_direction[1] < 0: #up
                self.current_frames = self.all_frames[1]
            elif self.last_direction[0] > 0: #right
                self.current_frames = self.all_frames[2]
            elif self.last_direction[0] < 0: #left
                self.current_frames = self.all_frames[3]
            self.image = self.current_frames[0]
            self.mask = pygame.mask.from_surface(self.image)
        if change_image:
            self.current_frame = (self.current_frame + 1) % len(self.current_frames)
            self.image = self.current_frames[self.current_frame]
            #print(self.current_frame)
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


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == "X":
                Tile("hole", x, y)
            elif level[y][x] == "E":
                Tile("exit", x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            else:
                Tile("hole", x, y)            
    return new_player, x, y


FPS = 50
 
 
def terminate():
    pygame.quit()
    sys.exit()
 
 
def start_screen(count=0):
    intro_text = ["Ваша задача:",
                  "Выбраться отсюда",
                  "Попыток совершено:"+str(count)]
 
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
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


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
 
     # и подсчитываем максимальную длину     
    max_width = max(map(len, level_map))
 
    # дополняем каждую строку пустыми клетками ('.')    
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

  
def new_game(count):
    global running, camera, player, X, Y
    camera = Camera()
    running = True
    
    # sprites
    global all_sprites, tiles_group, walls_group, hole_group, player_group, exit_group
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group() #Grass
    walls_group = pygame.sprite.Group() # WALLS
    hole_group = pygame.sprite.Group() #DIE
    player_group = pygame.sprite.Group() #player
    exit_group = pygame.sprite.Group() #exit
    
    # player
    global player
    player = None
    
    try:
        name = sys.argv[1]
        player, X, Y = generate_level(load_level(name))
        start_screen(count)
    except Exception as e:
        print("Error....", e)
        running = False
    pass


def music():
    if not pygame.mixer.get_busy():
        path = os.path.abspath(os.curdir)+"\\data\\sound.mp3"
        print(path)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
    pass


'''
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group() # WALLS
hole_group = pygame.sprite.Group() #DIE
player_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
'''
tile_images = {
    'wall': load_dir('wall', count=1),
    'empty': load_dir("ground", count=1),
    "hole": load_dir("hole"),
    "exit": load_image("exit.png")
}
player_down_image = load_image("player\\player_down.png")
player_up_image = load_image("player\\player_down.png")
player_left_image = load_image("player\\player_left.png")
player_right_image = load_image("player\\player_right.png")
 
tile_width = tile_height = 50
count = 0 # number of attemps
new_game(count)
last_direction = [0, 0]
volume = 1

music()
pygame.time.set_timer(CHANGE_SHEET_ID, 500)

while running:
    coords = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False    
        elif event.type == CHANGE_SHEET_ID or player.last_direction != last_direction:
            player_group.update(True, last_direction)
        elif event.type == pygame.KEYDOWN:
            if event.key == 275 or event.key == 100: #right
                player.rect.x += STEP
                last_direction = [STEP, 0]
            elif event.key == 276 or event.key == 97: #left
                player.rect.x -= STEP
                last_direction = [-STEP, 0]
            if event.key == 274 or event.key == 115: #bottom
                player.rect.y += STEP
                last_direction = [0, STEP]
            elif event.key == 273 or event.key == 119: #top
                player.rect.y -= STEP
                last_direction = [0, -STEP]         
            elif event.key == 107: #suicideC
                running = False
                print("You killed yourself\nCongradulations!")
                count += 1
                new_game(count)
            elif event.key == 93:
                volume = (volume+0.1)%1
                pygame.mixer.music.set_volume(volume)
                pass
            elif event.key == 91:
                volume = (volume-0.1)%1
                pygame.mixer.music.set_volume(volume)                
                pass
            elif event.key == 32: #jump
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
                #print("WAAAAALL")
                player.rect.x -= last_direction[0]
                player.rect.y -= last_direction[1]
            if pygame.sprite.spritecollideany(player, hole_group):
                running = False
                print("Game Over")
                count += 1
                new_game(count)
                pass
            if pygame.sprite.spritecollideany(player, exit_group):
                running = False
                count += 1
                print("FINISHED", "COUNTS: "+str(count), sep="\n")
                pass

    all_sprites.update()
    camera.update(player)
    screen.fill(pygame.Color("black"))
    for sprite in all_sprites:
        camera.apply(sprite)
    tiles_group.draw(screen)
    walls_group.draw(screen)
    hole_group.draw(screen)
    exit_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
pygame.quit()