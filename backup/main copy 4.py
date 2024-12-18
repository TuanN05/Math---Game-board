import pygame
pygame.mixer.init()
click_sound = pygame.mixer.Sound('sounds/button01.mp3.wav')  # Load the sound
complete_sound = pygame.mixer.Sound('sounds/completetask_0.mp3')  # Load the sound
import random
import sys

def slide_transition(current_surface, next_surface, direction="left", speed=20):
    """
    Hiệu ứng chuyển màn hình với trượt ngang.
    :param current_surface: Màn hình hiện tại.
    :param next_surface: Màn hình tiếp theo.
    :param direction: Hướng trượt ("left" hoặc "right").
    :param speed: Tốc độ trượt (px mỗi khung hình).
    """
    offset = 0
    while offset < SCREEN_WIDTH:
        if direction == "left":
            screen.blit(current_surface, (-offset, 0))
            screen.blit(next_surface, (SCREEN_WIDTH - offset, 0))
        elif direction == "right":
            screen.blit(current_surface, (offset, 0))
            screen.blit(next_surface, (-SCREEN_WIDTH + offset, 0))
        
        pygame.display.flip()
        offset += speed
        clock.tick(60)

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700
CELL_SIZE = 80
GRID_PADDING = 10
FONT_SIZE = 36
HEADER_HEIGHT = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (173, 216, 230)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Math Game for Kids")

font = pygame.font.Font(None, FONT_SIZE)

is_paused = False
grid_size = 4
numbers = []
selected_cells = []
target_number = 0
score = 0
clock = pygame.time.Clock()
time_left = 60
high_score = 0
current_screen = "menu"

def draw_menu_button():
    menu_text = font.render("Menu", True, BLACK)
    menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH - 50, 50))
    pygame.draw.rect(screen, GRAY, menu_rect.inflate(20, 10))
    screen.blit(menu_text, menu_rect)

def update_grid_for_valid_pair(grid, target):
    size = len(grid)
    existing_cells = [(row, col) for row in range(size) for col in range(size) if grid[row][col] is not None]
    
    if len(existing_cells) < 2:
        return

    (row1, col1), (row2, col2) = random.sample(existing_cells, 2)
    num1 = random.randint(0, 9)
    num2 = target - num1 if random.choice([True, False]) else target + num1
    grid[row1][col1] = num1
    grid[row2][col2] = num2

def generate_grid(size):
    grid = [[random.randint(0, 9) for _ in range(size)] for _ in range(size)]
    row1, col1 = random.randint(0, size - 1), random.randint(0, size - 1)
    while True:
        row2, col2 = random.randint(0, size - 1), random.randint(0, size - 1)
        if (row1 != row2 or col1 != col2):
            break
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)
    grid[row1][col1] = num1
    grid[row2][col2] = num2
    global target_number
    target_number = random.choice([num1 + num2, abs(num1 - num2)])
    return grid

#background_image = pygame.image.load('normal.png')

def draw_grid():
    # Tải ảnh nền và thay đổi kích thước
    background_image = pygame.image.load('normal.png')
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT - HEADER_HEIGHT))  # Thay đổi kích thước ảnh nền

    screen.blit(background_image, (0, HEADER_HEIGHT))  # Vẽ ảnh nền đã được thay đổi kích thước

    # Tính toán kích thước của lưới
    total_grid_width = grid_size * (CELL_SIZE + GRID_PADDING) - GRID_PADDING
    total_grid_height = grid_size * (CELL_SIZE + GRID_PADDING) - GRID_PADDING

    # Tính toán vị trí bắt đầu để căn giữa
    start_x = (SCREEN_WIDTH - total_grid_width) // 2
    start_y = HEADER_HEIGHT + (SCREEN_HEIGHT - HEADER_HEIGHT - total_grid_height) // 2

    for row in range(grid_size):
        for col in range(grid_size):
            x = start_x + col * (CELL_SIZE + GRID_PADDING)
            y = start_y + row * (CELL_SIZE + GRID_PADDING)
            color = BLUE if (row, col) in selected_cells else WHITE
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            number = numbers[row][col]
            if number is not None:
                text = font.render(str(number), True, BLACK)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text, text_rect)

font = pygame.font.Font('arial.ttf', FONT_SIZE)

def draw_header():
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, HEADER_HEIGHT))
    
    # Tạo font mới với kích thước nhỏ hơn cho các thông tin
    small_font = pygame.font.Font('arial.ttf', FONT_SIZE - 10)  # Giảm kích thước font

    # Vẽ các thông tin khác với font nhỏ hơn
    target_text = small_font.render(f"Target: {target_number}", True, BLACK)
    screen.blit(target_text, (20, 10))  # Đặt vị trí y ở 60

    score_text = small_font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH - 250, 10))  # Đặt vị trí y ở 60

    time_text = small_font.render(f"Time Left: {int(time_left)}", True, BLACK)
    screen.blit(time_text, (SCREEN_WIDTH // 2 - 150, 10))  # Đặt vị trí y ở 60

    # Tạo font mới với kích thước nhỏ hơn cho dòng chữ hướng dẫn
    instruction_text = small_font.render(f"Hãy chọn cặp số có tổng hoặc hiệu bằng {target_number}", True, BLACK)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2-50, 70))  # Đặt vị trí y ở 100 để không bị đè
    screen.blit(instruction_text, instruction_rect)

def reset_game():
    global numbers, target_number, selected_cells, score, time_left
    numbers = generate_grid(grid_size)
    target_number = random.randint(1, 18)
    selected_cells = []
    score = 0
    time_left = 60

def has_valid_pair(grid, target):
    size = len(grid)
    for row1 in range(size):
        for col1 in range(size):
            for row2 in range(size):
                for col2 in range(size):
                    if (row1 != row2 or col1 != col2) and grid[row1][col1] is not None and grid[row2][col2] is not None:
                        num1 = grid[row1][col1]
                        num2 = grid[row2][col2]
                        if num1 + num2 == target or abs(num1 - num2) == target:
                            return True
    return False

def check_selection():
    if len(selected_cells) == 2:
        global score, numbers
        cell1 = selected_cells[0]
        cell2 = selected_cells[1]
        num1 = numbers[cell1[0]][cell1[1]]
        num2 = numbers[cell2[0]][cell2[1]]
        if num1 is not None and num2 is not None:
            if num1 + num2 == target_number or abs(num1 - num2) == target_number:
                numbers[cell1[0]][cell1[1]] = None
                numbers[cell2[0]][cell2[1]] = None
                score += 1
                complete_sound.play()
        selected_cells.clear()
        if not has_valid_pair(numbers, target_number):
            update_grid_for_valid_pair(numbers, target_number)

def handle_click(pos):
    x, y = pos
    if SCREEN_WIDTH - 70 < x < SCREEN_WIDTH - 30 and 30 < y < 70:
        global current_screen, is_paused
        print("Đã nhấn Menu")
        current_surface = screen.copy()  # Sao chép màn hình hiện tại
        next_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Tạo màn hình mới cho menu
        next_surface.fill(WHITE)  # Đặt màu nền cho màn hình mới
        draw_menu()  # Vẽ menu lên màn hình mới
        slide_menu_transition(current_surface, next_surface, direction="right", speed=30)  # Thực hiện hiệu ứng trượt
        current_screen = "menu"  # Cập nhật trạng thái màn hình hiện tại
        is_paused = False  # Đặt trạng thái tạm dừng thành False
        click_sound.play()  # Phát âm thanh khi nhấn nút
        play_menu_music()

    if y > HEADER_HEIGHT:
        # Tính toán vị trí bắt đầu của lưới
        total_grid_width = grid_size * (CELL_SIZE + GRID_PADDING) - GRID_PADDING
        start_x = (SCREEN_WIDTH - total_grid_width) // 2
        start_y = HEADER_HEIGHT + (SCREEN_HEIGHT - HEADER_HEIGHT - (grid_size * (CELL_SIZE + GRID_PADDING) - GRID_PADDING)) // 2

        # Tính toán hàng và cột dựa trên vị trí nhấn
        col = (x - start_x) // (CELL_SIZE + GRID_PADDING)
        row = (y - start_y) // (CELL_SIZE + GRID_PADDING)
        
        if 0 <= row < grid_size and 0 <= col < grid_size:
            if len(selected_cells) < 2 and (row, col) not in selected_cells:
                selected_cells.append((row, col))
                click_sound.play()

def draw_button_with_flash(surface, text, pos, is_flashing):
    button_color = GRAY if not is_flashing else RED
    button_text = font.render(text, True, BLACK)
    button_rect = button_text.get_rect(center=pos)
    pygame.draw.rect(surface, button_color, button_rect.inflate(20, 10))
    surface.blit(button_text, button_rect)

def prepare_menu_surface():
    menu_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    menu_surface.fill(WHITE)
    title_text = font.render("Math Game for Kids", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    menu_surface.blit(title_text, title_rect)
    buttons = [
        ("Play New Game", (SCREEN_WIDTH // 2, 250)),
        ("Choose Level", (SCREEN_WIDTH // 2, 350)),
        ("View High Scores", (SCREEN_WIDTH // 2, 450)),
    ]
    for text, pos in buttons:
        button_text = font.render(text, True, BLACK)
        button_rect = button_text.get_rect(center=pos)
        pygame.draw.rect(menu_surface, GRAY, button_rect.inflate(20, 10))
        menu_surface.blit(button_text, button_rect)
    return menu_surface

def set_menu_background():
    """
    Đặt hình nền cho màn hình menu.
    """
    background_image = pygame.image.load('bg_go.png')  # Thay đổi đường dẫn đến hình ảnh của bạn
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Thay đổi kích thước hình ảnh
    screen.blit(background_image, (0, 0))  # Vẽ hình nền lên màn hình

def draw_button_with_rounded_corners(surface, text, pos, is_flashing):
    button_color = GRAY if not is_flashing else RED
    button_width = 300  # Thay đổi chiều rộng nút
    button_height = 50   # Chiều cao nút
    button_rect = pygame.Rect(pos[0] - button_width // 2, pos[1] - button_height // 2, button_width, button_height)  # Kích thước nút

    # Vẽ đổ bóng
    shadow_rect = button_rect.move(5, 5)  # Di chuyển vị trí để tạo hiệu ứng đổ bóng
    pygame.draw.rect(surface, (50, 50, 50), shadow_rect, border_radius=20)  # Màu đổ bóng

    # Vẽ nút với góc bo tròn
    pygame.draw.rect(surface, button_color, button_rect, border_radius=20)  # Vẽ nút

    # Vẽ văn bản lên nút
    button_text = font.render(text, True, BLACK)
    text_rect = button_text.get_rect(center=button_rect.center)
    surface.blit(button_text, text_rect)

def draw_menu(is_flashing=None):
    
    screen.blit(prepare_menu_surface(), (0, 0))
    set_menu_background()
    buttons = [
        ("Play New Game", (SCREEN_WIDTH // 2, 250)),
        ("Choose Level", (SCREEN_WIDTH // 2, 350)),
        ("View High Scores", (SCREEN_WIDTH // 2, 450)),
    ]
    for i, (text, pos) in enumerate(buttons):
        draw_button_with_rounded_corners(screen, text, pos, is_flashing == i)  # Vẽ nút với góc bo tròn và đổ bóng
    pygame.display.flip()

def slide_menu_transition(current_surface, next_surface, direction="right", speed=20):
    """
    Hiệu ứng chuyển màn hình với trượt ngang cho menu.
    :param current_surface: Màn hình hiện tại.
    :param next_surface: Màn hình tiếp theo.
    :param direction: Hướng trượt ("left" hoặc "right").
    :param speed: Tốc độ trượt (px mỗi khung hình).
    """
    offset = 0
    while offset < SCREEN_WIDTH:
        if direction == "left":
            screen.blit(current_surface, (-offset, 0))
            screen.blit(next_surface, (SCREEN_WIDTH - offset, 0))
        elif direction == "right":
            screen.blit(current_surface, (offset, 0))
            screen.blit(next_surface, (-SCREEN_WIDTH + offset, 0))
        
        pygame.display.flip()
        offset += speed
        clock.tick(60)

def handle_menu_click(pos):
    global current_screen, grid_size
    x, y = pos
    buttons = [
        ("Play New Game", (SCREEN_WIDTH // 2, 250)),
        ("Choose Level", (SCREEN_WIDTH // 2, 350)),
        ("View High Scores", (SCREEN_WIDTH // 2, 450)),
    ]
    for i, (text, pos) in enumerate(buttons):
        if 230 + i * 100 < y < 270 + i * 100:
            click_sound.play()
            current_surface = screen.copy()
            if i == 0:
                reset_game()
                next_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                next_surface.fill(BLACK)
                draw_header()
                draw_grid()
                slide_menu_transition(current_surface, next_surface, direction="left", speed=30)
                current_screen = "game"
                play_game_music()
            elif i == 1:
                grid_size = (grid_size % 6) + 3
            elif i == 2:
                next_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                next_surface.fill(WHITE)
                draw_high_score()
                slide_menu_transition(current_surface, next_surface, direction="left", speed=30)
                current_screen = "high_score"
            break

def prepare_high_score_surface():
    high_score_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    high_score_surface.fill(WHITE)
    title_text = font.render("High Score", True, BLACK)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    high_score_surface.blit(title_text, title_rect)
    score_text = font.render(f"High Score: {high_score}", True, BLACK)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
    high_score_surface.blit(score_text, score_rect)
    back_text = font.render("Back to Menu", True, BLACK)
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
    pygame.draw.rect(high_score_surface, GRAY, back_rect.inflate(20, 10))
    high_score_surface.blit(back_text, back_rect)
    return high_score_surface

def draw_high_score():
    screen.blit(prepare_high_score_surface(), (0, 0))
    pygame.display.flip()

def handle_high_score_click(pos):
    global current_screen
    x, y = pos
    if 480 < y < 520:
        click_sound.play()
        current_surface = screen.copy()
        next_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        next_surface.fill(WHITE)
        draw_menu()
        slide_transition(current_surface, next_surface, direction="right", speed=30)
        current_screen = "menu"

def prepare_game_over_surface():
    game_over_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_over_surface.fill(WHITE)
    game_over_text = font.render("Game Over", True, BLACK)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    game_over_surface.blit(game_over_text, game_over_rect)
    final_score_text = font.render(f"Your Score: {score}", True, BLACK)
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
    game_over_surface.blit(final_score_text, final_score_rect)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
    game_over_surface.blit(high_score_text, high_score_rect)
    back_text = font.render("Back to Menu", True, BLACK)
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
    pygame.draw.rect(game_over_surface, GRAY, back_rect.inflate(20, 10))
    game_over_surface.blit(back_text, back_rect)

    play_menu_music()
    return game_over_surface

def draw_game_over():
    screen.blit(prepare_game_over_surface(), (0, 0))
    pygame.display.flip()

def prepare_win_surface():
    win_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    win_surface.fill(WHITE)
    win_text = font.render("You Win!", True, BLACK)
    win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    win_surface.blit(win_text, win_rect)
    final_score_text = font.render(f"Your Score: {score}", True, BLACK)
    final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
    win_surface.blit(final_score_text, final_score_rect)
    back_text = font.render("Back to Menu", True, BLACK)
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
    pygame.draw.rect(win_surface, GRAY, back_rect.inflate(20, 10))
    win_surface.blit(back_text, back_rect)

    play_menu_music()
    return win_surface

def draw_win_screen():
    screen.blit(prepare_win_surface(), (0, 0))
    pygame.display.flip()

def play_game_music():
    """
    Phát nhạc nền cho màn hình game.
    """
    pygame.mixer.music.load('sounds/the_field_of_dreams.mp3')  # Thay đổi đường dẫn đến file nhạc nền game của bạn
    pygame.mixer.music.play(-1)  # Phát nhạc lặp lại vô hạn

def play_menu_music():
    """
    Phát nhạc nền cho màn hình menu.
    """
    pygame.mixer.music.load('sounds/TownTheme.mp3')  # Thay đổi đường dẫn đến file nhạc nền menu của bạn
    pygame.mixer.music.play(-1)  # Phát nhạc lặp lại vô hạn

def main():
    global current_screen, high_score, score, time_left, is_paused

    running = True
    play_menu_music()
    while running:
        if current_screen == "menu":
            draw_menu()
        elif current_screen == "game":
            if is_paused:
                draw_pause_screen()
                continue
            if time_left <= 0:
                high_score = max(high_score, score)
                current_screen = "game_over"
            elif all(cell is None for row in numbers for cell in row):
                high_score = max(high_score, score)
                current_screen = "win"
            else:
                screen.fill(BLACK)
                draw_header()
                draw_menu_button()  # Draw the Menu button
                draw_grid()
                pygame.display.flip()
        elif current_screen == "high_score":
            draw_high_score()
        elif current_screen == "game_over":
            draw_game_over()
        elif current_screen == "win":
            draw_win_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_screen == "menu":
                    handle_menu_click(event.pos)
                elif current_screen == "high_score":
                    handle_high_score_click(event.pos)
                elif current_screen == "game":
                    handle_click(event.pos)
                elif current_screen == "game_over":
                    if 480 < event.pos[1] < 520:
                        current_screen = "menu"
                elif current_screen == "win":
                    if 480 < event.pos[1] < 520:
                        current_screen = "menu"

        if current_screen == "game" and not is_paused:
            check_selection()
            time_left -= clock.get_time() / 1000
        clock.tick(30)

def handle_pause_click(pos):
    x, y = pos
    if 480 < y < 520:
        global current_screen, is_paused
        current_screen = "menu"
        is_paused = False

def draw_pause_screen():
    screen.fill(WHITE)
    pause_text = font.render("Game Paused", True, BLACK)
    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(pause_text, pause_rect)

    back_text = font.render("Back to Menu", True, BLACK)
    back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, 500))
    pygame.draw.rect(screen, GRAY, back_rect.inflate(20, 10))
    screen.blit(back_text, back_rect)

    pygame.display.flip()
    
if __name__ == "__main__":
    main()
    pygame.quit()
