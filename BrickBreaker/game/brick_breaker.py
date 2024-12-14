import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Цвета
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, GREEN, BLUE]

# FPS и таймеры
clock = pygame.time.Clock()
FPS = 60
color_change_timer = 0
COLOR_CHANGE_INTERVAL = 10000  # 10 секунд

# Параметры платформы
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2
paddle_y = HEIGHT - 30
paddle_speed = 10

# Параметры мяча
BALL_RADIUS = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx, ball_dy = 4, -4
ball_color = random.choice(COLORS)

# Параметры блоков
BLOCK_WIDTH, BLOCK_HEIGHT = 75, 30
BLOCK_PADDING = 5
blocks = []
for row in range(5):
    for col in range(10):
        x = col * (BLOCK_WIDTH + BLOCK_PADDING) + 10
        y = row * (BLOCK_HEIGHT + BLOCK_PADDING) + 10
        color = random.choice(COLORS)
        block = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)
        blocks.append((block, color))

# Основной игровой цикл
running = True
while running:
    screen.fill(BLACK)
    current_time = pygame.time.get_ticks()

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление платформой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
        paddle_x += paddle_speed

    # Движение мяча
    ball_x += ball_dx
    ball_y += ball_dy

    # Столкновения с границами
    if ball_x - BALL_RADIUS <= 0 or ball_x + BALL_RADIUS >= WIDTH:
        ball_dx = -ball_dx
    if ball_y - BALL_RADIUS <= 0:
        ball_dy = -ball_dy
    if ball_y + BALL_RADIUS >= HEIGHT:
        print("Game Over!")
        running = False

    # Столкновение с платформой
    paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    if paddle_rect.collidepoint(ball_x, ball_y + BALL_RADIUS):
        ball_dy = -abs(ball_dy)

    # Столкновения с блоками
    ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
    for block, color in blocks[:]:
        if block.colliderect(ball_rect):
            if ball_color == color:  # Уничтожение блока при совпадении цвета
                blocks.remove((block, color))
            else:
                # Определение стороны столкновения
                overlap_left = ball_rect.right - block.left
                overlap_right = block.right - ball_rect.left
                overlap_top = ball_rect.bottom - block.top
                overlap_bottom = block.bottom - ball_rect.top

                # Выбираем наименьшее пересечение для определения стороны
                if min(overlap_left, overlap_right) < min(overlap_top, overlap_bottom):
                    # Горизонтальное столкновение
                    if overlap_left < overlap_right:
                        ball_dx = -abs(ball_dx)
                        ball_x = block.left - BALL_RADIUS
                    else:
                        ball_dx = abs(ball_dx)
                        ball_x = block.right + BALL_RADIUS
                else:
                    # Вертикальное столкновение
                    if overlap_top < overlap_bottom:
                        ball_dy = -abs(ball_dy)
                        ball_y = block.top - BALL_RADIUS
                    else:
                        ball_dy = abs(ball_dy)
                        ball_y = block.bottom + BALL_RADIUS
            break  # Прекращаем проверку после столкновения

    # Смена цвета мяча каждые 10 секунд
    if current_time - color_change_timer >= COLOR_CHANGE_INTERVAL:
        ball_color = random.choice(COLORS)
        color_change_timer = current_time

    # Рисование платформы, мяча и блоков
    pygame.draw.rect(screen, WHITE, paddle_rect)
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), BALL_RADIUS)
    for block, color in blocks:
        pygame.draw.rect(screen, color, block)

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
