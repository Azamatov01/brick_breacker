import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [RED, GREEN, BLUE]

# Шрифты
font = pygame.font.SysFont("Arial", 30)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Состояния игры
STATE_MENU = "menu"
STATE_SETTINGS = "settings"
STATE_GAME = "game"
STATE_AI_GAME = "ai_game"
STATE_GAME_SELECTION = "game_selection"
game_state = STATE_MENU  # Установка начального состояния в главное меню

# Функции рисования
def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_button(text, x, y, width, height, color, text_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, width, height)

    pygame.draw.rect(screen, color, button_rect)
    draw_text(text, x + 20, y + 10, text_color)

    if button_rect.collidepoint(mouse) and click[0] == 1 and action is not None:
        pygame.time.delay(150)  # Задержка для избежания двойного клика
        action()

# Функция изменения состояния
def change_state(new_state):
    global game_state
    print(f"Changing state to: {new_state}")  # Логируем изменение состояния
    game_state = new_state

# Главное меню
def main_menu():
    screen.fill(BLACK)
    draw_text("Main Menu", WIDTH // 2 - 100, 100, WHITE)
    draw_button("Start Game", WIDTH // 2 - 100, 200, 200, 50, GRAY, WHITE, start_game_selection)
    draw_button("Settings", WIDTH // 2 - 100, 300, 200, 50, GRAY, WHITE, lambda: change_state(STATE_SETTINGS))
    draw_button("Exit", WIDTH // 2 - 100, 400, 200, 50, GRAY, WHITE, quit_game)

# Меню выбора игры
def start_game_selection():
    change_state(STATE_GAME_SELECTION)  # Переход в меню выбора игры
    screen.fill(BLACK)
    draw_text("Game Selection", WIDTH // 2 - 100, 100, WHITE)
    draw_button("Play Game", WIDTH // 2 - 100, 200, 200, 50, GRAY, WHITE, lambda: change_state(STATE_GAME))
    draw_button("Play Game with AI", WIDTH // 2 - 100, 300, 200, 50, GRAY, WHITE, lambda: change_state(STATE_AI_GAME))
    draw_button("Back to Menu", WIDTH // 2 - 100, 400, 200, 50, GRAY, WHITE, lambda: change_state(STATE_MENU))

# Настройки
def settings():
    screen.fill(BLACK)
    draw_text("Settings Menu", WIDTH // 2 - 100, 100, WHITE)
    draw_button("Back to Menu", WIDTH // 2 - 100, 400, 200, 50, GRAY, WHITE, return_to_menu)

# Функция возврата в главное меню
def return_to_menu():
    print("Returning to main menu...")
    global game_state
    game_state = STATE_MENU

# Завершение игры
def quit_game():
    print("Quitting game...")
    pygame.quit()
    exit()

# Заглушка для игры
def game():
    screen.fill(BLACK)
    draw_text("Game is running!", WIDTH // 2 - 100, HEIGHT // 2 - 20, WHITE)
    draw_button("Back to Menu", WIDTH // 2 - 100, 400, 200, 50, GRAY, WHITE, lambda: change_state(STATE_MENU))

# Заглушка для игры с ИИ
def ai_game():
    screen.fill(BLACK)
    draw_text("AI Game is running!", WIDTH // 2 - 100, HEIGHT // 2 - 20, WHITE)
    draw_button("Back to Menu", WIDTH // 2 - 100, 400, 200, 50, GRAY, WHITE, lambda: change_state(STATE_MENU))

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == STATE_MENU:
        main_menu()
    elif game_state == STATE_SETTINGS:
        settings()
    elif game_state == STATE_GAME:
        game()
    elif game_state == STATE_AI_GAME:
        ai_game()
    elif game_state == STATE_GAME_SELECTION:
        start_game_selection()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
