import pygame
import random
import sys

# Initialize pygame
pygame.init()

#for sound & music
pygame.mixer.init()


# Background music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(0.5)  # set volume 0.0–1.0

# Bottle breaking sound
break_sound = pygame.mixer.Sound("break.wav")
break_sound.set_volume(0.7)


# Window dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Little smasher")

# Load assets
menu_bg_image = pygame.image.load("front.jpg")
menu_bg_image = pygame.transform.scale(menu_bg_image, (WIDTH, HEIGHT))


bg_image = pygame.image.load("background.jpg")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

player_img = pygame.image.load("stoner.png")
player_img = pygame.transform.scale(player_img, (90, 90))

ball_img = pygame.image.load("stone.png")
ball_img = pygame.transform.scale(ball_img, (20, 20))

# Load bottle images
bottle_images = [
    pygame.image.load("assets/bottles/bottle_red.png"),
    pygame.image.load("assets/bottles/bottle_blue.png"),
    pygame.image.load("assets/bottles/bottle_green.png"),
    pygame.image.load("assets/bottles/bottle_pink.png"),
    pygame.image.load("assets/bottles/bottle_yellow.png"),
    pygame.image.load("assets/bottles/bottle_purple.png"),
]
bottle_images = [pygame.transform.scale(img, (50, 80)) for img in bottle_images]

font = pygame.font.SysFont("comicsans", 30)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game variables
player_x, player_y = WIDTH//6, HEIGHT//2
balls = []
obstacles = []
score = 0
ball_count = 5
ball_speed = 10
obstacle_timer = 0
speed = 5

# Button class
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, (200, 200, 255), self.rect, border_radius=12)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=12)
        txt = font.render(self.text, True, BLACK)
        screen.blit(txt, (self.rect.x + 20, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Obstacle class with image
class Obstacle:
    def __init__(self, x, y):
        self.image = random.choice(bottle_images)
        self.rect = self.image.get_rect(midbottom=(x, y))

    def move(self):
        self.rect.x -= speed

    def draw(self):
        screen.blit(self.image, self.rect)

def spawn_obstacle():
    x = WIDTH + 50
    y = random.randint(200, HEIGHT - 40)
    return Obstacle(x, y)

def reset_game():
    global balls, obstacles, score, ball_count, player_y, obstacle_timer
    balls = []
    obstacles = []
    score = 0
    ball_count = 10
    player_y = HEIGHT//2
    obstacle_timer = 0

def draw_game():
    screen.blit(bg_image, (0, 0))
    screen.blit(player_img, (player_x - 30, player_y - 30))
    for ball in balls:
        screen.blit(ball_img, ball)
    for obs in obstacles:
        obs.draw()
    
    txt = font.render(f"Balls: {ball_count}  Score: {score}", True, BLACK)
    screen.blit(txt, (10, 10))

# Buttons
start_button = Button(WIDTH//2 - 60, HEIGHT//2 - 60, 120, 50, "Start")
restart_button = Button(WIDTH//2 - 60, HEIGHT//2, 140, 50, "Restart")
quit_button = Button(WIDTH//2 - 60, HEIGHT//2 + 60, 120, 50, "Quit")

# Game loop control
clock = pygame.time.Clock()
run_game = False
in_menu = True

while True:
    screen.blit(menu_bg_image, (0, 0))

    if in_menu:
        screen.blit(menu_bg_image, (0, 0))
        start_button.draw()
        restart_button.draw()
        quit_button.draw()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(event.pos):
                    run_game = True
                    in_menu = False
                    pygame.mixer.music.play(-1)  # Start background music
                elif restart_button.is_clicked(event.pos):
                    reset_game()
                    run_game = True
                    in_menu = False
                    pygame.mixer.music.play(-1)  # Start background music
                elif quit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()
        continue

    if run_game and ball_count <= 0:
        run_game = False
        in_menu = True
        pygame.mixer.music.stop()  # Stop background music
        continue

    clock.tick(60)
    draw_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and ball_count > 0:
                balls.append(pygame.Rect(player_x + 30, player_y - 10, 20, 20))
                ball_count -= 1
            elif event.key == pygame.K_UP:
                player_y = max(player_y - 20, 50)
            elif event.key == pygame.K_DOWN:
                player_y = min(player_y + 20, HEIGHT - 50)
            elif event.key == pygame.K_ESCAPE:
                in_menu = True

    # Update ball positions
    for ball in balls:
        ball.x += ball_speed
    balls = [b for b in balls if b.x < WIDTH]

    # Obstacle generation
    obstacle_timer += 1
    if obstacle_timer > 50:
        obstacles.append(spawn_obstacle())
        obstacle_timer = 0

    # Update obstacles
    for obs in obstacles:
        obs.move()
    obstacles = [obs for obs in obstacles if obs.rect.right > 0]

    # Collision check
    hit_list = []
    for ball in balls:
        for obs in obstacles:
            if ball.colliderect(obs.rect):
                score += 1
                ball_count += 2
                hit_list.append((ball, obs))
                break_sound.play()
    for ball, obs in hit_list:
        if ball in balls:
            balls.remove(ball)
        if obs in obstacles:
            obstacles.remove(obs)

    pygame.display.flip()
