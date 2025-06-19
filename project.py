import pygame
#from pygame.locals import
from pygame import mixer
import levels



pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1300
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('The Game')


#define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)




#define game variables
tile_size = 50  
game_over = 0
main_menu = True
collection_menu = False
levels_menu = False
cur_locked_level = 2 #has to be 2 by defalt
cur_level = 1
max_levels = 10
cur_level_score = 0

# stats
saved_score = 0
cur_bullet_stats = 0
cur_dead_stats = 0
is_cur_door_closed = False


#define colors
white = (255, 255, 255)
pink = (234, 15, 217)
red = (240, 39, 39)


#define treasures
treasures = [False, False, False, False]

# special and secret unlocked levels
special_level_unlocked_array = [False, False, False]

#local img
bg_img = pygame.image.load('img/Ground/sky1.png')
in_castle_bg_img = pygame.image.load('img/Ground/in_castle_bg.png')
treasure_room_bg_img = pygame.image.load('img/Ground/treasure_room_bg.png')
main_menu_bg_img = pygame.image.load('img/Ground/main_menu_bg.png')
restart_img = pygame.image.load('img/Buttons/restart_button.png')
start_img = pygame.image.load('img/Buttons/play_button.png')
exit_img = pygame.image.load('img/Buttons/exit_button.png')
level_menu_img = pygame.image.load('img/Buttons/level_menu_button.png')
go_back_button_img = pygame.image.load('img/Buttons/go_back_button.png')
go_treasure_room_img = pygame.image.load('img/Buttons/go_treasure_button.png')
go_shop_img = pygame.image.load('img/Buttons/go_shop_button.png')

#level buttons
level_1_Button_img = pygame.image.load('img/Buttons/level_1_Button.png')
level_2_Button_img = pygame.image.load('img/Buttons/level_2_Button.png')
level_3_Button_img = pygame.image.load('img/Buttons/level_3_Button.png')
level_4_Button_img = pygame.image.load('img/Buttons/level_4_Button.png')
level_5_Button_img = pygame.image.load('img/Buttons/level_5_Button.png')
level_6_Button_img = pygame.image.load('img/Buttons/level_6_Button.png')
level_7_Button_img = pygame.image.load('img/Buttons/level_7_Button.png')
level_8_Button_img = pygame.image.load('img/Buttons/level_8_Button.png')
level_9_Button_img = pygame.image.load('img/Buttons/level_9_Button.png')
level_10_Button_img = pygame.image.load('img/Buttons/level_10_Button.png')
level_11_Button_img = pygame.image.load('img/Buttons/level_11_Button.png')
level_12_Button_img = pygame.image.load('img/Buttons/level_12_Button.png')

level_special_One_Button_img = pygame.image.load('img/Buttons/special_level_button_1.png')


level_lock_Button_img = pygame.image.load('img/Buttons/level_locked_Button.png')
level_sicret_lock_Button_img = pygame.image.load('img/Buttons/empty_level_Button_sicret_locked.png')
level_special_lock_Button_img = pygame.image.load('img/Buttons/empty_level_Button_special_locked.png')

#load sounds
pygame.mixer.music.load('sounds/bg_sound_(fairy tail).mp3')
pygame.mixer.music.play(-1, 0.0, 0)
pygame.mixer.music.set_volume(0.5)

coin_fx = pygame.mixer.Sound('sounds/collect_coin.wav')
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('sounds/jumped.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('sounds/game_over.wav')
game_over_fx.set_volume(0.5)
next_level_fx = pygame.mixer.Sound('sounds/next_level.wav')
next_level_fx.set_volume(0.5)
door_opened_fx = pygame.mixer.Sound('sounds/door_opened.wav')
door_opened_fx.set_volume(0.5)
collected_treasure_fx = pygame.mixer.Sound('sounds/collected_treasure.mp3')
collected_treasure_fx.set_volume(0.5)



def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


#table 
def draw_grid():
	for line in range(0, 26):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


def clear_groups():
    player.reset(100 ,screen_height - 130)
    blob_group.empty()
    animated_skeleton_group.empty()
    lava_group.empty()
    coin_group.empty()
    bullet_collector_group.empty()
    platform_group.empty()
    exit_mid_group.empty()
    exit_top_group.empty()
    key_for_cur_level_group.empty()
    key_for_special_level_group.empty()
    treasure_group.empty()
    bullet_group.empty()


def reset_level(level):
    player.reset(100 ,screen_height - 130)
    clear_groups()

    #load world
    if cur_level == 1:
        world = World(levels.level_1)
    elif cur_level == 2:
        world = World(levels.level_2)
    elif cur_level == 3:
        world = World(levels.level_3)
    elif cur_level == 4:
        world = World(levels.level_4)
    elif cur_level == 5:
        world = World(levels.level_5)
    elif cur_level == 6:
        world = World(levels.level_6)
    elif cur_level == 7:
        world = World(levels.level_7)
    elif cur_level == 8:
        world = World(levels.level_8)
    elif cur_level == 9:
        world = World(levels.level_9)
    elif cur_level == 10:
        world = World(levels.level_10)
    else:
        world = World(levels.level_0)

    return world


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouse over and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        #draw button 
        screen.blit(self.image, self.rect)
        
        return action


class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 2
        col_thresh = 20

        if game_over == 0:
            #get pressed
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and not self.in_air:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 4
                self.couter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 4
                self.couter += 1
                self.direction = 1
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.couter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            

            #handle animation
            if self.couter > walk_cooldown:
                self.couter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]




            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10  
            dy += self.vel_y

            #check for  collision with ground
            self.in_air = True
            for tile in world.tile_list:
                #checking in X direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #checking in Y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below the ground
                    if self.vel_y < 0:
                        dy =  tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above the ground
                    elif self.vel_y >= 0:
                        dy =  tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False 


            #check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False) or pygame.sprite.spritecollide(self, animated_skeleton_group, False):
                game_over = -1
                game_over_fx.play()


            #check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                game_over_fx.play()

            #check for collision with exit
            if pygame.sprite.spritecollide(self, exit_mid_group, False) or pygame.sprite.spritecollide(self, exit_top_group, False):
                if is_cur_door_closed != 1:
                    game_over = 1

            #check for collision with platforms
            for platform in platform_group:
                #collisiong with x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #collisiong with y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    #check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    #move sideway with platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_dirction

            


            #update player coordinates
            self.rect.x += dx    
            self.rect.y += dy    

        elif game_over == -1:
            self.image = self.dead_image
            draw_text('YOU DIED!', font, red, (screen_width // 2) - 155, screen_height // 2)
            if self.rect.y > 25:
                self.rect.y -= 5


        #draw player onto screen
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over
    


    def update_cur_bullets(self, game_over, cur_bullet_stats):

        if game_over == 0:
            #get pressed
            key = pygame.key.get_pressed()
            if key[pygame.K_r] and self.shoted == False and cur_bullet_stats > 0:
                bullet = Bullet(self.rect.x, self.rect.y + 40, self.direction)
                bullet_group.add(bullet)
                self.shoted = True    
                cur_bullet_stats -= 1
            if key[pygame.K_r] == False:
                self.shoted = False

        return cur_bullet_stats


    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.couter = 0
        for num in range(1, 11):
            img_right = pygame.image.load(f'img/Player/Walk/p1_walk{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        self.dead_image = pygame.image.load('img/Player/dead/ghost1.png')
        self.shoting_image = pygame.image.load('img/Player/dead/ghost1.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.shoted = False
        self.direction = 1
        self.in_air = True


class World():
      
    def __init__(self, data):
        self.tile_list = []
            
        #load img
        dirt_img = pygame.image.load('img/Tiles/dirt.png')
        grass_img = pygame.image.load('img/Tiles/grassMid.png')
        castle_basic_img = pygame.image.load('img/Tiles/castleCenter.png')
        castle_top_wall_img = pygame.image.load('img/Tiles/castleMid.png')
        castle_cliff_left_img = pygame.image.load('img/Tiles/castleCliffLeft.png')
        castle_cliff_right_img = pygame.image.load('img/Tiles/castleCliffRight.png')
        castle_cliff_left_alt_img = pygame.image.load('img/Tiles/castleCliffLeftAlt.png')
        castle_cliff_right_alt_img = pygame.image.load('img/Tiles/castleCliffRightAlt.png')
        box_img = pygame.image.load('img/Tiles/box.png')
        boxAlt_img = pygame.image.load('img/Tiles/boxAlt.png')


        row_cout = 0
        for row in data:
            col_cout = 0
            for tile in row:
                if tile == 1:  #dirt
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_cout * tile_size
                    img_rect.y = row_cout * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:  #grass
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_cout * tile_size
                    img_rect.y = row_cout * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:  #blob_Enemy
                    blob = Enemy(col_cout * tile_size, row_cout * tile_size + 10)
                    blob_group.add(blob)
                if tile == 4:  #moving_platform ---
                    platform = Platform(col_cout * tile_size, row_cout * tile_size, 1 , 0)
                    platform_group.add(platform)
                if tile == 5:  #moving_platform  |
                    platform = Platform(col_cout * tile_size, row_cout * tile_size, 0 , 1)
                    platform_group.add(platform)
                if tile == 6:  #lava
                    lava = Lava(col_cout * tile_size, row_cout * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 7:  #Coin
                    coin = Coin(col_cout * tile_size + (tile_size // 2), row_cout * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:  #exit_mid_gate
                    if is_cur_door_closed:
                        exit_mid = Exit_Mid(col_cout * tile_size, row_cout * tile_size, 0)
                    else:
                        exit_mid = Exit_Mid(col_cout * tile_size, row_cout * tile_size, 1)
                    exit_mid_group.add(exit_mid)
                if tile == 9: #exit_top_gate
                    if is_cur_door_closed:
                        exit_top = Exit_Top(col_cout * tile_size, row_cout * tile_size, 0)
                    else:
                        exit_top = Exit_Top(col_cout * tile_size, row_cout * tile_size, 1)
                    exit_top_group.add(exit_top)
                if tile == 12:  #moving_platform_castle ---
                    platform = Platform(col_cout * tile_size, row_cout * tile_size, 1 , 0, 1)
                    platform_group.add(platform)
                if tile == 13:  #moving_platform_castle  |
                    platform = Platform(col_cout * tile_size, row_cout * tile_size, 0 , 1, 1)
                    platform_group.add(platform)
                if tile == 14:  #castle_basic
                    img = pygame.transform.scale(castle_basic_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_cout * tile_size
                    img_rect.y = row_cout * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 15:  #castle_top_wall
                    img = pygame.transform.scale(castle_top_wall_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_cout * tile_size
                    img_rect.y = row_cout * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 16:  #castle_cliff_left
                    img = pygame.transform.scale(castle_cliff_left_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_cout * tile_size
                    img_rect.y = row_cout * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 17:  #castle_cliff_right
                    img = pygame.transform.scale(castle_cliff_right_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_cout * tile_size
                    img_rect.y = row_cout * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 18:  #castle_cliff_left_alt
                    img = pygame.transform.scale(castle_cliff_left_alt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_cout * tile_size
                    img_rect.y = row_cout * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 19:  #castle_cliff_right_alt
                    img = pygame.transform.scale(castle_cliff_right_alt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_cout * tile_size
                    img_rect.y = row_cout * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 21:  #Key_For_Cur_Level
                    key = Key_For_Cur_Level(col_cout * tile_size + (tile_size // 2), row_cout * tile_size + (tile_size // 2))
                    key_for_cur_level_group.add(key)
                if tile == 22:  #moving_platform_castle_5 ---
                    platform = Platform(col_cout * tile_size, row_cout * tile_size, 1 , 0, 1, 2)
                    platform_group.add(platform)
                if tile == 23:  #moving_platform_castle_5  |
                    platform = Platform(col_cout * tile_size, row_cout * tile_size, 0 , 1, 1, 2)
                    platform_group.add(platform)
                if tile == 31:  #castle_top_wall_slap
                    img = pygame.transform.scale(castle_top_wall_img, (tile_size, tile_size // 2))
                    img_rect = img.get_rect()
                    img_rect.x = col_cout * tile_size
                    img_rect.y = row_cout * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 32:  #castle_basic_slap
                    img = pygame.transform.scale(castle_basic_img, (tile_size, tile_size // 2))
                    img_rect = img.get_rect()
                    img_rect.x = col_cout * tile_size
                    img_rect.y = row_cout * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 33:  #castle_top_wall_1/4
                    img = pygame.transform.scale(castle_basic_img, (tile_size * 0.6, tile_size // 2))
                    img_rect = img.get_rect()
                    img_rect.x = col_cout * tile_size
                    img_rect.y = row_cout * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 34:  #castle_top_wall_1/4
                    img = pygame.transform.scale(castle_basic_img, (tile_size * 0.4, tile_size ))
                    img_rect = img.get_rect()
                    img_rect.x = col_cout * tile_size
                    img_rect.y = row_cout * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 35:  #box
                    img = pygame.transform.scale(box_img, (tile_size , tile_size ))
                    img_rect = img.get_rect()
                    img_rect.x = col_cout * tile_size
                    img_rect.y = row_cout * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 36:  #boxAlt
                    img = pygame.transform.scale(boxAlt_img, (tile_size, tile_size ))
                    img_rect = img.get_rect()
                    img_rect.x = col_cout * tile_size
                    img_rect.y = row_cout * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 51:  #Treasure_1
                    treasure = Treasure(col_cout * tile_size + (tile_size // 2), row_cout * tile_size + (tile_size // 2), 1)
                    treasure_group.add(treasure)
                if tile == 52:  #Treasure_2
                    treasure = Treasure(col_cout * tile_size + (tile_size // 2), row_cout * tile_size + (tile_size // 2), 2)
                    treasure_group.add(treasure)
                if tile == 53:  #Treasure_3
                    treasure = Treasure(col_cout * tile_size + (tile_size // 2), row_cout * tile_size + (tile_size // 2), 3)
                    treasure_group.add(treasure)
                if tile == 54:  #Treasure_4
                    treasure = Treasure(col_cout * tile_size + (tile_size // 2), row_cout * tile_size + (tile_size // 2), 4)
                    treasure_group.add(treasure)
                if tile == 71:  #Animated_Skeleton_Enemy - 70
                    skeleton = Animated_Skeleton(col_cout * tile_size, row_cout * tile_size - 20, 70)
                    animated_skeleton_group.add(skeleton)
                if tile == 72:  #Animated_Skeleton_Enemy - 40
                    skeleton = Animated_Skeleton(col_cout * tile_size, row_cout * tile_size - 20, 40)
                    animated_skeleton_group.add(skeleton)
                if tile == 81:  #Bullet_Collector
                    bullet_collector = Bullet_Collector(col_cout * tile_size + (tile_size // 2), row_cout * tile_size + (tile_size // 2))
                    bullet_collector_group.add(bullet_collector)
                if tile == 82:  #Key_For_Special_Level_One
                    key_for_special_level_one = Key_For_Special_Level(col_cout * tile_size, row_cout * tile_size + (tile_size // 2), 1)
                    key_for_special_level_group.add(key_for_special_level_one)
                col_cout += 1
            row_cout += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)
         

class Enemy(pygame.sprite.Sprite):
         
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/Enemies/blockerMad.png')
        self.image = pygame.transform.scale(img, (tile_size * 0.8, tile_size * 0.8))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_dirction = 1
        self.move_couter = 0

    def update(self):
        self.rect.x += self.move_dirction
        self.move_couter += 1
        if abs(self.move_couter) > 30:
            self.move_dirction *= -1
            self.move_couter *= -1
            

class Animated_Skeleton(pygame.sprite.Sprite):
    def __init__(self, x, y, distanse):
        self.reset()
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/Enemies/skeleton_1.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_dirction = 1
        self.move_couter = 0
        self.couter = 0
        self.index  = 0
        self.distanse = distanse

    def update(self):
        walk_cooldown = 7
        self.couter += 1
        self.rect.x += self.move_dirction
        self.move_couter += 1
        if abs(self.move_couter) > self.distanse:
            self.move_dirction *= -1
            self.move_couter *= -1


         #handle animation
        if self.couter > walk_cooldown:
            self.couter = 0
            self.index += 1
        if self.index >= len(self.images_right):
            self.index = 0
        if self.move_dirction == -1:
            self.image = self.images_right[self.index]
        if self.move_dirction == 1:
            self.image = self.images_left[self.index]


        #check for collision with bullet
        if pygame.sprite.spritecollide(self, bullet_group, False):
            animated_skeleton_group.remove(self)
        
            


    def reset(self):
        self.images_right = []
        self.images_left = []
        for num in range(1, 4):
            img_right = pygame.image.load(f'img/Enemies/skeleton_{num}.png')
            img_right = pygame.transform.scale(img_right, (50, 70))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y, isInCastle = 0, how_many_blocks_diferrencse = 1):
        pygame.sprite.Sprite.__init__(self)
        if isInCastle == 0:
            img = pygame.image.load('img/Tiles/grass.png')
        else:
            img = pygame.image.load('img/Tiles/castle.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_couter = 0
        self.move_dirction = 1  
        self.move_x = move_x
        self.move_y = move_y
        self.how_many_blocks_diferrencse = how_many_blocks_diferrencse
    
    def update(self):
        self.rect.x += self.move_dirction * self.move_x
        self.rect.y += self.move_dirction * self.move_y
        self.move_couter += 1
        if abs(self.move_couter) > 50 * self.how_many_blocks_diferrencse:
            self.move_dirction *= -1
            self.move_couter *= -1


class Lava(pygame.sprite.Sprite):
         
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/Tiles/liquidLavaTop_mid.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
         
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/treasure/coinOne.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Key_For_Cur_Level(pygame.sprite.Sprite):
         
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/treasure/hud_keyYellow.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Key_For_Special_Level(pygame.sprite.Sprite):

    def __init__(self, x, y, number):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(f'img/treasure/key_for_special_level_{number}.png')
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Treasure(pygame.sprite.Sprite):
         
    def __init__(self, x, y, treasure_index):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(f'img/treasure/treasure_{treasure_index}.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.treasure_index = treasure_index


class Exit_Mid(pygame.sprite.Sprite):

    def __init__(self, x, y, isOpened = 1):
        pygame.sprite.Sprite.__init__(self)
        img_opened = pygame.image.load('img/Tiles/door_openMid.png')
        img_closed = pygame.image.load('img/Tiles/door_closedMid.png')

        self.image_opened = pygame.transform.scale(img_opened, (tile_size, tile_size))
        self.image_closed = pygame.transform.scale(img_closed, (tile_size, tile_size))

        if isOpened:
            self.image = self.image_opened
        else:
            self.image = self.image_closed
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        
        if is_cur_door_closed:
            self.image = self.image_closed 
        else:
            self.image = self.image_opened
        
    
class Exit_Top(pygame.sprite.Sprite):
         
    def __init__(self, x, y, isOpened = 1):
        pygame.sprite.Sprite.__init__(self)
        img_opened = pygame.image.load('img/Tiles/door_openTop.png')
        img_closed = pygame.image.load('img/Tiles/door_closedTop.png')

        self.image_opened = pygame.transform.scale(img_opened, (tile_size, tile_size))
        self.image_closed = pygame.transform.scale(img_closed, (tile_size, tile_size))

        if isOpened:
            self.image = self.image_opened
        else:
            self.image = self.image_closed
        self.rect = self.image.get_rect()
        self.isOpened = isOpened
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        
        if is_cur_door_closed:
            self.image = self.image_closed 
        else:
            self.image = self.image_opened


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/Bullets/fireball_01.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.move_dirction = 15 * direction

    def update(self):
        self.rect.x += self.move_dirction
        if self.rect.x > 1270:
            bullet_group.remove(self)
        if self.rect.x <= 0:
            bullet_group.remove(self)

        #check for  collision with ground
        for tile in world.tile_list:
            #checking in X direction
            if tile[1].colliderect(self.rect.x, self.rect.y, self.width, self.height):
                bullet_group.remove(self)


class Bullet_Collector(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/treasure/bullet_collector.png')
        self.image = pygame.transform.scale(img, (tile_size * 0.7, tile_size * 0.7))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)





player = Player(100 ,screen_height - 130)

blob_group = pygame.sprite.Group()
animated_skeleton_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
bullet_collector_group = pygame.sprite.Group()
exit_mid_group = pygame.sprite.Group()
exit_top_group = pygame.sprite.Group()
key_for_cur_level_group = pygame.sprite.Group()
key_for_special_level_group = pygame.sprite.Group()
treasure_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()


#create dummy coin for showing score
score_coin = Coin(tile_size // 2, tile_size // 2)
score_bullet = Bullet_Collector(tile_size // 2 + 120, tile_size // 2)

#create buttons
restart_button = Button(screen_width // 2 - 420 , screen_height // 2 + 65 , restart_img)
levels_menu_button = Button(screen_width // 2 + 50 , screen_height // 2 + 65 , level_menu_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 50, screen_height // 2, exit_img)
go_back_button = Button(screen_width // 2 - 300, screen_height // 2 + 250, go_back_button_img)
go_treasure_room = Button(screen_width // 2 + 150, screen_height // 2 + 250, go_treasure_room_img)
go_shop_button = Button(screen_width // 2 - 75, screen_height // 2 + 250, go_shop_img)


#level buttons
level_1_Button = Button(screen_width // 2 - 450, screen_height // 2 - 300, level_1_Button_img)
level_2_Button = Button(screen_width // 2 - 300, screen_height // 2 - 300, level_2_Button_img)
level_3_Button = Button(screen_width // 2 - 150, screen_height // 2 - 300, level_3_Button_img)
level_4_Button = Button(screen_width // 2, screen_height // 2 - 300, level_4_Button_img)
level_5_Button = Button(screen_width // 2 + 150, screen_height // 2 - 300, level_5_Button_img)
level_6_Button = Button(screen_width // 2 + 300, screen_height // 2 - 300, level_6_Button_img)
level_7_Button = Button(screen_width // 2 - 450, screen_height // 2 - 150, level_7_Button_img)
level_8_Button = Button(screen_width // 2 - 300, screen_height // 2 - 150, level_8_Button_img)
level_9_Button = Button(screen_width // 2 - 150, screen_height // 2 - 150, level_9_Button_img)
level_10_Button = Button(screen_width // 2, screen_height // 2 - 150, level_10_Button_img)
level_11_Button = Button(screen_width // 2 + 150, screen_height // 2 - 150, level_11_Button_img)
level_12_Button = Button(screen_width // 2 + 300, screen_height // 2 - 150, level_12_Button_img)

level_special_1_Button = Button(screen_width // 2 - 450, screen_height // 2 + 50, level_special_One_Button_img)

#locked levels buttons
level_2_locked_Button = Button(screen_width // 2 - 300, screen_height // 2 - 300, level_lock_Button_img)
level_3_locked_Button = Button(screen_width // 2 - 150, screen_height // 2 - 300, level_lock_Button_img)
level_4_locked_Button = Button(screen_width // 2, screen_height // 2 - 300, level_lock_Button_img)
level_5_locked_Button = Button(screen_width // 2 + 150, screen_height // 2 - 300, level_lock_Button_img)
level_6_locked_Button = Button(screen_width // 2 + 300, screen_height // 2 - 300, level_lock_Button_img)
level_7_locked_Button = Button(screen_width // 2 - 450, screen_height // 2 - 150, level_lock_Button_img)
level_8_locked_Button = Button(screen_width // 2 - 300, screen_height // 2 - 150, level_lock_Button_img)
level_9_locked_Button = Button(screen_width // 2 - 150, screen_height // 2 - 150, level_lock_Button_img)
level_10_locked_Button = Button(screen_width // 2, screen_height // 2 - 150, level_lock_Button_img)
level_11_locked_Button = Button(screen_width // 2 + 150, screen_height // 2 - 150, level_lock_Button_img)
level_12_locked_Button = Button(screen_width // 2 + 300, screen_height // 2 - 150, level_lock_Button_img)

level_special_1_lock_Button = Button(screen_width // 2 - 450, screen_height // 2 + 50, level_special_lock_Button_img)
level_special_2_lock_Button = Button(screen_width // 2 - 300, screen_height // 2 + 50, level_special_lock_Button_img)
level_special_3_lock_Button = Button(screen_width // 2 - 150, screen_height // 2 + 50, level_special_lock_Button_img)

level_sicret_1_lock_Button = Button(screen_width // 2, screen_height // 2 + 50, level_sicret_lock_Button_img)
level_sicret_2_lock_Button = Button(screen_width // 2 + 150, screen_height // 2 + 50, level_sicret_lock_Button_img)
level_sicret_3_lock_Button = Button(screen_width // 2 + 300, screen_height // 2 + 50, level_sicret_lock_Button_img)

world = World(levels.level_1)
run = True  
while run:

    clock.tick(fps)

    if main_menu:
        screen.blit(main_menu_bg_img, (0, 0))
        if start_button.draw():
            main_menu = False
            levels_menu = True
        if exit_button.draw():
            run = False
    elif collection_menu:
        screen.blit(treasure_room_bg_img, (0, 0))
        if go_back_button.draw():
            collection_menu = False
            levels_menu = True
    elif levels_menu:
        screen.blit(bg_img, (0, 0))


        cur_bullet_stats = 0
        if level_1_Button.draw():
            is_cur_door_closed = False
            cur_level = 1
            world = World(levels.level_1)
            levels_menu = False
        if cur_locked_level > 2:
            if level_2_Button.draw():
                is_cur_door_closed = False
                cur_level = 2
                clear_groups()
                world = World(levels.level_2)
                levels_menu = False
        else:
            level_2_locked_Button.draw()
        if cur_locked_level > 3:
            if level_3_Button.draw() :
                is_cur_door_closed = False
                cur_level = 3
                clear_groups()
                world = World(levels.level_3)
                levels_menu = False
        else:
            level_3_locked_Button.draw()
        if cur_locked_level > 4:
            if level_4_Button.draw():
                is_cur_door_closed = False
                cur_level = 4
                clear_groups()
                world = World(levels.level_4)
                levels_menu = False
        else:
            level_4_locked_Button.draw()
        if cur_locked_level > 5:
            if level_5_Button.draw():
                is_cur_door_closed = False
                cur_level = 5
                clear_groups()
                world = World(levels.level_5)
                levels_menu = False
        else:
            level_5_locked_Button.draw()
        if cur_locked_level > 6:
            if level_6_Button.draw():
                is_cur_door_closed = False
                cur_level = 6
                clear_groups()
                world = World(levels.level_6)
                levels_menu = False
        else:
            level_6_locked_Button.draw()
        if cur_locked_level > 7:
            if level_7_Button.draw():
                is_cur_door_closed = False
                cur_level = 7
                clear_groups()
                world = World(levels.level_7)
                levels_menu = False
        else:
            level_7_locked_Button.draw()
        if cur_locked_level > 8:
            if level_8_Button.draw():
                is_cur_door_closed = True   
                cur_level = 8
                clear_groups()
                world = World(levels.level_8)
                levels_menu = False
        else:
            level_8_locked_Button.draw()
        if cur_locked_level > 9:
            if level_9_Button.draw():
                is_cur_door_closed = True
                cur_level = 9
                clear_groups()
                world = World(levels.level_9)
                levels_menu = False
        else:
            level_9_locked_Button.draw()
        if cur_locked_level > 10:
            if level_10_Button.draw():
                is_cur_door_closed = True
                cur_level = 10
                clear_groups()
                world = World(levels.level_10)
                levels_menu = False
        else:
            level_10_locked_Button.draw()
        if cur_locked_level > 11:
            if level_11_Button.draw():
                is_cur_door_closed = True
                cur_level = 11
                clear_groups()
                world = World(levels.level_0)
                levels_menu = False
        else:
            level_11_locked_Button.draw()
        if cur_locked_level > 12:
            if level_12_Button.draw():
                is_cur_door_closed = True
                cur_level = 12
                clear_groups()
                world = World(levels.level_0)
                levels_menu = False
        else:
            level_12_locked_Button.draw()
        
    
        if special_level_unlocked_array[0]:
            if level_special_1_Button.draw():
                pass
        elif level_special_1_lock_Button.draw():
            pass


        if level_special_2_lock_Button.draw():
            pass
        if level_special_3_lock_Button.draw():
            pass
        if level_sicret_1_lock_Button.draw():
            pass
        if level_sicret_2_lock_Button.draw():
            pass
        if level_sicret_3_lock_Button.draw():
            pass

        if go_back_button.draw():
            main_menu = True
            levels_menu = False
            clear_groups()    
        if go_treasure_room.draw():
            collection_menu = True
            levels_menu = False
            clear_groups() 
        if go_shop_button.draw():
            pass
    
    #while playing
    else:
        if cur_level < 8:
            screen.blit(bg_img, (0, 0))          
        elif cur_level >= 7 and cur_level <= 12:
            screen.blit(in_castle_bg_img, (0, 0))

        coin_group.add(score_coin)
        bullet_collector_group.add(score_bullet)
        world.draw()

        if game_over == 0:
            blob_group.update()
            animated_skeleton_group.update()
            platform_group.update()
            bullet_group.update()


            draw_text('x ' + str(saved_score + cur_level_score), font_score, white, tile_size - 10, 17)
            draw_text('x ' + str(cur_bullet_stats), font_score, white, tile_size + 112, 17)


            #check if coin collected
            if pygame.sprite.spritecollide(player, coin_group, True):
                cur_level_score += 1
                coin_fx.play()
            
            #check if key_cur_level collected
            if pygame.sprite.spritecollide(player, key_for_cur_level_group, True):
                is_cur_door_closed = False
                exit_mid_group.update()
                exit_top_group.update()
                door_opened_fx.play()

            #check if treasure collected
            if pygame.sprite.spritecollide(player, treasure_group, True):
                if cur_level == 3:
                    treasures[0] = True
                    collected_treasure_fx.play()
                elif cur_level == 8:
                    treasures[1] = True
                    collected_treasure_fx.play()

            #check if bullet collected
            if pygame.sprite.spritecollide(player, bullet_collector_group, True):
                cur_bullet_stats += 3

            #check if key_for_special_level collected
            if pygame.sprite.spritecollide(player, key_for_special_level_group, True):
                if cur_level == 9:
                    special_level_unlocked_array[0] = True


        blob_group.draw(screen)
        animated_skeleton_group.draw(screen)
        lava_group.draw(screen)
        platform_group.draw(screen)
        coin_group.draw(screen)
        bullet_collector_group.draw(screen)
        key_for_cur_level_group.draw(screen)
        key_for_special_level_group.draw(screen)
        treasure_group.draw(screen)
        exit_mid_group.draw(screen)
        exit_top_group.draw(screen)
        bullet_group.draw(screen)


        game_over = player.update(game_over)
        cur_bullet_stats = player.update_cur_bullets(game_over, cur_bullet_stats)
                
        #if player die
        if game_over == -1:
            
            if cur_level > 7 and cur_level <= 12:
                is_cur_door_closed = True
            if restart_button.draw():
                cur_dead_stats += 1
                #print('current level: {} dead number: {}'.format(cur_level, cur_dead_stats))
                world = reset_level(cur_level)
                game_over = 0
                cur_level_score = 0
                cur_bullet_stats = 0
            if levels_menu_button.draw():
                cur_dead_stats += 1
                #print('current level: {} dead number: {}'.format(cur_level, cur_dead_stats))
                clear_groups()
                levels_menu = True
                game_over = 0
                cur_level_score = 0
                cur_bullet_stats = 0
        


        #if player complete level
        if game_over == 1:
            #reset game and go next level
            cur_level += 1
            cur_bullet_stats = 0

            # if next level in castle lock it
            if cur_level > 7 and cur_level <= 12:
                is_cur_door_closed = True
            else:
                is_cur_door_closed = False
            

            if cur_level == cur_locked_level:
                cur_locked_level += 1

            if cur_level <= max_levels:
                #reset levels
                next_level_fx.play()
                saved_score += cur_level_score
                cur_level_score = 0
                world = reset_level(cur_level)
                game_over = 0
            else:
                draw_text('YOU WIN!', font, pink, (screen_width // 2) - 140, screen_height // 2)
                if restart_button.draw():
                    cur_level = 1
                    #restart game
                    world = reset_level(cur_level)
                    game_over = 0
                    #score = 0
                if levels_menu_button.draw():
                    clear_groups()
                    levels_menu = True
                    game_over = 0
                    cur_level_score = 0


        #draw_grid()

        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()