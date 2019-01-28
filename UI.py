import os
import pygame
import sys
sys.argv.append("ex2.txt") #TODO: REMOVE


pygame.init()
pygame.key.set_repeat(70, 70)
size = WIDTH, HEIGHT = 400, 350
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
 

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image 


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
    # ������������ ������������, �� ���������� ������������ �������� �� ��������������            
    return new_player, x, y



FPS = 50
 
 
def terminate():
    pygame.quit()
    sys.exit()
 
 
def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "ПРАВИЛА ИГРЫ",
                  "КТО-НИБУДЬ ИХ ЗНАЕТ?"]
 
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

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
    "hole": load_image("hole.png"),
    "exit": load_image("exit.png")
}
player_image = load_image('mario.png')
 
tile_width = tile_height = 50
# player
player = None
 
# sprites
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group() #Grass
walls_group = pygame.sprite.Group() # WALLS
hole_group = pygame.sprite.Group() #DIE
player_group = pygame.sprite.Group() #player
exit_group = pygame.sprite.Group() #exit



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

        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
    pass
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
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
        '''
        if obj.rect.x > WIDTH+50:
            obj.rect.x -= (X+1)*50
        elif obj.rect.x < -50:
            obj.rect.x += (X+1)*50
        
        if obj.rect.y > HEIGHT+50:
            obj.rect.y -= (Y+1)*50
        elif obj.rect.y < -50:
            obj.rect.y += (Y+1)*50   
        '''

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)
#====================================   
camera = Camera()
running = True
try:
    name = sys.argv[1]
    player, X, Y = generate_level(load_level(name))
    start_screen()
except Exception as e:
    print("Error....", e)
    running = False

'''
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group() # WALLS
hole_group = pygame.sprite.Group() #DIE
player_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
'''


while running:
    coords = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False             
        elif event.type == pygame.KEYDOWN:
            last_x, last_y = 0, 0
            if event.key == 275:
                player.rect.x += 10
                last_x += 10
            elif event.key == 276:
                player.rect.x -= 10
                last_x -= 10
            if event.key == 274:
                player.rect.y += 10
                last_y += 10
            elif event.key == 273:
                player.rect.y -= 10
                last_y = -10
                
            if pygame.sprite.spritecollideany(player, walls_group):
                player.rect.x -= last_x
                player.rect.y -= last_y
            if pygame.sprite.spritecollideany(player, hole_group):
                running = False
                print("Game Over")
                pass
            if pygame.sprite.spritecollideany(player, exit_group):
                running = False
                print("FINISHED")
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