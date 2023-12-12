import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
STATE_WIDTH, STATE_HEIGHT = 720, 720
TILE_SIZE = 60
GRID_WIDTH = STATE_WIDTH // TILE_SIZE
GRID_HEIGHT = STATE_HEIGHT // TILE_SIZE
CAR_HEIGHT = 60
CAR_WIDTH = 40
FPS = 60
BACKGROUND_COLOR = (160, 160, 160)
CAR_SPEED = 60


# Create the game window
screen = pygame.display.set_mode((STATE_WIDTH, STATE_HEIGHT))
pygame.display.set_caption("Car Parking Game")
clock = pygame.time.Clock()

# Load car sprites for all 4 orientations
car_images = [pygame.image.load("assets/car-up.png"), pygame.image.load("assets/car-down.png"), pygame.image.load("assets/car-left.png"), pygame.image.load("assets/car-right.png")]
obstacle_image = pygame.image.load("assets/obstacle.png")


def grid_to_pixels(x, y):
    return x * TILE_SIZE, y * TILE_SIZE


def get_random_car_position():
    car_tile = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    car_rect = pygame.Rect(grid_to_pixels(*car_tile), (TILE_SIZE, TILE_SIZE))
    car_rect.x += (TILE_SIZE - CAR_WIDTH) // 2
    car_rect.y += (TILE_SIZE - CAR_HEIGHT) // 2
    return car_rect

def get_random_orientation():
    return random.choice(["up", "down", "left", "right"])

def get_random_obstacle_positions():
    obstacle_rects = []
    while len(obstacle_rects) < 4:
        obstacle_tile = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        obstacle_rect = pygame.Rect(grid_to_pixels(*obstacle_tile), (TILE_SIZE, TILE_SIZE))

        overlap = False
        for existing_obstacle in obstacle_rects:
            if obstacle_rect.colliderect(existing_obstacle):
                overlap = True
                break
        if not overlap:
            obstacle_rects.append(obstacle_rect)

    return obstacle_rects

def get_random_parking_position():
    lot_tile = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    return pygame.Rect(grid_to_pixels(*lot_tile), (TILE_SIZE, TILE_SIZE))

car_rect = get_random_car_position()
car_orientation = get_random_orientation()
parking_rect = get_random_parking_position()
obstacles_rect = get_random_obstacle_positions()





while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3: # 3 to go straight
                if car_orientation == "up":
                    car_rect.y -= CAR_SPEED
                elif car_orientation == "down":
                    car_rect.y += CAR_SPEED
                elif car_orientation == "left":
                    car_rect.x -= CAR_SPEED
                elif car_orientation == "right":
                    car_rect.x += CAR_SPEED

            elif event.key == pygame.K_4: # 4 to go backwards
                if car_orientation == "up":
                    car_rect.y += CAR_SPEED
                elif car_orientation == "down":
                    car_rect.y -= CAR_SPEED
                elif car_orientation == "left":
                    car_rect.x += CAR_SPEED
                elif car_orientation == "right":
                    car_rect.x -= CAR_SPEED

            elif event.key == pygame.K_1: # 1 for turning left
                if car_orientation == "up":
                    car_orientation = "left"
                elif car_orientation == "down":
                    car_orientation = "right"
                elif car_orientation == "left":
                    car_orientation = "down"
                elif car_orientation == "right":
                    car_orientation = "up"

            elif event.key == pygame.K_2:  # 2 for turning right
                if car_orientation == "up":
                    car_orientation = "right"
                elif car_orientation == "down":
                    car_orientation = "left"
                elif car_orientation == "left":
                    car_orientation = "up"
                elif car_orientation == "right":
                    car_orientation = "down"


    # Check if the car is inside the parking lot
    if parking_rect.colliderect(car_rect):
        pygame.quit()
        sys.exit()

    if car_rect.left < 0:
        car_rect.left = 0
    elif car_rect.right > STATE_WIDTH:
        car_rect.right = STATE_WIDTH
    if car_rect.top < 0:
        car_rect.top = 0
    elif car_rect.bottom > STATE_HEIGHT:
        car_rect.bottom = STATE_HEIGHT



    # Update the display
    screen.fill(BACKGROUND_COLOR)
    car_sprite = None
    if car_orientation == "up":
        car_sprite = car_images[0]
    elif car_orientation == "down":
        car_sprite = car_images[1]
    elif car_orientation == "left":
        car_sprite = car_images[2]
    elif car_orientation == "right":
        car_sprite = car_images[3]

    for obstacle_rect in obstacles_rect:
        if car_rect.colliderect(obstacle_rect):
            break

    screen.blit(car_sprite, car_rect)
    for obstacle_rect in obstacles_rect:
        screen.blit(obstacle_image, obstacle_rect)
    pygame.draw.rect(screen, (255, 255, 0), parking_rect)

    pygame.display.flip()
    pygame.time.delay(200)
    clock.tick(FPS)
