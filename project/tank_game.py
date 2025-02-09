import sys

import pygame
import math
import random
import subprocess

# Инициализация Pygame
pygame.init()

# Загрузка музыки
pygame.mixer.init()
pygame.mixer.music.load("AUDIO-2025-02-09-19-19-04.mp3")  # Название вашего файла
pygame.mixer.music.set_volume(0.5)  # Настройте громкость
pygame.mixer.music.play(-1)  # Бесконечное воспроизведение


# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

TANK_WIDTH = 40
TANK_HEIGHT = 20
TANK_SPEED = 3
BULLET_SPEED = 6

ENEMY_SPEED = 2
ENEMY_BULLET_SPEED = 4
ENEMY_SHOOT_INTERVAL = 2000  # 2 секунды
ENEMY_SPAWN_TIME = 3000  # 3 секунды
MAX_ENEMIES = 4
PLAYER_LIVES = 3

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank Battle")

# Игрок
tank_x = SCREEN_WIDTH // 2
tank_y = SCREEN_HEIGHT // 2
tank_angle = 0
player_lives = PLAYER_LIVES
player_score = 0
player_alive = True

bullets = []
enemy_bullets = []
enemies = []
last_shot_time = 0
last_enemy_spawn = 0

# Стены (x, y, width, height)
walls = [(200, 200, 100, 50), (500, 300, 100, 50), (300, 400, 150, 50)]


def spawn_enemy():
    if len(enemies) < MAX_ENEMIES:
        while True:
            enemy_x = random.randint(50, SCREEN_WIDTH - 50)
            enemy_y = random.randint(50, SCREEN_HEIGHT - 50)
            if not any(pygame.Rect(wall).collidepoint(enemy_x, enemy_y) for wall in walls):
                enemies.append([enemy_x, enemy_y, 0, pygame.time.get_ticks()])
                break


def move_tank(x, y, speed, angle):
    new_x = x + speed * math.cos(math.radians(angle))
    new_y = y - speed * math.sin(math.radians(angle))

    # Проверка на стены
    future_rect = pygame.Rect(new_x - TANK_WIDTH // 2, new_y - TANK_HEIGHT // 2, TANK_WIDTH, TANK_HEIGHT)
    if any(pygame.Rect(wall).colliderect(future_rect) for wall in walls):
        return x, y  # Остановка перед стеной

    # Проверка на столкновение с врагами
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0] - TANK_WIDTH // 2, enemy[1] - TANK_HEIGHT // 2, TANK_WIDTH, TANK_HEIGHT)
        if future_rect.colliderect(enemy_rect):
            return x, y  # Остановка перед врагом

    return new_x, new_y


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def return_to_menu():
    pygame.mixer.music.stop()
    pygame.quit()
    subprocess.run([sys.executable, "main_menu.py"])

def reset_game():
    global tank_x, tank_y, tank_angle, player_lives, player_score, player_alive, bullets, enemy_bullets, enemies, last_shot_time, last_enemy_spawn
    tank_x = SCREEN_WIDTH // 2
    tank_y = SCREEN_HEIGHT // 2
    tank_angle = 0
    player_lives = PLAYER_LIVES
    player_score = 0
    player_alive = True
    bullets = []
    enemy_bullets = []
    enemies = []
    last_shot_time = 0
    last_enemy_spawn = 0


running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and not player_alive:
            reset_game()

    if not running:
        break

    screen.fill(WHITE)

    keys = pygame.key.get_pressed()
    if player_alive:
        if keys[pygame.K_LEFT]:
            tank_angle += 5
        if keys[pygame.K_RIGHT]:
            tank_angle -= 5
        if keys[pygame.K_UP]:
            tank_x, tank_y = move_tank(tank_x, tank_y, TANK_SPEED, tank_angle)
        if keys[pygame.K_DOWN]:
            tank_x, tank_y = move_tank(tank_x, tank_y, -TANK_SPEED, tank_angle)
        if keys[pygame.K_SPACE] and current_time - last_shot_time >= 500:
            bullet_x = tank_x + TANK_WIDTH // 2 * math.cos(math.radians(tank_angle))
            bullet_y = tank_y - TANK_HEIGHT // 2 * math.sin(math.radians(tank_angle))
            bullets.append([bullet_x, bullet_y, tank_angle])
            last_shot_time = current_time

    for wall in walls:
        pygame.draw.rect(screen, GRAY, wall)

    if player_alive:
        pygame.draw.rect(screen, GREEN, (tank_x - TANK_WIDTH // 2, tank_y - TANK_HEIGHT // 2, TANK_WIDTH, TANK_HEIGHT))
        pygame.draw.line(screen, BLACK, (tank_x, tank_y),
                         (tank_x + TANK_WIDTH // 2 * math.cos(math.radians(tank_angle)),
                          tank_y - TANK_HEIGHT // 2 * math.sin(math.radians(tank_angle))), 3)

    for bullet in bullets[:]:
        bullet[0] += BULLET_SPEED * math.cos(math.radians(bullet[2]))
        bullet[1] -= BULLET_SPEED * math.sin(math.radians(bullet[2]))
        pygame.draw.circle(screen, BLACK, (int(bullet[0]), int(bullet[1])), 5)
        if bullet[0] < 0 or bullet[0] > SCREEN_WIDTH or bullet[1] < 0 or bullet[1] > SCREEN_HEIGHT:
            bullets.remove(bullet)
            continue
        bullet_rect = pygame.Rect(bullet[0] - 2, bullet[1] - 2, 4, 4)
        if any(pygame.Rect(wall).colliderect(bullet_rect) for wall in walls):
            bullets.remove(bullet)

    for enemy in enemies[:]:
        enemy_x, enemy_y, enemy_angle, last_shot = enemy

        dx = tank_x - enemy_x
        dy = tank_y - enemy_y
        enemy_angle = math.degrees(math.atan2(-dy, dx))

        enemy_x, enemy_y = move_tank(enemy_x, enemy_y, ENEMY_SPEED, enemy_angle)

        if current_time - last_shot >= ENEMY_SHOOT_INTERVAL:
            bullet_x = enemy_x + TANK_WIDTH // 2 * math.cos(math.radians(enemy_angle))
            bullet_y = enemy_y - TANK_HEIGHT // 2 * math.sin(math.radians(enemy_angle))
            enemy_bullets.append([bullet_x, bullet_y, enemy_angle])
            last_shot = current_time

        enemy[:] = [enemy_x, enemy_y, enemy_angle, last_shot]

        pygame.draw.rect(screen, RED, (enemy_x - TANK_WIDTH // 2, enemy_y - TANK_HEIGHT // 2, TANK_WIDTH, TANK_HEIGHT))
        pygame.draw.line(screen, BLACK, (enemy_x, enemy_y),
                         (enemy_x + TANK_WIDTH // 2 * math.cos(math.radians(enemy_angle)),
                          enemy_y - TANK_HEIGHT // 2 * math.sin(math.radians(enemy_angle))), 3)

        for bullet in bullets[:]:
            if pygame.Rect(enemy_x - TANK_WIDTH // 2, enemy_y - TANK_HEIGHT // 2, TANK_WIDTH, TANK_HEIGHT).collidepoint(
                    bullet[0], bullet[1]):
                enemies.remove(enemy)
                bullets.remove(bullet)
                player_score += 1
                break

    for enemy_bullet in enemy_bullets[:]:
        enemy_bullet[0] += ENEMY_BULLET_SPEED * math.cos(math.radians(enemy_bullet[2]))
        enemy_bullet[1] -= ENEMY_BULLET_SPEED * math.sin(math.radians(enemy_bullet[2]))
        pygame.draw.circle(screen, RED, (int(enemy_bullet[0]), int(enemy_bullet[1])), 5)
        if enemy_bullet[0] < 0 or enemy_bullet[0] > SCREEN_WIDTH or enemy_bullet[1] < 0 or enemy_bullet[1] > SCREEN_HEIGHT:
            enemy_bullets.remove(enemy_bullet)
        if pygame.Rect(tank_x - TANK_WIDTH // 2, tank_y - TANK_HEIGHT // 2, TANK_WIDTH, TANK_HEIGHT).collidepoint(
                enemy_bullet[0], enemy_bullet[1]):
            player_lives -= 1
            enemy_bullets.remove(enemy_bullet)
            if player_lives == 0:
                player_alive = False

    if current_time - last_enemy_spawn >= ENEMY_SPAWN_TIME:
        spawn_enemy()
        last_enemy_spawn = current_time

    font = pygame.font.Font(None, 36)
    draw_text(f"Lives: {player_lives}", font, BLACK, screen, 10, 10)
    draw_text(f"Score: {player_score}", font, BLACK, screen, 10, 50)

    if not player_alive:
        draw_text("GAME OVER", font, RED, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
        draw_text("Press R to Restart", font, RED, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 40)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
