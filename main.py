import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up display
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRADIENT_START = (30, 40, 50)
GRADIENT_END = (15, 25, 35)

# Game variables
block_size = 20
snake_speed = 15
snake_eye_size = 4
particles = []

# Initialize clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)

# Create gradient background
def draw_gradient():
    for y in range(dis_height):
        # Linear interpolation between gradient colors
        r = GRADIENT_START[0] + (GRADIENT_END[0] - GRADIENT_START[0]) * y / dis_height
        g = GRADIENT_START[1] + (GRADIENT_END[1] - GRADIENT_START[1]) * y / dis_height
        b = GRADIENT_START[2] + (GRADIENT_END[2] - GRADIENT_START[2]) * y / dis_height
        pygame.draw.line(dis, (int(r), int(g), int(b)), (0, y), (dis_width, y))

# Particle effect class
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.lifetime = 30

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self):
        alpha = int(255 * self.lifetime / 30)
        pygame.draw.circle(dis, (255, 215, 0), (int(self.x), int(self.y)), 3)

# Rotated snake head
def draw_snake_head(position, direction):
    head_rect = pygame.Rect(position[0], position[1], block_size, block_size)
    angle = 0
    if direction == "LEFT":
        angle = 180
    elif direction == "UP":
        angle = 90
    elif direction == "DOWN":
        angle = 270
        
    # Draw snake head with eyes
    pygame.draw.rect(dis, GREEN, head_rect, border_radius=5)
    
    # Calculate eye positions
    eye_offset = block_size // 3
    if direction == "RIGHT":
        eye1 = (position[0] + block_size - eye_offset, position[1] + eye_offset)
        eye2 = (position[0] + block_size - eye_offset, position[1] + block_size - eye_offset)
    elif direction == "LEFT":
        eye1 = (position[0] + eye_offset, position[1] + eye_offset)
        eye2 = (position[0] + eye_offset, position[1] + block_size - eye_offset)
    elif direction == "UP":
        eye1 = (position[0] + eye_offset, position[1] + eye_offset)
        eye2 = (position[0] + block_size - eye_offset, position[1] + eye_offset)
    else:  # DOWN
        eye1 = (position[0] + eye_offset, position[1] + block_size - eye_offset)
        eye2 = (position[0] + block_size - eye_offset, position[1] + block_size - eye_offset)
    
    pygame.draw.circle(dis, WHITE, eye1, snake_eye_size)
    pygame.draw.circle(dis, WHITE, eye2, snake_eye_size)

# Glowing food effect
def draw_food(x, y, frame):
    # Pulse animation
    pulse = math.sin(frame * 0.1) * 2 + 3
    glow_size = block_size + int(pulse)
    
    # Glowing effect
    for i in range(3):
        alpha = 50 * (3 - i)
        glow_rect = pygame.Rect(x - pulse + i*2, y - pulse + i*2, 
                              block_size + pulse*2 - i*4, block_size + pulse*2 - i*4)
        pygame.draw.rect(dis, (255, 40 + i*20, 0, alpha), glow_rect, border_radius=8)
    
    # Main food
    pygame.draw.rect(dis, RED, (x, y, block_size, block_size), border_radius=8)

def game_loop():
    global particles
    game_over = False
    game_close = False
    frame = 0

    start_x = dis_width // 2
    start_y = dis_height // 2
    snake_list = [[start_x - i * block_size, start_y] for i in range(3)]
    x1_change = block_size
    y1_change = 0
    direction = "RIGHT"

    food_x, food_y = generate_food(snake_list)
    score = 0

    while not game_over:
        frame += 1
        dis.fill(BLACK)
        draw_gradient()

        while game_close:
            # Dark overlay
            overlay = pygame.Surface((dis_width, dis_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            dis.blit(overlay, (0, 0))
            
            # Game over text
            game_over_text = title_font.render("GAME OVER", True, RED)
            dis.blit(game_over_text, (dis_width//2 - game_over_text.get_width()//2, dis_height//2 - 60))
            
            # Score display
            score_text = font.render(f"Score: {score}", True, WHITE)
            dis.blit(score_text, (dis_width//2 - score_text.get_width()//2, dis_height//2))
            
            # Restart prompt
            restart_text = font.render("Press SPACE to restart or ESC to quit", True, WHITE)
            dis.blit(restart_text, (dis_width//2 - restart_text.get_width()//2, dis_height//2 + 60))
            
            pygame.display.update()

            # Handle game over input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_SPACE:
                        game_loop()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    x1_change = -block_size
                    y1_change = 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    x1_change = block_size
                    y1_change = 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    y1_change = -block_size
                    x1_change = 0
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    y1_change = block_size
                    x1_change = 0
                    direction = "DOWN"

        # Update snake position
        new_head = [snake_list[0][0] + x1_change, snake_list[0][1] + y1_change]

        # Collision detection
        if (new_head[0] >= dis_width or new_head[0] < 0 or
            new_head[1] >= dis_height or new_head[1] < 0 or
            new_head in snake_list[1:]):
            game_close = True

        snake_list.insert(0, new_head)

        # Food collision
        if new_head[0] == food_x and new_head[1] == food_y:
            score += 10
            food_x, food_y = generate_food(snake_list)
            # Add particles
            for _ in range(15):
                particles.append(Particle(food_x + block_size//2, food_y + block_size//2))
        else:
            snake_list.pop()

        # Update particles
        particles = [p for p in particles if p.lifetime > 0]
        for p in particles:
            p.update()

        # Draw elements
        # Draw particles
        for p in particles:
            p.draw()

        # Draw snake with gradient body
        for i, pos in enumerate(snake_list):
            if i == 0:
                draw_snake_head(pos, direction)
            else:
                alpha = 200 - (i * 5)
                if alpha < 50:
                    alpha = 50
                body_color = (0, 255 - (i * 3), 0, alpha)
                pygame.draw.rect(dis, body_color, (pos[0], pos[1], block_size, block_size), border_radius=5)

        # Draw food with animation
        draw_food(food_x, food_y, frame)

        # Score display
        score_text = font.render(f"Score: {score}", True, WHITE)
        dis.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Generate food function (same as before)
def generate_food(snake_list):
    while True:
        food_x = random.randrange(0, dis_width, block_size)
        food_y = random.randrange(0, dis_height, block_size)
        if [food_x, food_y] not in snake_list:
            return (food_x, food_y)

# Start the game
game_loop()