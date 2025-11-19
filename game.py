import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen Dimensions
WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Load Assets
def load_image(name, scale=None):
    try:
        img = pygame.image.load(name).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    except FileNotFoundError:
        print(f"Warning: {name} not found. Using placeholder.")
        return None

# Backgrounds
bg_img_1 = load_image("newSpaceBackGround.jpg", (WIDTH, HEIGHT))
bg_img_2 = load_image("space_background.png", (WIDTH, HEIGHT))
current_bg = bg_img_1

# Player Sprites
player_img_1 = load_image("sprite.png", (50, 50))
player_img_2 = load_image("newSprite.png", (50, 50))
player_img_3 = load_image("sprite3.png", (50, 50))

# Bullet Sprites
bullet_img_fire = load_image("fire.png", (15, 30))
bullet_img_blue = load_image("blue_fire.png", (15, 30))

# Sound
shoot_sound = None
try:
    shoot_sound = pygame.mixer.Sound("shoot.mp3")
except FileNotFoundError:
    print("Warning: shoot.mp3 not found.")

def play_shoot_sound():
    if shoot_sound:
        shoot_sound.play()

def play_bg_music():
    pygame.mixer.music.load("interstellar.mp3")
    pygame.mixer.music.play(-1)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img_1 if player_img_1 else pygame.Surface((50, 40))
        if not player_img_1: self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.kills = 0
        self.power_level = 1
        self.last_power_up_time = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -8
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 8
        
        self.rect.x += self.speed_x
        
        # Boundaries
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        # Power Level & Visual Progression Logic
        old_level = self.power_level
        
        # Update Player Sprite based on kills
        if self.kills >= 100:
            if player_img_3: self.image = player_img_3
        elif self.kills >= 50:
            if player_img_2: self.image = player_img_2
        else:
            if player_img_1: self.image = player_img_1

        # Power Level
        if self.kills >= 20:
            self.power_level = 3
        elif self.kills >= 10:
            self.power_level = 2
        else:
            self.power_level = 1
        
        if self.power_level > old_level:
            self.last_power_up_time = pygame.time.get_ticks()

    def shoot(self):
        # Determine Bullet Image
        b_img = bullet_img_fire
        if 50 <= self.kills < 100:
            b_img = bullet_img_blue
        
        if self.power_level == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top, b_img)
            all_sprites.add(bullet)
            bullets.add(bullet)
        elif self.power_level == 2:
            bullet1 = Bullet(self.rect.left, self.rect.centery, b_img)
            bullet2 = Bullet(self.rect.right, self.rect.centery, b_img)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bullets.add(bullet1)
            bullets.add(bullet2)
        elif self.power_level == 3:
            bullet1 = Bullet(self.rect.centerx, self.rect.top, b_img, 0)
            bullet2 = Bullet(self.rect.centerx, self.rect.top, b_img, -3)
            bullet3 = Bullet(self.rect.centerx, self.rect.top, b_img, 3)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            all_sprites.add(bullet3)
            bullets.add(bullet1)
            bullets.add(bullet2)
            bullets.add(bullet3)
            
        play_shoot_sound()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN) # Green for Enemies
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(2, 8)
        self.speed_x = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        
        # Respawn if off screen
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(2, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, img, speed_x=0):
        super().__init__()
        if img:
            self.image = img
        else:
            self.image = pygame.Surface((10, 20))
            self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_y = -10
        self.speed_x = speed_x

    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.bottom < 0:
            self.kill()

# Game Loop Variables
bg_y = 0
score = 0
font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x, y, color=WHITE):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_go_screen():
    SCREEN.fill(BLACK)
    draw_text(SCREEN, "SPACE SHOOTER", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(SCREEN, "Arrow keys to move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(SCREEN, "Press R to start", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False

# Groups
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
    m = Enemy()
    all_sprites.add(m)
    mobs.add(m)

# Start Music
play_bg_music()

game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            m = Enemy()
            all_sprites.add(m)
            mobs.add(m)
        score = 0

    # Keep loop running at the right speed
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update
    all_sprites.update()

    # Check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 10
        player.kills += 1
        m = Enemy()
        all_sprites.add(m)
        mobs.add(m)

    # Check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        game_over = True

    # Draw / Render
    # Scrolling Background
    # Determine Background based on kills
    if player.kills >= 50:
        current_bg = bg_img_2
    else:
        current_bg = bg_img_1

    if current_bg:
        rel_y = bg_y % current_bg.get_rect().height
        SCREEN.blit(current_bg, (0, rel_y - current_bg.get_rect().height))
        if rel_y < HEIGHT:
            SCREEN.blit(current_bg, (0, rel_y))
        bg_y += 2
    else:
        SCREEN.fill(BLACK)

    all_sprites.draw(SCREEN)
    draw_text(SCREEN, str(score), 18, WIDTH / 2, 10)
    draw_text(SCREEN, f"Kills: {player.kills}", 18, WIDTH - 50, 10)

    # Power Up Text
    if pygame.time.get_ticks() - player.last_power_up_time < 2000:
        draw_text(SCREEN, "POWER UP!", 40, WIDTH / 2, HEIGHT / 2, YELLOW)

    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
