import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 720, 720
TILE_SIZE = 60
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
CAR_HEIGHT = 60
CAR_WIDTH = 40
FPS = 60
WHITE = (255, 255, 255)
CAR_SPEED = 60


# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Parking Game")
clock = pygame.time.Clock()

# Load car sprites for all 4 orientations
car_up = pygame.image.load("assets/car-up.png")
car_down = pygame.image.load("assets/car-down.png")
car_left = pygame.image.load("assets/car-left.png")
car_right = pygame.image.load("assets/car-right.png")


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

def get_random_parking_position():
    lot_tile = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    return pygame.Rect(grid_to_pixels(*lot_tile), (TILE_SIZE, TILE_SIZE))

car_rect = get_random_car_position()
car_orientation = get_random_orientation()
parking_lot = get_random_parking_position()




while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                if car_orientation == "up":
                    car_rect.y -= CAR_SPEED
                elif car_orientation == "down":
                    car_rect.y += CAR_SPEED
                elif car_orientation == "left":
                    car_rect.x -= CAR_SPEED
                elif car_orientation == "right":
                    car_rect.x += CAR_SPEED

            elif event.key == pygame.K_4:
                if car_orientation == "up":
                    car_rect.y += CAR_SPEED
                elif car_orientation == "down":
                    car_rect.y -= CAR_SPEED
                elif car_orientation == "left":
                    car_rect.x += CAR_SPEED
                elif car_orientation == "right":
                    car_rect.x -= CAR_SPEED

            elif event.key == pygame.K_1:
                if car_orientation == "up":
                    car_orientation = "left"
                elif car_orientation == "down":
                    car_orientation = "right"
                elif car_orientation == "left":
                    car_orientation = "down"
                elif car_orientation == "right":
                    car_orientation = "up"

            elif event.key == pygame.K_2:  # Numeric keypad 2 for turning right
                if car_orientation == "up":
                    car_orientation = "right"
                elif car_orientation == "down":
                    car_orientation = "left"
                elif car_orientation == "left":
                    car_orientation = "up"
                elif car_orientation == "right":
                    car_orientation = "down"


    # Check if the car is inside the parking lot
    if parking_lot.colliderect(car_rect):
        print("Game Over - You parked the car!")
        pygame.quit()
        sys.exit()

    if car_rect.left < 0:
        car_rect.left = 0
    elif car_rect.right > WIDTH:
        car_rect.right = WIDTH
    if car_rect.top < 0:
        car_rect.top = 0
    elif car_rect.bottom > HEIGHT:
        car_rect.bottom = HEIGHT



    # Update the display
    screen.fill(WHITE)
    car_sprite = None
    if car_orientation == "up":
        car_sprite = car_up
    elif car_orientation == "down":
        car_sprite = car_down
    elif car_orientation == "left":
        car_sprite = car_left
    elif car_orientation == "right":
        car_sprite = car_right



    screen.blit(car_sprite, car_rect)
    pygame.draw.rect(screen, (0, 255, 0), parking_lot)

    pygame.display.flip()
    pygame.time.delay(200)
    clock.tick(FPS)
