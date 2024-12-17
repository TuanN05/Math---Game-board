import pygame

# Khởi tạo Pygame
pygame.init()

# Kích thước của mỗi khung hình
frame_width = 32
frame_height = 32

# Tải sprite sheet cho hoạt ảnh
sprite_sheet = pygame.image.load("images/charge.png")

# Tải hình nền
background_image = pygame.image.load("images/normal.png")

# Hàm để hiển thị khung hình
def draw_frame(surface, sprite_sheet, frame_index, x, y):
    frame_x = frame_index * frame_width
    frame_y = 0  # Vì sprite sheet chỉ có một hàng
    frame = sprite_sheet.subsurface((frame_x, frame_y, frame_width, frame_height))
    surface.blit(frame, (x, y))

# Hàm để hiển thị hoạt ảnh tại vị trí cụ thể
def show_animation(surface, sprite_sheet, position, duration, frame_count):
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    current_frame_index = 0

    while pygame.time.get_ticks() - start_time < duration:
        # Vẽ hình nền
        surface.blit(background_image, (0, 0))  # Vẽ hình nền ở góc trên bên trái

        # Vẽ khung hình hoạt ảnh
        draw_frame(surface, sprite_sheet, current_frame_index, position[0], position[1])

        # Cập nhật chỉ số khung hình
        current_frame_index = (current_frame_index + 1) % frame_count

        # Cập nhật màn hình
        pygame.display.flip()

        # Giới hạn tốc độ khung hình
        clock.tick(10)  # 10 khung hình mỗi giây

# Ví dụ sử dụng
screen = pygame.display.set_mode((800, 600))
running = True

# Vòng lặp chính
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Hiển thị hoạt ảnh tại vị trí (100, 100) trong 1 giây với 8 khung hình
    show_animation(screen, sprite_sheet, (100, 100), 1000, sprite_sheet.get_width() // frame_width)

    # Cập nhật màn hình
    pygame.display.flip()

# Thoát Pygame
pygame.quit()