import pygame
import sys
import math
import logging
import random

# Initialize logging
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Shooter Game")

# Font for displaying text 
font = pygame.font.Font(None, 36)

# Level settings
levels = {
    '1': {'background': 'Game.jpg', 'speed': 0.05, 'projectile_speed': 5},
    '2': {'background': 'Game.jpg', 'speed': 0.1, 'projectile_speed': 5},
    '3': {'background': 'Game3.jpg', 'speed': 0.5, 'projectile_speed': 5},
}
# Function to display text
def render_text(text, font, color, surface, x, y): 
    text_obj = font.render(text, True, color) 
    text_rect = text_obj.get_rect() 
    text_rect.topleft = (x, y) 
    surface.blit(text_obj, text_rect)
    
# Main menu function
def main_menu(): 
    while True: 
        screen.fill((0, 0, 0)) # Fill the screen with black 
        render_text('Choose a level (1, 2, or 3):', font, (255, 255, 255), screen, 20, 20)
        
        pygame.display.flip() 
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: 
                    return '1' 
                elif event.key == pygame.K_2: 
                    return '2' 
                elif event.key == pygame.K_3: 
                    return '3' 
            
# Main function  
level_choice = main_menu() 
    
# Validate input
while level_choice not in levels: 
    level_choice = main_menu() 
        
# Load level settings
background_image = pygame.image.load(levels[level_choice]['background'])
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)) # Scale to screen size 
falling_speed = levels[level_choice]['speed']
projectile_speed = levels[level_choice]['projectile_speed'] 
    
# Set shooter's starting position to the center 
start_x = SCREEN_WIDTH // 2 - 25 # Center x 
start_y = SCREEN_HEIGHT - 50 # Bottom of the screen 
    
# Initialize score and lives 
score = 0
lives = 3

# Load tank image
tank_image = pygame.image.load('C:/Users/raagh/OneDrive/Desktop/pyscript_game/tank.png')
tank_image = pygame.transform.scale(tank_image, (150, 50)) # Adjust the size as needed

# Shooter class
class Shooter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0  # Initial angle set to 90 (facing up)
        logging.info("Shooter initialized at position (%d, %d) with angle %d", self.x, self.y, self.angle)

    def draw(self, screen):
        rotated_tank = pygame.transform.rotate(tank_image, self.angle) # Rotate the tank image based on angle
        screen.blit(rotated_tank, (self.x, self.y))
        logging.debug("Shooter drawn at position (%d, %d) with angle %d", self.x, self.y, self.angle)

    def update_angle(self, new_angle):
        self.angle = max(0, min(new_angle, 180))  # Limit angle between 0 and 180 degrees
        logging.info("Shooter angle changed to %d", self.angle)

# Falling object class
class FallingObject:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        logging.info("Falling object created at position (%d, %d) with speed %d and color %s", self.x, self.y, self.speed, self.color)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 15)
        logging.debug("Falling object drawn at position (%d, %d)", self.x, self.y)

    def update_position(self):
        self.y += self.speed
        logging.debug("Falling object moved to position (%d, %d)", self.x, self.y)

# Projectile class
class Projectile:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        #logging.info("Projectile created at position (%d, %d) with angle %d", self.x, self.y, self.angle)

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), 7)
        #logging.debug("Projectile drawn at position (%d, %d)", self.x, self.y)

    def update_position(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))
        #logging.debug("Projectile moved to position (%d, %d)", self.x, self.y)

# Check collision function
def check_collision(object1, object2):
    distance = ((object1.x - object2.x) ** 2 + (object1.y - object2.y) ** 2) ** 0.5
    collision = distance < 15  # Adjust based on size
    #logging.debug("Checking collision: %s", collision)
    return collision

# Define custom events
ADD_OBJECT_EVENT = pygame.USEREVENT + 1
FIRE_PROJECTILE_EVENT = pygame.USEREVENT + 2

# Instantiate objects
shooter = Shooter(start_x, SCREEN_HEIGHT - 50)
falling_objects = []

# Add falling objects continuously
ADD_OBJECT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_OBJECT_EVENT, 3000)  # Add new object every second

projectiles = []

# Font for displaying score
font = pygame.font.Font(None, 36)

# Game loop
running = True
fire_projectile = False  # Flag to control firing

logging.info("Game loop started")
while running:
    logging.info("Game loop running")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            logging.info("Game loop ended by user")
        if event.type == ADD_OBJECT_EVENT:
            x = random.randint(0, SCREEN_WIDTH)
            falling_objects.append(FallingObject(x, 0, falling_speed, (255, 0, 0)))  # Slower speed and random position
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fire_projectile = True  # Start firing
                pygame.time.set_timer(FIRE_PROJECTILE_EVENT, 100)  # Fire every 100 milliseconds (0.1 seconds)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                fire_projectile = False  # Stop firing
                pygame.time.set_timer(FIRE_PROJECTILE_EVENT, 0)  # Stop the timer
        if event.type == FIRE_PROJECTILE_EVENT and fire_projectile:
            projectiles.append(Projectile(shooter.x, shooter.y, shooter.angle, projectile_speed))
            logging.info("Projectile shot at angle %d", shooter.angle)

    # Continuously update angle while keys are pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        shooter.update_angle(shooter.angle + 0.1)  # Adjust the step size as needed
    if keys[pygame.K_RIGHT]:
        shooter.update_angle(shooter.angle - 0.1)

    screen.blit(background_image, (0, 0))  # Draw background image

    # Update and draw falling objects
    #for obj in falling_objects:
        
    for obj in falling_objects:
        obj.update_position()
        obj.draw(screen)
        if obj.y > SCREEN_HEIGHT:
            falling_objects.remove(obj)
            logging.info("Falling object removed at position (%d, %d)", obj.x, obj.y)
            lives -= 1 # Decrease lives by 1
            if lives == 0: running = False # End game when lives are 0

    # Update and draw projectiles
    #for proj in projectiles:
        
    for proj in projectiles:
        proj.update_position()
        proj.draw(screen)
        # Check for collisions
        for obj in falling_objects:
            if check_collision(proj, obj):
                projectiles.remove(proj)
                falling_objects.remove(obj)
                #logging.info("Collision detected and objects removed: projectile at (%d, %d) and falling object at (%d, %d)", proj.x, proj.y, obj.x, obj.y)
                score += 10 # Increment score by 10
                break

    # Draw shooter
    shooter.draw(screen)

    # Render and display the score and lives
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    logging.info("score displayed")
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (SCREEN_WIDTH - 100, 10))
    logging.info("lives displayed")

    pygame.display.flip()

#Display game over screen
screen.fill((0, 0, 0))
logging.info("Game over screen displayed")
game_over_text = font.render(f"Game Over! Final Score: {score}", True, (255, 255, 255))
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
logging.info("Pygame terminated")
sys.exit()
