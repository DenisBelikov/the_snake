"""Добавляем импорты."""
from random import choice, randint
import sys
import pygame

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
SNAKE_COLOR = (0, 255, 0)  # Цвет змейки

# Скорость игры
SPEED = 20

# Инициализация экрана Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

INITIONAL_POSITION = (0, 0)


class GameObject:
    """Базовый класс для игровых объектов с координатами и цветом тела."""

    def __init__(self, position=INITIONAL_POSITION, body_color=0):
        self.position = position
        self.body_color = body_color

    def draw(self, screen):
        """Рисует объект на экране."""
        raise NotImplementedError

    def draw_rect(self, screen, position):
        """Рисует прямоугольник (часть объекта) на экране."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position([])

    def randomize_position(self, occupied_cells):
        """Случайно устанавливает позицию яблока, избегая занятых клеток."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in occupied_cells:
                self.position = new_position
                break

    def draw(self, screen):
        """Рисует яблоко на экране."""
        self.draw_rect(screen, self.position)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(center, SNAKE_COLOR)
        self.positions = [center]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1
        self.last = None

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def move(self):
        """Двигает змейку в текущем направлении."""
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
        """Сбрасывает позицию и параметры змейки в стартовое состояние."""
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [center]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def draw(self, screen):
        """Рисует змейку на экране."""
        for position in self.positions[:-1]:
            self.draw_rect(screen, position)
        headrect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, headrect)
        pygame.draw.rect(screen, BORDER_COLOR, headrect, 1)
        # Затираем последний хвост, если змейка не увеличилась
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки, если оно не противоположное
        текущему."""
        if new_direction != tuple(-x for x in self.direction):
            self.direction = new_direction


def handle_keys(snake):
    """Обрабатывает нажатия клавиш, изменяющих направление змейки."""

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


def main():
    """Основная функция игры, запускает игровой цикл."""

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.move()
        # Проверка на съедание яблока

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        # Проверка на столкновение с самим собой

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
