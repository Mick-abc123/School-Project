import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLATFORM_WIDTH = 200
PLATFORM_HEIGHT = 20
PLAYER_SIZE = 50
GRAVITY = 0.25
JUMP_SPEED = 15
PLAYER_SPEED = 5

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Level 1")

# Define some colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Load the player image
player_image = pygame.image.load("C:\\Users\\Huettelm23\\Documents\\School-Project-main\\School-Project-main\\Levels\\Player.png")
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))
player_rect = player_image.get_rect()
player_rect.topleft = [100, SCREEN_HEIGHT - 100]

# Load the opponent player image
opponent_player_image = pygame.image.load("C:\\Users\\Huettelm23\\Documents\\School-Project-main\\School-Project-main\\Levels\\oppoplayer.png")
opponent_player_image = pygame.transform.scale(opponent_player_image, (PLAYER_SIZE, PLAYER_SIZE))
opponent_player_rect = opponent_player_image.get_rect()
opponent_player_rect.topleft = [700, SCREEN_HEIGHT - 100]

# Set up the target position and size
target_pos = [700, SCREEN_HEIGHT - 100]
target_size = 50

# Set up the jumping variables
jumping = False
player_y_velocity = 0

# Set up the ground height
ground_height = SCREEN_HEIGHT - 50

# Set up the start time
start_ticks = pygame.time.get_ticks()

# Set up the font for the timer
font = pygame.font.Font(None, 36)

# Function to load level availability
def load_level_availability(filename):
    level_status = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split('=')
                key = key.strip()
                value = value.strip().lower()
                if value in ['available', 'unavailable']:
                    level_status[key] = value
    except FileNotFoundError:
        print(f"Config file {filename} not found.")
    return level_status

# Function to update level availability
def update_level_availability(filename, level_id, new_status):
    level_status = load_level_availability(filename)
    level_status[level_id] = new_status
    with open(filename, 'w') as file:
        for key, value in level_status.items():
            file.write(f"{key} = {value}\n")

# Opponent AI Variables
opponent_jumping = False
opponent_y_velocity = 0
opponent_move_timer = 0
opponent_move_direction = 0
MAX_OPPONENT_MOVE_DISTANCE = 5
OPPONENT_GRAVITY = 0.25
OPPONENT_JUMP_SPEED = 12
GROUND_HEIGHT = SCREEN_HEIGHT - 50

# Opponent AI movement and jumping logic
def update_opponent_movement_and_jumping():
    global opponent_jumping, opponent_y_velocity, opponent_move_timer, opponent_move_direction

    # AI Movement logic (randomly move towards player or stay still)
    if opponent_move_timer > 0:
        opponent_move_timer -= 1
    else:
        # Calculate the horizontal direction towards the player
        dx = player_rect.x - opponent_player_rect.x

        # Simple AI: move towards the player if player is far away horizontally
        if abs(dx) > PLAYER_SIZE:  # If the player is far enough
            if dx > 0:
                opponent_move_direction = 1  # Move right towards player
            else:
                opponent_move_direction = -1  # Move left towards player
        else:
            opponent_move_direction = 0  # Stay still if close enough

        # Randomly reset move timer to avoid immediate response
        opponent_move_timer = random.randint(20, 40)

    # Update opponent's horizontal movement
    if opponent_move_direction != 0:
        move_distance = opponent_move_direction * PLAYER_SPEED
        new_x = opponent_player_rect.x + move_distance

        # Ensure the AI stays within horizontal screen bounds
        if 0 <= new_x <= SCREEN_WIDTH - PLAYER_SIZE:
            opponent_player_rect.x = new_x

    # AI Jumping logic (20% chance of jumping)
    if not opponent_jumping and random.randint(0, 100) < 2:
        opponent_jumping = True
        opponent_y_velocity = -OPPONENT_JUMP_SPEED  # Start jumping upwards

    # Apply gravity and update vertical position when jumping
    if opponent_jumping:
        opponent_player_rect.y += opponent_y_velocity
        opponent_y_velocity += OPPONENT_GRAVITY  # Gravity effect (pull AI downwards)

        # Check if the AI has landed on the ground
        if opponent_player_rect.bottom >= GROUND_HEIGHT:
            opponent_player_rect.bottom = GROUND_HEIGHT  # Snap AI to ground
            opponent_jumping = False  # Stop jumping
            opponent_y_velocity = 0  # Reset vertical velocity

    # Top boundary: Prevent AI from going above the screen
    if opponent_player_rect.top < 0:
        opponent_player_rect.top = 0
        opponent_y_velocity = 0  # Stop any further vertical movement upwards

    # Bottom boundary: Ensure AI stays above the ground level
    if opponent_player_rect.bottom > GROUND_HEIGHT:
        opponent_player_rect.bottom = GROUND_HEIGHT
        opponent_jumping = False  # Stop jumping
        opponent_y_velocity = 0  # Reset velocity

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not jumping:
                jumping = True
                player_y_velocity = -JUMP_SPEED

    # Get the current key presses
    keys = pygame.key.get_pressed()

    # Move the player left and right
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
        player_rect.x += PLAYER_SPEED

    # Handle player jumping
    if jumping:
        player_rect.y += player_y_velocity
        player_y_velocity += GRAVITY

        # Check if the player has landed
        if player_rect.bottom >= ground_height:
            player_rect.bottom = ground_height
            jumping = False
            player_y_velocity = 0

    # Check if the player has reached the target
    if player_rect.colliderect(pygame.Rect(target_pos[0], target_pos[1], target_size, target_size)):
        print("Level 1 completed!")
        update_level_availability('Levelcheck.cfg', 'level_2', 'available')
        pygame.quit()
        sys.exit()

    # Update opponent AI movement and jumping
    update_opponent_movement_and_jumping()

    # Calculate the elapsed time
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer_text = font.render(f"Time: {elapsed_time:.2f} seconds", True, BLACK)

    # Draw everything
    screen.fill(WHITE)
    screen.blit(timer_text, (10, 10))
    screen.blit(player_image, player_rect)
    screen.blit(opponent_player_image, opponent_player_rect)
    pygame.draw.rect(screen, RED, (target_pos[0], target_pos[1], target_size, target_size))
    
    platform_pos = [SCREEN_WIDTH / 2 - PLATFORM_WIDTH / 2, SCREEN_HEIGHT / 2 - PLATFORM_HEIGHT / 2]
    platform_size = [PLATFORM_WIDTH, PLATFORM_HEIGHT]
    pygame.draw.rect(screen, BLACK, (platform_pos[0], platform_pos[1], platform_size[0], platform_size[1]))

    # Update the display
    pygame.display.update()
    pygame.time.Clock().tick(120)
