import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font("PlayfairDisplay-Bold.otf", 20)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", "x, y")
BLOCK_SIZE = 20
SPEED = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)


class SnakeGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height

        # initialize display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        # initial game states
        self.direction = Direction.RIGHT
        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - 2 * BLOCK_SIZE, self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        # if food is on snake, place food again
        if self.food in self.snake:
            self._place_food()

    def _update_display(self):
        self.display.fill(BLACK)
        for point in self.snake:
            pygame.draw.rect(self.display, BLUE, (point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, SKY_BLUE, (point.x + 4, point.y + 4, 12, 12))
        pygame.draw.rect(self.display, YELLOW, (self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))  # food

        text = font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, [5, 5])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)

    def _collided(self):
        if self.head.x > self.width - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.height - BLOCK_SIZE or self.head.y < 0:
            return True
        if self.head in self.snake[1:]:
            return True
        return False

    def game_play(self):
        # collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_d:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_w:
                    self.direction = Direction.UP
                elif event.key == pygame.K_s:
                    self.direction = Direction.DOWN

        # move snake
        self._move(self.direction)
        self.snake.insert(0, self.head)

        # check for collision
        if self._collided():
            game_over = True
            return game_over, self.score

        # place new food
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # update display
        self._update_display()
        self.clock.tick(SPEED)

        # return game state
        game_over = False
        return game_over, self.score


if __name__ == "__main__":
    game = SnakeGame()

    # game loop
    while True:
        game_over, score = game.game_play()
        if game_over:
            break
    print(f"Final Score: {score}")

    pygame.quit()
