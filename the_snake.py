from random import choice, randint
import pygame
import sys

# Размеры экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20

# Количество клеток по горизонтали и вертикали
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона
BORDER_COLOR = (93, 216, 228)  # Цвет рамки
APPLE_COLOR = (255, 0, 0)  # Цвет яблока
SNAKE_COLOR = (0, 255, 0)   # Цвет змейки

# Скорость игры
SPEED = 20


class GameObject:
    def __init__(self, position):
        self.position = position

    def draw(self, screen):
        raise NotImplementedError("Этот метод должен быть переопределён \
            в подклассах.")


class Apple(GameObject):
    def __init__(self):
        super().__init__((randint(0, GRIDWIDTH - 1) * GRIDSIZE,
                          randint(0, GRIDHEIGHT - 1) * GRIDSIZE))
        self.bodycolor = APPLECOLOR

    def draw(self, screen):
        rect = pygame.Rect(self.position, (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(screen, self.bodycolor, rect)
        pygame.draw.rect(screen, BORDERCOLOR, rect, 1)


class Snake(GameObject):
    def __init__(self):
        center = (SCREENWIDTH // 2, SCREENHEIGHT // 2)
        super().__init__(center)
        self.positions = [center]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1
        self.last = None
        self.bodycolor = SNAKECOLOR

    def getheadposition(self):
        return self.positions[0]

    def move(self):
        headx, heady = self.getheadposition()
        dx, dy = self.direction
        newhead = ((headx + (dx * GRIDSIZE)) % SCREENWIDTH,
                    (heady + (dy * GRIDSIZE)) % SCREENHEIGHT)
        self.positions.insert(0, newhead)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        center = (SCREENWIDTH // 2, SCREENHEIGHT // 2)
        self.length = 1
        self.positions = [center]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def draw(self, screen):
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(screen, self.bodycolor, rect)
            pygame.draw.rect(screen, BORDERCOLOR, rect, 1)
        headrect = pygame.Rect(self.positions[0], (GRIDSIZE, GRIDSIZE))
        pygame.draw.rect(screen, self.bodycolor, headrect)
        pygame.draw.rect(screen, BORDERCOLOR, headrect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRIDSIZE, GRIDSIZE))
            pygame.draw.rect(screen, BOARDBACKGROUNDCOLOR, last_rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple()

    while True:
        screen.fill(BOARDBACKGROUNDCOLOR)
        handleinput(snake)
        snake.move()
        if snake.getheadposition() == apple.position:
            snake.length += 1
            apple = Apple()
        if snake.getheadposition() in snake.positions[1:]:
            snake.reset()
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(SPEED)


def handleinput(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.direction = RIGHT


if __name__ == '__main__':
    main()
