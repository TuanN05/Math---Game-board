from tkinter import Tk, Label, Button, filedialog, Canvas, Entry
from PIL import Image, ImageTk

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixelate Image")

        # Khởi tạo biến toàn cục
        self.original_image = None
        self.pixelated_image = None
        self.image_on_canvas = None
        self.canvas_offset_x = 0
        self.canvas_offset_y = 0

        # Canvas hiển thị hình ảnh
        self.canvas_original = Canvas(root, width=600, height=450, bg="white")
        self.canvas_original.grid(row=0, column=0, padx=10, pady=10)

        self.canvas_pixelated = Canvas(root, width=600, height=450, bg="white")
        self.canvas_pixelated.grid(row=0, column=1, padx=10, pady=10)

        # Các nút chức năng
        btn_open = Button(root, text="Open Image", command=self.open_image)
        btn_open.grid(row=1, column=0, pady=10)

        Label(root, text="Block Size:").grid(row=2, column=0, sticky="e")
        self.block_size_entry = Entry(root)
        self.block_size_entry.insert(0, "10")  # Giá trị mặc định
        self.block_size_entry.grid(row=2, column=1, padx=5)

        btn_pixelate = Button(root, text="Pixelate Image", command=self.pixelate_image)
        btn_pixelate.grid(row=1, column=1, pady=10)

        # Thêm sự kiện cho canvas
        self.canvas_original.bind("<ButtonPress-1>", self.start_move)
        self.canvas_original.bind("<B1-Motion>", self.move_image)
        self.canvas_original.bind("<MouseWheel>", self.zoom_image)

        # Khởi tạo biến cho việc di chuyển
        self.start_x = None
        self.start_y = None

    def open_image(self):
        """Mở tệp hình ảnh."""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image, self.canvas_original)

    def pixelate_image(self):
        """Pixel hóa hình ảnh."""
        if self.original_image:
            block_size = int(self.block_size_entry.get()) if self.block_size_entry.get().isdigit() else 10
            self.pixelated_image = self.original_image.resize(
                (self.original_image.width // block_size, self.original_image.height // block_size),
                Image.NEAREST
            )
            self.pixelated_image = self.pixelated_image.resize(
                (self.original_image.width, self.original_image.height),
                Image.NEAREST
            )
            self.display_image(self.pixelated_image, self.canvas_pixelated)

    def display_image(self, image, canvas):
        """Hiển thị hình ảnh lên canvas."""
        image_tk = ImageTk.PhotoImage(image)
        canvas.image = image_tk  # Lưu tham chiếu để không bị xóa
        canvas.create_image(self.canvas_offset_x, self.canvas_offset_y, anchor="nw", image=image_tk)
        self.image_on_canvas = image_tk  # Lưu hình ảnh để không bị xóa

    def start_move(self, event):
        """Bắt đầu di chuyển hình ảnh."""
        self.start_x = event.x
        self.start_y = event.y

    def move_image(self, event):
        """Di chuyển hình ảnh."""
        if self.image_on_canvas:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.canvas_offset_x += dx
            self.canvas_offset_y += dy
            self.canvas_original.move(self.image_on_canvas, dx, dy)
            self.start_x = event.x
            self.start_y = event.y

    def zoom_image(self, event):
        """Phóng to hoặc thu nhỏ hình ảnh."""
        scale_factor = 1.1 if event.delta > 0 else 0.9
        if self.original_image:
            new_width = int(self.original_image.width * scale_factor)
            new_height = int(self.original_image.height * scale_factor)
            self.original_image = self.original_image.resize((new_width, new_height), Image.ANTIALIAS)
            self.display_image(self.original_image, self.canvas_original)

# Khởi tạo ứng dụng
root = Tk()
app = ImageApp(root)

# Chạy ứng dụng
root.mainloop