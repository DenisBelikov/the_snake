import pygame
import sys
import random

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
    """Базовый класс для игровых объектов."""
    def __init__(self, position):
        """Инициализация позиции объекта."""
        self.position = position

    def draw(self, surface):
        """Рисование объекта на экране."""
        pass NotImplementedError ("Этот метод должен быть переопределён 
                                    в подклассах.")


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        """Инициализация, установка случайной позиции для яблока."""
        super().__init__((0, 0))
        self.bodycolor = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Рисование яблока на экране."""
        r = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.bodycolor, r)


class Snake(GameObject):
    """Класс для змеи."""
    def __init__(self):
        """Инициализация змейки в центре экрана."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.nextdirection = None
        self.bodycolor = SNAKE_COLOR

    def get_head_position(self):
        """Получить позицию головы змеи."""
        return self.positions[0]

    def move(self):
        """Переместить змею в текущем направлении."""
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH)
        (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)

        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()

        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        """Сброс позиции и направления змеи при столкновении с самой собой."""
        """Сбросить состояние змеи до начального."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT

    def draw(self, surface):
        """Рисование змеи на экране."""
        for p in self.positions:
            r = pygame.Rect(p, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, r)

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction

def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змеей."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT

def main():
    """Главная функция игры."""
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    apple = Apple()
    snake = Snake()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(SPEED)

if __name__ == "__main__":
    main()
