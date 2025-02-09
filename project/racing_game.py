import pygame
import sys
import subprocess
import random

# Инициализация Pygame
pygame.init()

# Музыкальное сопровождение
def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load("AUDIO-2025-02-09-19-19-04.mp3")  # Укажите свой файл музыки для гонки
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

# Остановка музыки
def stop_music():
    pygame.mixer.music.stop()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ROAD_COLOR = (50, 50, 50)
ROAD_LINE_COLOR = (255, 255, 255)

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Гоночная игра")
clock = pygame.time.Clock()

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 100), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, BLUE, [(25, 0), (50, 100), (0, 100)])
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120)
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

# Класс препятствий
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 100), pygame.SRCALPHA)
        pygame.draw.rect(self.image, RED, self.image.get_rect(), border_radius=15)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.speed = random.randint(3, 7)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Экран окончания игры
def game_over_screen(score):
    stop_music()  # Остановить музыку гонки перед выходом

    font = pygame.font.Font(None, 72)
    draw_text("GAME OVER", font, RED, screen, SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50)
    draw_text(f"Score: {score}", font, WHITE, screen, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2)
    pygame.display.flip()

    button_font = pygame.font.Font(None, 36)
    restart_button = pygame.Rect(100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    menu_button = pygame.Rect(500, SCREEN_HEIGHT // 2 + 50, 200, 50)

    pygame.draw.rect(screen, GRAY, restart_button)
    pygame.draw.rect(screen, GRAY, menu_button)

    draw_text("RESTART", button_font, BLACK, screen, restart_button.x + 50, restart_button.y + 10)
    draw_text("MAIN MENU", button_font, BLACK, screen, menu_button.x + 30, menu_button.y + 10)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    main()  # Перезапуск игры
                elif menu_button.collidepoint(event.pos):
                    stop_music()  # Остановить музыку перед выходом в меню
                    subprocess.run([sys.executable, "main_menu.py"])
                    return

        clock.tick(FPS)

# Основная функция игры
def main():
    play_music()  # Запустить музыку гонки

    player = Player()
    obstacles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    all_sprites.add(player)

    for _ in range(5):
        obstacle = Obstacle()
        obstacles.add(obstacle)
        all_sprites.add(obstacle)

    score = 0
    font = pygame.font.Font(None, 36)
    running = True

    while running:
        screen.fill(ROAD_COLOR)

        for i in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.rect(screen, ROAD_LINE_COLOR, (SCREEN_WIDTH // 2 - 5, i, 10, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_music()
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.update(keys)
        obstacles.update()

        if pygame.sprite.spritecollideany(player, obstacles):
            running = False
            game_over_screen(score)

        score += 1
        all_sprites.draw(screen)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
