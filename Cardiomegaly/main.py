import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)

        self.image = None
        self.image_tk = None

        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Edit", command=self.open_image)
        menubar.add_cascade(label="Files", menu=file_menu)
        self.root.config(menu=menubar)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            self.image = Image.open(file_path)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.config(width=self.image.width, height=self.image.height)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

    def start_drawing(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):
        self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, width=2)
        self.last_x = event.x
        self.last_y = event.y

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()








