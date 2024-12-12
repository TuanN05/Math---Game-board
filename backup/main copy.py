import pygame
pygame.mixer.init()
click_sound = pygame.mixer.Sound('sounds/button01.mp3.wav')  # Load the sound
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
            # Vẽ màn hình hiện tại và tiếp theo khi trượt từ phải sang trái
            screen.blit(current_surface, (-offset, 0))
            screen.blit(next_surface, (SCREEN_WIDTH - offset, 0))
        elif direction == "right":
            # Vẽ màn hình hiện tại và tiếp theo khi trượt từ trái sang phải
            screen.blit(current_surface, (offset, 0))
            screen.blit(next_surface, (-SCREEN_WIDTH + offset, 0))
        
        pygame.display.flip()
        offset += speed
        clock.tick(60)

# Khởi tạo pygame
pygame.init()

# Thiết lập màn hình và các thông số
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 700
CELL_SIZE = 80
GRID_PADDING = 10
FONT_SIZE = 36
HEADER_HEIGHT = 100

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (173, 216, 230)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Tạo màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Math Game for Kids")

# Khởi tạo font
font = pygame.font.Font(None, FONT_SIZE)

# Các biến toàn cục
is_paused = False  # Trạng thái tạm dừng
grid_size = 4  # Kích thước bảng mặc định
numbers = []
selected_cells = []
target_number = 0
score = 0
clock = pygame.time.Clock()
time_left = 60
high_score = 0  # Điểm cao nhất
current_screen = "menu"  # Màn hình hiện tại: menu / game / high_score

def draw_pause_button():
    pause_text = font.render("Pause", True, BLACK)
    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH - 50, 50))
    pygame.draw.rect(screen, GRAY, pause_rect.inflate(20, 10))
    screen.blit(pause_text, pause_rect)

def update_grid_for_valid_pair(grid, target):
    """
    Cập nhật số trong bảng chỉ trên các ô còn tồn tại (không bị xóa),
    để đảm bảo có ít nhất một cặp đáp án đúng.
    """
    size = len(grid)
    existing_cells = [(row, col) for row in range(size) for col in range(size) if grid[row][col] is not None]
    
    if len(existing_cells) < 2:
        return  # Nếu không đủ ô tồn tại để tạo cặp, thoát

    # Chọn ngẫu nhiên 2 ô trong danh sách các ô còn tồn tại
    (row1, col1), (row2, col2) = random.sample(existing_cells, 2)

    # Tạo cặp số hợp lệ
    num1 = random.randint(0, 9)
    num2 = target - num1 if random.choice([True, False]) else target + num1

    # Cập nhật lại số trong bảng
    grid[row1][col1] = num1
    grid[row2][col2] = num2

def generate_grid(size):
    """Sinh bảng n x n với số ngẫu nhiên từ 0-9, đảm bảo ít nhất một cặp hợp lệ"""
    grid = [[random.randint(0, 9) for _ in range(size)] for _ in range(size)]

    # Đảm bảo có ít nhất một cặp số hợp lệ
    row1, col1 = random.randint(0, size - 1), random.randint(0, size - 1)
    while True:
        row2, col2 = random.randint(0, size - 1), random.randint(0, size - 1)
        if (row1 != row2 or col1 != col2):  # Không trùng ô
            break

    # Tạo số mục tiêu dựa trên cặp số hợp lệ
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)
    grid[row1][col1] = num1
    grid[row2][col2] = num2

    global target_number
    target_number = random.choice([num1 + num2, abs(num1 - num2)])

    return grid

background_image = pygame.image.load('normal.png')

def draw_grid():
    screen.blit(background_image, (0, HEADER_HEIGHT))  # Vẽ hình nền từ vị trí (0, HEADER_HEIGHT)

    """Vẽ bảng và các ô vuông"""
    for row in range(grid_size):
        for col in range(grid_size):
            x = GRID_PADDING + col * (CELL_SIZE + GRID_PADDING)
            y = HEADER_HEIGHT + GRID_PADDING + row * (CELL_SIZE + GRID_PADDING)

            color = BLUE if (row, col) in selected_cells else WHITE

            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            number = numbers[row][col]
            if number is not None:
                text = font.render(str(number), True, BLACK)
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text, text_rect)

def draw_header():
    """Hiển thị số mục tiêu, điểm số và thời gian còn lại"""
    pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, HEADER_HEIGHT))

    # Hiển thị số mục tiêu
    target_text = font.render(f"Target: {target_number}", True, BLACK)
    screen.blit(target_text, (20, 20))

    # Hiển thị điểm số
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH - 200, 20))

    # Hiển thị thời gian còn lại
    time_text = font.render(f"Time Left: {int(time_left)}", True, BLACK)
    screen.blit(time_text, (SCREEN_WIDTH // 2 - 50, 20))  # Vị trí có thể điều chỉnh

def reset_game():
    """Khởi tạo lại trạng thái trò chơi"""
    global numbers, target_number, selected_cells, score, time_left
    numbers = generate_grid(grid_size)
    target_number = random.randint(1, 18)
    selected_cells = []
    score = 0
    time_left = 60

def has_valid_pair(grid, target):
    """Kiểm tra xem có cặp nào hợp lệ trong bảng hay không"""
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
    """Kiểm tra nếu 2 ô đã chọn hợp lệ"""
    if len(selected_cells) == 2:
        global score, numbers
        cell1 = selected_cells[0]
        cell2 = selected_cells[1]

        num1 = numbers[cell1[0]][cell1[1]]
        num2 = numbers[cell2[0]][cell2[1]]

        if num1 is not None and num2 is not None:
            if num1 + num2 == target_number or abs(num1 - num2) == target_number:
                # Xóa ô nếu đúng
                numbers[cell1[0]][cell1[1]] = None
                numbers[cell2[0]][cell2[1]] = None
                score += 1

        # Reset lựa chọn
        selected_cells.clear()

        # Kiểm tra và cập nhật lại bảng nếu không có cặp hợp lệ
        if not has_valid_pair(numbers, target_number):
            update_grid_for_valid_pair(numbers, target_number)

def handle_click(pos):
    """Xử lý khi người chơi click vào ô"""
    x, y = pos

    #print(f"Clicked at: ({x}, {y})")  # In ra tọa độ nhấp chuột

    if SCREEN_WIDTH - 70 < x < SCREEN_WIDTH - 30 and 30 < y < 70:  # Kiểm tra vị trí nút Pause
        global is_paused
        print("da nhap pause")
        is_paused = not is_paused  # Chuyển đổi trạng thái tạm dừng
        click_sound.play()  # Phát âm thanh khi nhấn nút Pause

    if y > HEADER_HEIGHT:  # Chỉ xử lý dưới header
        col = (x - GRID_PADDING) // (CELL_SIZE + GRID_PADDING)
        row = (y - HEADER_HEIGHT - GRID_PADDING) // (CELL_SIZE + GRID_PADDING)

        if 0 <= row < grid_size and 0 <= col < grid_size:
            if len(selected_cells) < 2 and (row, col) not in selected_cells:
                selected_cells.append((row, col))
                click_sound.play()  # Phát âm thanh khi chọn ô
        

def draw_button_with_flash(surface, text, pos, is_flashing):
    """Vẽ nút với hiệu ứng nhấp nháy."""
    button_color = GRAY if not is_flashing else RED  # Đổi màu khi nhấp nháy
    button_text = font.render(text, True, BLACK)
    button_rect = button_text.get_rect(center=pos)
    pygame.draw.rect(surface, button_color, button_rect.inflate(20, 10))
    surface.blit(button_text, button_rect)

def prepare_menu_surface():
    """Chuẩn bị surface cho màn hình menu"""
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

def draw_menu(is_flashing=None):
    """Vẽ màn hình menu chính"""
    screen.blit(prepare_menu_surface(), (0, 0))
    
    buttons = [
        ("Play New Game", (SCREEN_WIDTH // 2, 250)),
        ("Choose Level", (SCREEN_WIDTH // 2, 350)),
        ("View High Scores", (SCREEN_WIDTH // 2, 450)),
    ]

    for i, (text, pos) in enumerate(buttons):
        draw_button_with_flash(screen, text, pos, is_flashing == i)

    pygame.display.flip()

def handle_menu_click(pos):
    """Xử lý click trên màn hình menu"""
    global current_screen, grid_size
    x, y = pos

    buttons = [
        ("Play New Game", (SCREEN_WIDTH // 2, 250)),
        ("Choose Level", (SCREEN_WIDTH // 2, 350)),
        ("View High Scores", (SCREEN_WIDTH // 2, 450)),
    ]

    for i, (text, pos) in enumerate(buttons):
        if 230 + i * 100 < y < 270 + i * 100:  # Kiểm tra vị trí nhấp chuột
            click_sound.play()  # Play the sound when the button is clicked
            draw_menu(is_flashing=i)  # Gọi hàm vẽ với hiệu ứng nhấp nháy
            pygame.time.delay(100)  # Thời gian nhấp nháy
            draw_menu()  # Vẽ lại menu

            if i == 0:
                current_surface = screen.copy()  # Lưu màn hình hiện tại
                reset_game()
                next_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                next_surface.fill(BLACK)
                draw_header()
                draw_grid()
                slide_transition(current_surface, next_surface, direction="left", speed=30)
                current_screen = "game"
            elif i == 1:
                grid_size = (grid_size % 6) + 3  # Chuyển cấp độ giữa 3x3 -> 6x6
            elif i == 2:
                current_surface = screen.copy()  # Lưu màn hình hiện tại
                next_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                next_surface.fill(WHITE)
                draw_high_score()
                slide_transition(current_surface, next_surface, direction="left", speed=30)
                current_screen = "high_score"
            break

def prepare_high_score_surface():
    """Chuẩn bị surface cho màn hình điểm cao nhất"""
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
    """Vẽ màn hình điểm cao nhất"""
    screen.blit(prepare_high_score_surface(), (0, 0))
    pygame.display.flip()

def handle_high_score_click(pos):
    """Xử lý click trên màn hình điểm cao"""
    global current_screen
    x, y = pos
    if 480 < y < 520:
        current_surface = screen.copy()  # Lưu màn hình hiện tại
        next_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        next_surface.fill(WHITE)
        draw_menu()
        slide_transition(current_surface, next_surface, direction="right", speed=30)
        current_screen = "menu"

def prepare_game_over_surface():
    """Chuẩn bị surface cho màn hình kết thúc"""
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

    return game_over_surface

def draw_game_over():
    """Vẽ màn hình kết thúc"""
    screen.blit(prepare_game_over_surface(), (0, 0))
    pygame.display.flip()

def prepare_win_surface():
    """Chuẩn bị surface cho màn hình chiến thắng"""
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

    return win_surface

def draw_win_screen():
    """Vẽ màn hình chiến thắng"""
    screen.blit(prepare_win_surface(), (0, 0))
    pygame.display.flip()

def main():
    """Hàm chính để chạy game"""
    global current_screen, high_score, score, time_left, is_paused

    running = True
    while running:
        if current_screen == "menu":
            draw_menu()  # Ensure draw_menu is called without is_flashing
        elif current_screen == "game":
            if is_paused:
                draw_pause_screen()
                continue  # Dừng cập nhật trò chơi khi tạm dừng
            if time_left <= 0:
                high_score = max(high_score, score)
                current_screen = "game_over"  # Chuyển sang màn hình kết thúc
            elif all(cell is None for row in numbers for cell in row):
                high_score = max(high_score, score)
                current_screen = "win"  # Chuyển sang màn hình chiến thắng
            else:
                screen.fill(BLACK)
                draw_header()
                draw_pause_button()
                draw_grid()
                pygame.display.flip()
        elif current_screen == "high_score":
            draw_high_score()
        elif current_screen == "game_over":
            draw_game_over()
        elif current_screen == "win":  # Thêm điều kiện cho màn hình chiến thắng
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
                elif current_screen == "win":  # Xử lý click trên màn hình chiến thắng
                    if 480 < event.pos[1] < 520:
                        current_screen = "menu"
                elif is_paused:
                    handle_pause_click(event.pos)
                    # if 480 < event.pos[1] < 520:
                    #     current_screen = "menu"
                    #     is_paused = False

        if current_screen == "game" and not is_paused:
            check_selection()
            time_left -= clock.get_time() / 1000
        clock.tick(30)

def handle_pause_click(pos):
    """Xử lý click trên màn hình tạm dừng"""
    x, y = pos
    # Kiểm tra vị trí nhấp chuột cho nút "Back to Menu"
    if 480 < y < 520:  # Giả sử nút "Back to Menu" nằm trong khoảng này
        global current_screen, is_paused
        current_screen = "menu"  # Chuyển về màn hình menu
        is_paused = False  # Đặt lại trạng thái tạm dừng

def draw_pause_screen():
    """Vẽ màn hình tạm dừng"""
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
