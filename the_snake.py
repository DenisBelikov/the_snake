"""Добавляем импорты."""
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
    """Базовый класс для игровых объектов."""

    def __init__(self, position):
        """Инициализация позиции объекта."""
        self.position = position

    def draw(self, screen):
        """Рисование объекта на экране."""
        raise NotImplementedError("Этот метод должен быть \
                            переопределён в подклассах.")


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        """Инициализация, установка случайной позиции для яблока."""
        super().__init__((randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                          randint(0, GRID_HEIGHT - 1) * GRID_SIZE))
        self.body_color = APPLE_COLOR

    def draw(self, screen):
        """Рисование яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Рандомизирует положение объекта на сетке."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


class Snake(GameObject):
    """Класс для змеи."""

    def __init__(self):
        """Инициализация змейки в центре экрана."""
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(center)
        self.positions = [center]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1
        self.last = None
        self.body_color = SNAKE_COLOR

    def get_head_position(self):
        """Получить позицию головы змеи."""
        return self.positions[0]

    def move(self):
        """Переместить змею в текущем направлении."""
        headx, heady = self.get_head_position()
        dx, dy = self.direction
        new_head = ((headx + (dx * GRID_SIZE)) % SCREEN_WIDTH,
                    (heady + (dy * GRID_SIZE)) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

        else:
            self.last = None

    def reset(self):
        """Эта функция выполняет сброс позиции и направления змеи, 
        устанавливая её в начальное состояние,
        каждый раз, когда змея сталкивается с самой собой."""
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [center]
        self.direction = choice([UP, DOWN, LEFT, RIGHT]) 
        """Кнопки управления."""
        self.last = None

    def draw(self, screen):
        """Рисование яблока на экране."""
        for position in self.positions[:-1]:
            # Определяем область прямоугольника для текущего сегмента змеи.
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
            # Рисование головы змеи с дополнительной рамкой
        headrect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, headrect)
        pygame.draw.rect(screen, BORDER_COLOR, headrect, 1)
        """Если у змеи есть последнее оставленное положение,
        очищаем его, закрашивая фоновым цветом."""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self, new_direction):
        if new_direction != tuple(-x for x in self.direction):
            self.direction = new_direction


def main():
    """Главная функция игры."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()
    snake = Snake()
    apple = Apple()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(SPEED)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления змеей."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)

            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)

            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)

            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


if __name__ == '__main__':
    main()
