import pygame
import os
import random
import time

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Make 10 Game - Ocean Quest")

# Asset paths
ASSETS_PATH = "assets"
TURTLE_IMAGES = [f"{i}.png" for i in range(1, 11)]  # Generates the buttons 1 to 9 and 0
MASCOT_HAPPY = "bubbly_happy.png"
MASCOT_SAD = "bubbly_sad.png"
BACKGROUND_IMAGE = "game_bg.png"

# Load background
try:
    bg_image = pygame.image.load(os.path.join(ASSETS_PATH, BACKGROUND_IMAGE))
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
except:
    bg_image = pygame.Surface((WIDTH, HEIGHT))
    bg_image.fill((0, 0, 100))

# Load turtle buttons (1-9)
buttons = []
for idx, filename in enumerate(TURTLE_IMAGES):
    try:
        image = pygame.image.load(os.path.join(ASSETS_PATH, filename))
        image = pygame.transform.scale(image, (80, 80))
    except:
        # Create placeholder if image fails to load
        image = pygame.Surface((80, 80))
        image.fill((100, 200, 100))
        number = idx + 1  # 1-9
        text = pygame.font.SysFont(None, 40).render(str(number), True, (0, 0, 0))
        image.blit(text, (30, 30))

    x = 100 + (idx % 5) * 120
    y = 300 + (idx // 5) * 120
    rect = pygame.Rect(x, y, 80, 80)
    buttons.append({"image": image, "rect": rect, "value": idx + 1})

# Load mascot images
try:
    mascot_happy = pygame.image.load(os.path.join(ASSETS_PATH, MASCOT_HAPPY))
    mascot_happy = pygame.transform.scale(mascot_happy, (100, 100))
    mascot_sad = pygame.image.load(os.path.join(ASSETS_PATH, MASCOT_SAD))
    mascot_sad = pygame.transform.scale(mascot_sad, (100, 100))
except:
    # Create placeholders if mascot images fail to load
    mascot_happy = pygame.Surface((100, 100))
    mascot_happy.fill((255, 255, 0))
    mascot_sad = pygame.Surface((100, 100))
    mascot_sad.fill((255, 0, 0))

# Game variables
possible_numbers = list(range(1, 10)) + list(range(11, 20))
current_number = random.choice(possible_numbers)
operation = "+"
mascot_state = "neutral"
score = 0
rounds_played = 0
TOTAL_ROUNDS = 10
game_active = True
waiting_for_next = False
wait_time = 0

# Font setup
font = pygame.font.SysFont('Arial', 36)
large_font = pygame.font.SysFont('Arial', 72)


def draw_text(text, pos, color=(255, 255, 255), font_type=font):
    rendered = font_type.render(text, True, color)
    screen.blit(rendered, pos)


def reset_round():
    global current_number, mascot_state, waiting_for_next, wait_time
    current_number = random.choice(possible_numbers)
    mascot_state = "neutral"
    waiting_for_next = False
    wait_time = 0


def draw_game_screen():
    # Draw number and operation
    draw_text(f"Make 10: {current_number} {operation} ?", (50, 50))
    draw_text(f"Score: {score}/{rounds_played}", (50, 100))
    draw_text(f"Round: {rounds_played + 1}/{TOTAL_ROUNDS}", (50, 150))
    draw_text("Press + or - to change symbol", (50, 220), (200, 200, 255))

    # Draw mascot
    if mascot_state == "happy":
        screen.blit(mascot_happy, (650, 50))
    elif mascot_state == "sad":
        screen.blit(mascot_sad, (650, 50))

    # Draw turtle buttons (1-9)
    for btn in buttons:
        screen.blit(btn["image"], btn["rect"])


def draw_game_over():
    screen.fill((0, 0, 100))
    draw_text("Game Over!", (WIDTH // 2 - 150, HEIGHT // 2 - 100), (255, 255, 0), large_font)
    draw_text(f"Final Score: {score}/{TOTAL_ROUNDS}", (WIDTH // 2 - 150, HEIGHT // 2), (255, 255, 255), large_font)
    draw_text("Click or press any key to play again", (WIDTH // 2 - 250, HEIGHT // 2 + 100), (200, 200, 255))


# Main game loop
running = True
clock = pygame.time.Clock()
last_time = time.time()

while running:
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_active and not waiting_for_next:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for btn in buttons:
                    if btn["rect"].collidepoint((mx, my)):
                        chosen = btn["value"]  # Gets 1-9
                        result = current_number + chosen if operation == "+" else current_number - chosen
                        if result == 10:
                            mascot_state = "happy"
                            score += 1
                        else:
                            mascot_state = "sad"
                        rounds_played += 1
                        waiting_for_next = True
                        wait_time = 1.0  # 1 second delay

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    operation = "+"
                elif event.key == pygame.K_MINUS:
                    operation = "-"
        else:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # Reset game if any key is pressed or mouse is clicked
                if not game_active or (waiting_for_next and rounds_played >= TOTAL_ROUNDS):
                    score = 0
                    rounds_played = 0
                    game_active = True
                    reset_round()

    # Update game state
    if waiting_for_next:
        wait_time -= delta_time
        if wait_time <= 0:
            if rounds_played < TOTAL_ROUNDS:
                reset_round()
            else:
                game_active = False

    # Drawing
    screen.blit(bg_image, (0, 0))

    if game_active:
        draw_game_screen()
    else:
        draw_game_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()