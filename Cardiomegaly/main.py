import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import math

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.grid()

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)

        self.image = None
        self.image_tk = None
        self.modified_image = None
        self.drawn_lines = []

        self.create_menu()

        self.line_length = 0.0
        self.heart_line_length = 0.0
        self.lung_line_length = 0.0
        self.current_variable = None

        self.ratio = 0.0

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save Line", command=self.save_line)
        menubar.add_cascade(label="File", menu=file_menu)

        variable_menu = tk.Menu(menubar, tearoff=0)
        variable_menu.add_command(label="Heart Line", command=lambda: self.select_variable("Heart Line"))
        variable_menu.add_command(label="Lung Line", command=lambda: self.select_variable("Lung Line"))
        menubar.add_cascade(label="Select Variable", menu=variable_menu)

        self.root.config(menu=menubar)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            self.image = Image.open(file_path)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.modified_image = self.image.copy()  # Create a copy for modifications
            self.canvas.config(width=self.image.width, height=self.image.height)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

    def start_drawing(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):
        # Calculate the coordinates for a straight line
        x0 = self.last_x
        y0 = self.last_y
        x1 = event.x
        y1 = event.y

        # Compute the line length
        distance = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        self.line_length += distance

        # Draw the straight line
        self.canvas.delete("line")  # Delete previous line
        self.canvas.create_line(x0, y0, x1, y1, fill="red", width=2, tags="line")

    def select_variable(self, variable):
        self.current_variable = variable

    def save_line(self):
        if self.current_variable == "Heart Line":
            self.heart_line_length = self.line_length
        elif self.current_variable == "Lung Line":
            self.lung_line_length = self.line_length

        # Reset the line length after saving
        self.line_length = 0.0

    def get_heart_line_length(self):
        return self.heart_line_length

    def get_lung_line_length(self):
        return self.lung_line_length


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)

    label_frame = tk.Frame(root)
    label_frame.pack(side="top", padx=10, pady=10)

    heart_line_label = tk.Label(root, text="Heart Line Length: 0.0 cm")
    heart_line_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    lung_line_label = tk.Label(root, text="Lung Line Length: 0.0 cm")
    lung_line_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    ratio_label = tk.Label(root, text="Cardiothoracic Ratio:")
    ratio_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    percentage_label = tk.Label(root, text="Percentage of Ratio:")
    percentage_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    def update_line_lengths():
        heart_line_length = app.get_heart_line_length()
        lung_line_length = app.get_lung_line_length()
        heart_line_label.config(text="Heart Line Length:".format(heart_line_length))
        lung_line_label.config(text="Lung Line Length:".format(lung_line_length))

        if heart_line_length != 0 and lung_line_length != 0:
            calculation(heart_line_length, lung_line_length)
        else:
            root.after(100, update_line_lengths)  # Update every 100 milliseconds

    def calculation(heart_line_length, lung_line_length):
        ratio = heart_line_length / lung_line_length
        ratio_label.config(text="Cardiothoracic Ratio: {:}".format(ratio))
        percentage = round(ratio * 100, 2)
        percentage_label.config(text="Percentage of Ratio: {:.0f}%".format(percentage))

        if ratio > 0.5:
            ratio_label.config(text="This patient's Cardiothoracic Ratio is above 0.5, indicating an enlarged heart.")
        else:
            ratio_label.config(text="This patient's Cardiothoracic Ratio is not above 0.5, indicating a normal heart size.")

    update_line_lengths()  

    root.mainloop()

   
















