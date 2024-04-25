import sys
import json
import random
import pygame
from os import path

# Color definitions
GREEN = (0, 180, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

# Window dimensions
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600

# Setup display
pygame.init()
pygame.font.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')

# Score handling
filename = 'high_scores.json'

# Load existing high scores or initialize if none exist
def load_scores():
    if path.exists(filename):
        with open(filename, "r") as json_file:
            return json.load(json_file)
    else:
        return [0]  # Return a list with zero as initial high score if no file exists

score_list = [0]

score_list = load_scores()

def append_score(new_score):
    if new_score > max(score_list):
        score_list.append(new_score)
        with open(filename, "w") as json_file:
            json.dump(score_list, json_file, indent=4)

def random_coordinates():
    y_cord = random.randint(50, WINDOW_HEIGHT-30)
    x_cord = random.randint(50, WINDOW_WIDTH-30)
    return x_cord, y_cord

class Apple:
    def __init__(self):
        self.xpos, self.ypos = random_coordinates()
        self.rect = pygame.Rect(self.xpos, self.ypos, 15, 15)

    def draw(self):
        pygame.draw.rect(SCREEN, RED, self.rect)

class Snake:
    def __init__(self, xpos, ypos):
        self.body = [pygame.Rect(xpos, ypos, 15, 15)]

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(SCREEN, WHITE, segment)

    def move(self, direction):
        new_head = self.body[0].copy()
        if direction == "up":
            new_head.y -= 15
        elif direction == "down":
            new_head.y += 15
        elif direction == "left":
            new_head.x -= 15
        elif direction == "right":
            new_head.x += 15

        if new_head.left < 0 or new_head.right > WINDOW_WIDTH or new_head.top < 0 or new_head.bottom > WINDOW_HEIGHT or new_head.collidelist(self.body[1:]) != -1:
            return False

        self.body.insert(0, new_head)
        self.body.pop()
        return True

def final_screen():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    direction = None
                    run = False

        SCREEN.fill(RED)
        font = pygame.font.Font(None, 36)
        msg = font.render("YOU LOST!", True, WHITE, BLACK)
        msg_rect = msg.get_rect(center=(WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2 - 90 )))
        again = font.render('Press RETURN to play again.', True, WHITE, BLACK)
        again_rect = again.get_rect(center = (WINDOW_WIDTH/2, (WINDOW_HEIGHT / 2 + 0)))
        esc = font.render('Press ESC to close the game.', True, WHITE, BLACK)
        esc_rect = esc.get_rect(center = (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2 + 90)))
        SCREEN.blit(msg, msg_rect)
        SCREEN.blit(again, again_rect)
        SCREEN.blit(esc, esc_rect)

        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    direction = None
    snake = Snake(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    apple = Apple()


    #handles both score and highscore:
    font = pygame.font.Font('freesansbold.ttf', 25)
    score = 0
    highscore = max(score_list)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and direction != "down":
                    direction = "up"
                elif (event.key == pygame.K_s or event.key == pygame.K_DOWN) and direction != "up":
                    direction = "down"
                elif (event.key == pygame.K_a or event.key == pygame.K_LEFT) and direction != "right":
                    direction = "left"
                elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and direction != "left":
                    direction = "right"

        if not snake.move(direction):
            if score > highscore:
                append_score(score)  # Update high score if current score is greater
                highscore = score  # Update highscore variable to reflect new high score
            final_screen()  # Call the final screen if there's a collision
            snake = Snake(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)  # Reset snake
            score = 0  # Reset score
            direction = None  # Reset direction

        SCREEN.fill(BLACK)
        snake.draw()
        apple.draw()

        if snake.body[0].colliderect(apple.rect):
            snake.body.append(snake.body[-1].copy())
            score += 1
            apple = Apple()

        score_text = font.render('Score: ' + str(score), True, WHITE, BLACK)
        highscore_text = font.render('Highscore: ' + str(highscore), True, WHITE, BLACK)
        score_text_rect = score_text.get_rect(center=((WINDOW_WIDTH/2) + 80, 30))
        highscore_text_rect = highscore_text.get_rect(center=((WINDOW_WIDTH/2) - 80, 30))
        SCREEN.blit(score_text, score_text_rect)
        SCREEN.blit(highscore_text, highscore_text_rect)

        pygame.display.update()
        clock.tick(30)

main()