import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
CAR_SPEED = 5


# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Parking Game")
clock = pygame.time.Clock()

# Load car sprites for all 4 orientations
car_up = pygame.image.load("assets/car-up.png")
car_down = pygame.image.load("assets/car-down.png")
car_left = pygame.image.load("assets/car-left.png")
car_right = pygame.image.load("assets/car-right.png")

# Initial car position, orientation, and parking lot location (randomized)
car_rect = car_up.get_rect(center=(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))
car_orientation = random.choice(["up", "down", "left", "right"])

# Randomized parking lot location
parking_lot = pygame.Rect(random.randint(50, WIDTH - 200), random.randint(50, HEIGHT - 200), 150, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:  # Numeric keypad 3 for going forward
                if car_orientation == "up":
                    car_rect.y -= CAR_SPEED
                elif car_orientation == "down":
                    car_rect.y += CAR_SPEED
                elif car_orientation == "left":
                    car_rect.x -= CAR_SPEED
                elif car_orientation == "right":
                    car_rect.x += CAR_SPEED

            elif event.key == pygame.K_4:  # Numeric keypad 4 for going backward
                if car_orientation == "up":
                    car_rect.y += CAR_SPEED
                elif car_orientation == "down":
                    car_rect.y -= CAR_SPEED
                elif car_orientation == "left":
                    car_rect.x += CAR_SPEED
                elif car_orientation == "right":
                    car_rect.x -= CAR_SPEED

            elif event.key == pygame.K_1:  # Numeric keypad 1 for turning left
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

    print(car_orientation)

    # Check if the car is inside the parking lot
    if parking_lot.colliderect(car_rect):
        print("Game Over - You parked the car!")
        pygame.quit()
        sys.exit()

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

    print(car_sprite)

    screen.blit(car_sprite, car_rect)
    pygame.draw.rect(screen, (0, 255, 0), parking_lot)

    pygame.display.flip()
    clock.tick(FPS)