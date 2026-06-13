import pygame
import random

# 初期設定
pygame.init()
width, height = 300, 600
cell_size = 30
grid_width = width // cell_size
grid_height = height // cell_size
colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# ウィンドウの作成
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris")

# フォントの設定
font = pygame.font.SysFont(None, 36)

# テトリミノの定義
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 1, 1], [0, 1, 0]]
]

class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.randint(1, len(colors) - 1)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def draw_grid():
    for x in range(grid_width):
        for y in range(grid_height):
            pygame.draw.rect(screen, (200, 200, 200), (x * cell_size, y * cell_size, cell_size, cell_size), 1)

def draw_tetromino(tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, colors[tetromino.color], ((tetromino.x + x) * cell_size, (tetromino.y + y) * cell_size, cell_size, cell_size))

def check_collision(tetromino, grid):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                nx, ny = tetromino.x + x, tetromino.y + y
                if nx < 0 or nx >= grid_width or ny >= grid_height or (ny < grid_height and grid[ny][nx]):
                    return True
    return False

def merge_tetromino(tetromino, grid):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                grid[tetromino.y + y][tetromino.x + x] = tetromino.color

def clear_lines(grid):
    lines_cleared = 0
    new_grid = [[0] * grid_width for _ in range(grid_height)]
    line_index = grid_height - 1
    for row in reversed(grid):
        if all(cell != 0 for cell in row):
            lines_cleared += 1
        else:
            new_grid[line_index] = row
            line_index -= 1
    return new_grid, lines_cleared

def main():
    clock = pygame.time.Clock()
    grid = [[0] * grid_width for _ in range(grid_height)]
    tetromino = Tetromino(grid_width // 2 - 2, 0, random.choice(shapes))
    game_over = False
    score = 0
    drop_time = 0
    drop_speed = 500

    while not game_over:
        screen.fill((0, 0, 0))
        draw_grid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(tetromino, grid):
                    tetromino.move(-1, 0)
                elif event.key == pygame.K_RIGHT and not check_collision(tetromino, grid):
                    tetromino.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    if not check_collision(tetromino, grid):
                        tetromino.move(0, 1)
                elif event.key == pygame.K_UP:
                    rotated_tetromino = Tetromino(tetromino.x, tetromino.y, [list(row) for row in zip(*tetromino.shape[::-1])])
                    if not check_collision(rotated_tetromino, grid):
                        tetromino = rotated_tetromino

        drop_time += clock.get_rawtime()
        clock.tick()

        if drop_time > drop_speed:
            drop_time = 0
            if not check_collision(tetromino, grid):
                tetromino.move(0, 1)
            else:
                merge_tetromino(tetromino, grid)
                grid, lines_cleared = clear_lines(grid)
                score += lines_cleared * 10
                tetromino = Tetromino(grid_width // 2 - 2, 0, random.choice(shapes))
                if check_collision(tetromino, grid):
                    game_over = True

        draw_tetromino(tetromino)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
