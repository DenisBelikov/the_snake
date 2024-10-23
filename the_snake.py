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
        raise NotImplementedError("Этот метод должен быть переопределён \
         в подклассах.")


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
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head_x + (dx * GRID_SIZE)) % SCREEN_WIDTH,
                    (head_y + (dy * GRID_SIZE)) % SCREEN_HEIGHT,)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Сброс позиции и направления змеи при столкновении с самой собой."""
        """Сбросить состояние змеи до начального."""
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [center]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def draw(self, screen):
        """Рисование змеи на экране."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Рисование головы змеи с дополнительной рамкой
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

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
        handle_input(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple = Apple()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(SPEED)


def handle_input(snake):
    """Обрабатывает нажатия клавиш для управления змеей."""
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
