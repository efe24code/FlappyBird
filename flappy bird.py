import pygame
import random

# PyGame'i başlat
pygame.init()

# Oyun penceresinin boyutları
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Kuş özellikleri
bird_img = pygame.image.load("bird.png").convert_alpha()  # Kullanmak istediğiniz görseli yükleyin
bird_img = pygame.transform.scale(bird_img, (40, 40))  # Görseli 40x40 boyutuna ayarlayın
bird_rect = bird_img.get_rect(center=(100, HEIGHT // 2))

# Engeller sınıfı
class Pipe:
    def __init__(self, x, height):
        self.x = x
        self.height = height
        self.scored = False

    def move(self, speed):
        self.x -= speed

    def is_visible(self):
        return self.x > -pipe_width

# Engeller için başlangıç
pipe_width = 60
pipe_gap = 150
pipe_speed = 5
pipes = []

# Hız ve yerçekimi
bird_velocity = 0
gravity = 0.4  # Yerçekimi değeri
jump_strength = -8  # Zıplama kuvveti

# Skor
score = 0
font = pygame.font.SysFont(None, 36)

# Oyun döngüsü
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength  # Zıplama kuvveti uygula

    # Kuşun hareketi
    bird_velocity += gravity
    bird_rect.y += bird_velocity

    # Engelleri hareket ettir ve yeni engeller ekle
    if not pipes or pipes[-1].x < WIDTH - 200:
        pipe_height = random.randint(100, 400)
        pipes.append(Pipe(WIDTH, pipe_height))

    for pipe in pipes:
        pipe.move(pipe_speed)

    # Engelleri ekrandan kaybolduğunda sil
    pipes = [pipe for pipe in pipes if pipe.is_visible()]

    # Ekranı temizle
    screen.fill(WHITE)

    # Engelleri çiz
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, (pipe.x, 0, pipe_width, pipe.height))  # Üst boru
        pygame.draw.rect(screen, GREEN, (pipe.x, pipe.height + pipe_gap, pipe_width, HEIGHT - pipe.height - pipe_gap))  # Alt boru

    # Çarpışma kontrolü
    for pipe in pipes:
        upper_pipe = pygame.Rect(pipe.x, 0, pipe_width, pipe.height)
        lower_pipe = pygame.Rect(pipe.x, pipe.height + pipe_gap, pipe_width, HEIGHT - pipe.height - pipe_gap)
        if bird_rect.colliderect(upper_pipe) or bird_rect.colliderect(lower_pipe):
            running = False

        # Skor kontrolü
        if pipe.x + pipe_width < bird_rect.x and not pipe.scored:
            score += 1
            pipe.scored = True

    # Kuşun ekrandan dışarı çıkma kontrolü
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        running = False

    # Kuşu ekranda göster
    screen.blit(bird_img, bird_rect)

    # Skoru göster
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Ekranı güncelle
    pygame.display.update()

    # FPS
    clock.tick(60)

# PyGame'i kapat
pygame.quit()