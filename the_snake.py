"""Добавляем импорты."""
from random import choice, randint

import sys

import pygame

pygame.init()

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

# Карта клавиш для управления направлением
DIRECTION_MAP = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
}

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона
BORDER_COLOR = (93, 216, 228)  # Цвет рамки
APPLE_COLOR = (255, 0, 0)  # Цвет яблока
SNAKE_COLOR = (0, 255, 0)  # Цвет змейки

# Скорость игры
SPEED = 20

# Инициализация экрана Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Snake Game')

# Настройка времени:
clock = pygame.time.Clock()

INITIONAL_POSITION = (0, 0)


class GameObject:
    """Базовый класс игрового объекта"""

    def __init__(self, position=INITIONAL_POSITION,
                 body_color=BOARD_BACKGROUND_COLOR):
        """Инициализация игрового объекта с позицией и цветом тела"""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Отрисовка игрового объекта на экране - должен быть переопределен в
        дочерних классах
        """
        raise NotImplementedError

    def draw_rect(self, position):
        """Отрисовка прямоугольника для объекта на указанной позиции"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для представления яблока на игровом поле"""

    def __init__(self, snake, color=APPLE_COLOR):
        """Инициализация яблока и установка его в случайную позицию"""
        super().__init__(body_color=color)
        self.randomize_position(snake.positions)

    def randomize_position(self, occupied_cells):
        """Установка позиции яблока вне занятых клеток"""
        while True:
            # Генерация новой случайной позиции
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in occupied_cells:
                # Проверка что данная позиция не занята
                self.position = new_position
                break

    def draw(self):
        """Отрисовка яблока на экране"""
        self.draw_rect(self.position)


class Snake(GameObject):
    """Класс для представления змейки"""

    def __init__(self, position=None, color=SNAKE_COLOR):
        """Инициализация змейки в центре поля"""
        if position is None:
            position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(position, color)
        self.positions = [position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1
        self.last = None

    def get_head_position(self):
        """Получить текущую позицию головы змейки"""
        return self.positions[0]

    def move(self):
        """Перемещение змейки в текущем направлении"""
        headx, heady = self.get_head_position()
        dx, dy = self.direction

        # Обновление позиции головы по модулю чтобы зацикливать экран
        new_head = (
            (headx + (dx * GRID_SIZE)) % SCREEN_WIDTH,
            (heady + (dy * GRID_SIZE)) % SCREEN_HEIGHT
        )

        # Добавление новой позиции головы
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Сброс змейки в изначальное состояние в центре поля"""
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [center]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def draw(self):
        """Отрисовка змейки на экране"""
        # Рисование всех частей тела
        for position in self.positions:
            self.draw_rect(position)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self, new_direction):
        """
        Обновление направления движения змейки если оно
        не противоположное текущему
        """
        # Не позволяем змейке двигаться в противоположном направлении
        if new_direction != tuple(-x for x in self.direction):
            self.direction = new_direction


def handle_keys(snake):
    """Обработка нажатий клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Меняем направление змейки в зависимости от нажатой клавиши
            new_direction = DIRECTION_MAP.get(event.key, snake.direction)
            snake.update_direction(new_direction)


def main():
    """Основная функция игры, запускает игровой цикл."""
    snake = Snake()
    apple = Apple(snake)
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        # Контроль скорости игры
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверка столкновения с самим собой
        elif snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()

        # Отрисовка змейки и яблока
        snake.draw()
        apple.draw()

        # Обновление экрана
        pygame.display.update()


if __name__ == '__main__':
    main()
