from random import choice, randint
import sys
import pygame

# Константы для параметров экрана и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Константы направленного движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Сопоставление клавиш с направлениями
DIRECTION_MAP = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
}

# Определения цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
OBSTACLE_COLOR = (255, 255, 255)

# Скорость игры и начальные настройки
SPEED = 10
APPLE_SCORE_INCREMENT = 10
SPEED_INCREASE_RATE = 1.05
OBSTACLE_START_COUNT = 3

# Настройка экрана Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
INITIONAL_POSITION = (0, 0)


class GameObject:
    """
    Базовый класс для всех игровых объектов, таких как Apple,
    Snake и Obstacles.
    """

    def __init__(self, position=INITIONAL_POSITION,
                 body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        raise NotImplementedError

    def draw_rect(self, position):
        """Нарисуйте прямоугольник для игрового объекта."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс объекта яблока в игре.."""

    def __init__(self):
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position([])

    def randomize_position(self, occupied_cells):
        """Поместите яблоко в случайное место, избегая занятых ячеек."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in occupied_cells:
                self.position = new_position
                break

    def draw(self):
        """Нарисуйте яблоко на экране."""
        self.draw_rect(self.position)


class Obstacle(GameObject):
    """Класс препятствий для добавления новых барьеров в игру."""

    def __init__(self, position):
        super().__init__(position, OBSTACLE_COLOR)

    def draw(self):
        """Нарисуйте препятствие на экране."""
        self.draw_rect(self.position)


class Snake(GameObject):
    """Класс Snake для объекта-змеи, управляемого игроком."""
    def __init__(self):
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(center, SNAKE_COLOR)
        self.positions = [center]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1
        self.last = None

    def get_head_position(self):
        """Возвращает текущее положение головы змеи."""
        return self.positions[0]

    def move(self):
        """Перемещайте змею в зависимости от ее направления."""
        headx, heady = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (headx + (dx * GRID_SIZE)) % SCREEN_WIDTH,
            (heady + (dy * GRID_SIZE)) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Верните змейку в исходное состояние."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [center]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def draw(self):
        """Нарисуйте змею на экране."""
        for position in self.positions:
            self.draw_rect(position)
        if self.last:
            lastrect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, lastrect)

    def update_direction(self, new_direction):
        """Обновите направление змеи."""
        if new_direction != tuple(-x for x in self.direction):
            self.direction = new_direction


def handle_keys(snake):
    """Обработка событий клавиатуры для управления змеей."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            new_direction = DIRECTION_MAP.get(event.key, snake.direction)
            snake.update_direction(new_direction)


def generate_obstacles(count, occupied_cells):
    """Создать список препятствий в случайных позициях."""
    obstacles = []
    for _ in range(count):
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if position not in occupied_cells:
                obstacles.append(Obstacle(position))
                occupied_cells.append(position)
                break
    return obstacles

def update_score(score, record):
    """Обновите счет и запишите его, если необходимо.."""
    score += APPLE_SCORE_INCREMENT
    if score > record:
        return score, score
    return score, record


def main():
    """Основная функция для запуска игрового цикла."""
    snake = Snake()
    apple = Apple()
    obstacles = generate_obstacles(OBSTACLE_START_COUNT, snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)
    score = 0
    record = 0
    speed = SPEED
    apple_eaten = 0

    while True:
        clock.tick(speed)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions +
            [o.position for o in obstacles])
            score, record = update_score(score, record)
            apple_eaten += 1
            speed *= SPEED_INCREASE_RATE

            if apple_eaten == 3:
                apple_eaten = 0
                obstacles += generate_obstacles(1, snake.positions +
                [o.position for o in obstacles])

        elif snake.get_head_position() in snake.positions[1:] or \
            snake.get_head_position() in [o.position for o in obstacles]:
            snake.reset()
            score = 0
            speed = SPEED
            apple_eaten = 0
            obstacles = generate_obstacles(OBSTACLE_START_COUNT,
            snake.positions)

        # Обновить экран
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        for obstacle in obstacles:
            obstacle.draw()

        # Показать оценку
        pygame.display.set_caption(f'Snake Game - Score: {score},
        Record: {record}')
        pygame.display.update()


if __name__ == '__main__':
    main()
