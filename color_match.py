import pygame
import random

#Setting up basic colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND = (232, 232, 232)
global score_list
score_list = [0]

#Setting up the Pyagme window
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
pygame.init() 
pygame.font.init()
SCREEN = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
pygame.display.set_caption('Color Match')
SCREEN.fill(BACKGROUND)
pygame.font.init() #Allows me to use fonts in the program

#Class that makes circles objects (allows for checking for collision with the mouth)
class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def move(self, dx, dy):
        self.center = (self.center[0] + dx, self.center[1] + dy)

    def collidepoint(self, point):
        return (point[0] - self.center[0]) ** 2 + (point[1] - self.center[1]) ** 2 <= self.radius ** 2


#Setting up initial colors
def color_setup():
    global red_circle
    red_circle = Circle((200, 700), 80)
    pygame.draw.circle(SCREEN, RED, (200, 700), 80)
    pygame.display.update()

    global green_circle
    green_circle = Circle((400, 700), 80)
    pygame.draw.circle(SCREEN, GREEN, (400, 700), 80)
    pygame.display.update()

    global blue_circle
    blue_circle = Circle((600, 700), 80)
    pygame.draw.circle(SCREEN, BLUE, (600, 700), 80)
    pygame.display.update()

    global white_circle
    white_circle = Circle((300, 550), 80)
    pygame.draw.circle(SCREEN, WHITE, (300, 550), 80)
    pygame.display.update()

    global black_circle
    black_circle = Circle((500, 550), 80)
    pygame.draw.circle(SCREEN, BLACK, (500, 550), 80)
    pygame.display.update()

    font = pygame.font.Font(None, 36)
    initial_text = font.render('No Color Yet', True, WHITE, BLACK)
    inital_text_rect = initial_text.get_rect(center = ((WINDOW_WIDTH/2), 300))
    SCREEN.blit(initial_text, inital_text_rect)
    pygame.display.update()

#Makes the random color
def making_random_color():
    global red_value, green_value, blue_value
    red_value = random.randint(0, 255)
    green_value = random.randint(0, 255)
    blue_value = random.randint(0, 255)
    random_color = (red_value, green_value, blue_value)
    return random_color

#Shows the random color
def showing_random_color():
    pygame.draw.circle(SCREEN, (making_random_color()), ((WINDOW_WIDTH/2), 100), 80)
    pygame.display.update()

def highscore():
    dimension = (200, 200)
    position = (0, 85.25)
    rectangle = pygame.Rect(position, dimension)
    pygame.draw.rect(SCREEN, BACKGROUND, rectangle)
    pygame.display.update()

    highscore = max(score_list)
    font = pygame.font.Font(None, 36)
    highscore_text = font.render(f'Highest: {highscore}%', True, WHITE, BLACK)
    highscore_text_rect = highscore_text.get_rect(center = ((150, 235.25)))
    SCREEN.blit(highscore_text, highscore_text_rect)
    pygame.display.update()

#Checks percent accuracy
def percent():
    dimension = (100, 100)
    position = (0, 60)
    rectangle = pygame.Rect(position, dimension)
    pygame.draw.rect(SCREEN, BACKGROUND, rectangle)
    pygame.display.update()
    # Maximum possible difference for any color component
    max_difference = 255
    percent_red = (abs(red - red_value) / max_difference) * 100
    percent_green = (abs(green - green_value) / max_difference) * 100
    percent_blue = (abs(blue - blue_value) / max_difference) * 100
    percent_error = (percent_red + percent_green + percent_blue) / 3
    percent_correct = 100 - percent_error
    if percent_correct < 0:
        percent_correct = 0
    rounded_percent = round(percent_correct, 1)
    

    # Draw new percent text
    font = pygame.font.Font(None, 36)
    rounded_percent_text = font.render(f'Current: {rounded_percent}%', True, WHITE, BLACK)
    rounded_percent_rect = rounded_percent_text.get_rect(center=((150, 260)))
    SCREEN.blit(rounded_percent_text, rounded_percent_rect)
    pygame.display.update()
    score_list.append(rounded_percent)

    accuracies_text = font.render(f'Accuracies:', True, WHITE, BLACK)
    accuracies_text_rect = accuracies_text.get_rect(center = ((150, 210)))
    SCREEN.blit(accuracies_text, accuracies_text_rect)
    pygame.display.update()

def player_color():
    player_circle = Circle((400, 300), 80)
    global red, green, blue
    red, green, blue = None, None, None  # Start with color components undefined

    dimension = (300, 200)
    position = (280, 200)
    rectangle = pygame.Rect(position, dimension)
    pygame.draw.rect(SCREEN, BACKGROUND, rectangle)
    pygame.display.update()

    # Display initial text "No color selected"
    font = pygame.font.Font(None, 36)
    initial_text = font.render('No color selected', True, WHITE, BLACK)
    initial_text_rect = initial_text.get_rect(center=((WINDOW_WIDTH / 2), 300))
    SCREEN.blit(initial_text, initial_text_rect)
    pygame.display.update()

    running = True
    first_interaction = True  # Track the first user interaction

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    return
                elif event.key == pygame.K_RETURN:
                    main()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                dimension = (300, 200)
                position = (280, 200)
                rectangle = pygame.Rect(position, dimension)
                pygame.draw.rect(SCREEN, BACKGROUND, rectangle)
                pygame.display.update()
                x, y = pygame.mouse.get_pos()

                if red_circle.collidepoint((x, y)):
                    color = (255, 0, 0)
                elif green_circle.collidepoint((x, y)):
                    color = (0, 255, 0)
                elif blue_circle.collidepoint((x, y)):
                    color = (0, 0, 255)
                elif white_circle.collidepoint((x, y)):
                    color = (255, 255, 255)
                elif black_circle.collidepoint((x, y)):
                    color = (0, 0, 0)
                else:
                    if first_interaction == True:
                        font = pygame.font.Font(None, 36)
                        initial_text = font.render('No color selected', True, WHITE, BLACK)
                        initial_text_rect = initial_text.get_rect(center=((WINDOW_WIDTH / 2), 300))
                        SCREEN.blit(initial_text, initial_text_rect)
                        pygame.display.update()
                        break
                    if first_interaction == False:
                        color = player_circle_rgb

                if first_interaction:
                    red, green, blue = color  # Directly set the first color
                    first_interaction = False
                else:
                    # Change the mixing ratio here for a more gradual effect
                    red = int(red * 0.75 + color[0] * 0.25)
                    green = int(green * 0.75 + color[1] * 0.25)
                    blue = int(blue * 0.75 + color[2] * 0.25)

                player_circle_rgb = (red, green, blue)
                pygame.draw.circle(SCREEN, player_circle_rgb, (400, 300), 80)
                highscore()
                pygame.display.update()
                percent()  # Call the function to display the percentage of color accuracy
                pygame.display.update()

def play_or_exit():
    font = pygame.font.Font(None, 36)
    play_text = font.render('New Color: RETURN', True, WHITE, BLACK)
    play_text_rect = play_text.get_rect(center = ((150, 50)))
    SCREEN.blit(play_text, play_text_rect)

    escape_text = font.render('To Quit: ESC', True, WHITE, BLACK)
    escape_text_rect = escape_text.get_rect(center = ((650, 50)))
    SCREEN.blit(escape_text, escape_text_rect)

    pygame.display.update()


#Puts everything together
def main():
    play_or_exit()
    showing_random_color()
    color_setup()
    player_color()

main()