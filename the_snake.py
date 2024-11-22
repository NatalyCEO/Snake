from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Base class for game objects"""

    def __init__(self):
        self.position = None,
        self.body_color = None

    def draw(self):
        """Method for drawing"""
        pass


class Apple(GameObject):
    """Generate Apple"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR,
        self.position = Apple.randomize_position()

    @staticmethod
    def randomize_position():
        """Generate a random position for an apple"""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Draw an apple on the screen"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Generate Snake"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR,
        self.position = (
            SCREEN_WIDTH // 2 - GRID_SIZE,
            SCREEN_HEIGHT // 2 - GRID_SIZE
        )
        self.last = self.position
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Update direction"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Move the snake"""
        width = self.position[0] + self.direction[0] * GRID_SIZE
        height = self.position[1] + self.direction[1] * GRID_SIZE
        self.position = (width % SCREEN_WIDTH, height % SCREEN_HEIGHT)
        self.positions.insert(0, self.position)
        if (len(self.positions) != self.length):
            self.positions.pop(-1)
            self.last = self.positions[-1]

    @property
    def get_head_position(self):
        """Get head coordinates"""
        return self.position

    def draw(self):
        """Draw a snake on the screen"""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Reset snake"""
        return Snake()


def handle_keys(game_object):
    """Get pressed key"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()


def main():
    """Main function"""
    # Инициализация PyGame:
    pygame.init()
    snake = Snake()
    apple = Apple()
    best_score = 0

    while (apple.position in snake.positions):
        apple.position = apple.randomize_position()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if (snake.get_head_position == apple.position):
            snake.length += 1
            while (apple.position in snake.positions):
                apple.position = apple.randomize_position()

        if (snake.get_head_position in snake.positions[1:]):
            if (snake.length > best_score):
                pygame.display.set_caption(
                    f'Змейка (best score: {snake.length})'
                )
                best_score = snake.length
            snake = snake.reset()

        snake.draw()
        apple.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
