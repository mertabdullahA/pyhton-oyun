import pygame
import random

# Pygame'i başlat
pygame.init()

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Ekran boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Ekran
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Üç Oyunlu Menü")

# Saat ayarı (FPS)
clock = pygame.time.Clock()

# Yazı fontu
font = pygame.font.SysFont("monospace", 50)

# Yılan oyunu
def snake_game():
    snake_speed = 10  # Orta hız
    snake_pos = [[100, 50]]
    direction = 'RIGHT'
    change_to = direction
    food_pos = [random.randrange(1, SCREEN_WIDTH // 10) * 10, random.randrange(1, SCREEN_HEIGHT // 10) * 10]
    food_spawn = True

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_RIGHT and direction != 'DOWN':
                    change_to = 'UP'

        direction = change_to

        # Yılanın hareketi
        if direction == 'UP':
            snake_pos[0][1] -= 10
        if direction == 'DOWN':
            snake_pos[0][1] += 10
        if direction == 'DOWN':
            snake_pos[0][0] -= 10
        if direction == 'UP':
            snake_pos[0][0] += 10

        # Yılanın sınır kontrolü (duvara çarparsa veya kendisine çarparsa oyun biter)
        if (snake_pos[0][0] < 0 or snake_pos[0][0] >= SCREEN_WIDTH or 
            snake_pos[0][1] < 0 or snake_pos[0][1] >= SCREEN_HEIGHT or 
            snake_pos[0] in snake_pos[1:]):
            running = False  # Oyun biter

        # Yılanın büyümesi
        snake_pos.insert(0, list(snake_pos[0]))
        if snake_pos[0] == food_pos:
            food_spawn = False
        else:
            snake_pos.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, SCREEN_WIDTH // 10) * 10, random.randrange(1, SCREEN_HEIGHT // 10) * 10]
        food_spawn = True

        screen.fill(BLACK)
        for block in snake_pos:
            pygame.draw.rect(screen, BLUE, pygame.Rect(block[0], block[1], 10, 10))

        pygame.draw.rect(screen, GREEN, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        pygame.display.update()
        clock.tick(snake_speed)

# Top yakalama oyunu
def ball_bounce_game():
    paddle_width = 100
    paddle_height = 20
    paddle_x = (SCREEN_WIDTH - paddle_width) // 2
    paddle_speed = 10

    ball_radius = 15
    ball_x = random.randint(ball_radius, SCREEN_WIDTH - ball_radius)
    ball_y = ball_radius
    ball_speed_x = 5
    ball_speed_y = 5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - paddle_width:
            paddle_x += paddle_speed

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        if ball_x - ball_radius < 0 or ball_x + ball_radius > SCREEN_WIDTH:
            ball_speed_x *= -1
        if ball_y - ball_radius < 0:
            ball_speed_y *= -1

        if ball_y + ball_radius > SCREEN_HEIGHT:
            running = False  # Oyunun sonlanması

        if paddle_x < ball_x < paddle_x + paddle_width and ball_y + ball_radius >= SCREEN_HEIGHT - paddle_height:
            ball_speed_y *= -1

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, (paddle_x, SCREEN_HEIGHT - paddle_height, paddle_width, paddle_height))
        pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

        pygame.display.update()
        clock.tick(60)

# FPS tarzı karakter oyunu
def shooter_game():
    player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    player_speed = 5
    bullets = []
    enemies = []
    score = 0
    lives = 3
    enemy_spawn_rate = 30  # Yaratıkların ekranda çıkma oranı

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Sol tıkla ateş etme
                    bullets.append(list(player_pos))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos[1] -= player_speed
        if keys[pygame.K_s]:
            player_pos[1] += player_speed
        if keys[pygame.K_a]:
            player_pos[0] -= player_speed
        if keys[pygame.K_d]:
            player_pos[0] += player_speed

        # Yaratıkların spawn olması
        if random.randint(1, enemy_spawn_rate) == 1:
            enemies.append([random.randint(0, SCREEN_WIDTH - 50), 0])  # Rastgele konumda yaratık ekle

        # Kurşunların hareketi
        for bullet in bullets:
            bullet[1] -= 10  # Kurşun yukarı hareket eder
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Yaratıkların hareketi
        for enemy in enemies:
            enemy[1] += 5  # Yaratıklar aşağıya doğru hareket eder
            if enemy[1] > SCREEN_HEIGHT:
                lives -= 1  # Can kaybı
                enemies.remove(enemy)

            # Çarpışma kontrolü: Karakter yaratığa çarparsa oyun biter
            if pygame.Rect(player_pos[0], player_pos[1], 50, 50).colliderect(pygame.Rect(enemy[0], enemy[1], 50, 50)):
                lives -= 1
                enemies.remove(enemy)  # Karakterle yaratık çarpışması
                if lives <= 0:
                    running = False  # Oyun biter

        # Kurşun ve yaratık çarpışması
        for bullet in bullets:
            for enemy in enemies:
                if pygame.Rect(bullet[0], bullet[1], 5, 5).colliderect(pygame.Rect(enemy[0], enemy[1], 50, 50)):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break  # İlk bulduğunda çık, çünkü bir kurşun bir yaratığı vurabilir

        screen.fill(BLACK)
        pygame.draw.circle(screen, BLUE, player_pos, 25)  # Karakter

        for bullet in bullets:
            pygame.draw.circle(screen, WHITE, bullet, 5)  # Kurşunlar

        for enemy in enemies:
            pygame.draw.rect(screen, RED, pygame.Rect(enemy[0], enemy[1], 50, 50))  # Yaratıklar

        pygame.display.update()
        clock.tick(60)

# Başlangıç menüsü
def start_menu():
    running = True
    while running:
        screen.fill(BLACK)

        draw_text("1: Yılan Oyunu", 50, WHITE, 150, 100)
        draw_text("2: Top Yakalama Oyunu", 50, WHITE, 150, 200)
        draw_text("3: FPS Tarzı Oyun", 50, WHITE, 150, 300)
        draw_text("Q: Çık", 50, WHITE, 150, 400)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    snake_game()
                elif event.key == pygame.K_2:
                    ball_bounce_game()
                elif event.key == pygame.K_3:
                    shooter_game()
                elif event.key == pygame.K_q:
                    running = False

# Yazı çizme fonksiyonu
def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont("monospace", size)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Oyun döngüsü
start_menu()
pygame.quit()
