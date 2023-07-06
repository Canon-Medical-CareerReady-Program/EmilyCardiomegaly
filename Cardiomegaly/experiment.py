import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import math

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cardiomegaly Detector")

        self.canvas = tk.Canvas(self.root, width=600, height=400)
        self.canvas.grid(row=0, column=1, rowspan=5, padx=10, pady=10)

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)

        self.image_paths = []  # List to store the paths of opened images
        self.current_image_index = -1  # Index of the currently displayed image

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
        menubar = tk.Menu(self.root, background="light blue", foreground="black")
        file_menu = tk.Menu(menubar, tearoff=0, background="light blue", foreground="black")
        file_menu.add_command(label="Open", command=self.open_image, background="light blue", foreground="black")
        menubar.add_cascade(label="File", menu=file_menu, background="light blue", foreground="black")

        menubar.add_cascade(label="Save Line", command=self.save_line, background="light blue", foreground="black")
        menubar.add_cascade(label="Clear", command=self.clear_canvas, background="light blue", foreground="black")

        variable_menu = tk.Menu(menubar, tearoff=0, background="light blue", foreground="black")
        variable_menu.add_command(label="Heart Line", command=lambda: self.select_variable("Heart Line"), background="light blue", foreground="black")
        variable_menu.add_command(label="Lung Line", command=lambda: self.select_variable("Lung Line"), background="light blue", foreground="black")
        menubar.add_cascade(label="Select Variable", menu=variable_menu, background="light blue", foreground="black")

        self.root.config(menu=menubar)

    def open_image(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])
        if file_paths:
            self.image_paths = list(file_paths)  # Store the selected image paths
            self.current_image_index = 0  # Set the current image index to the first image
            self.load_current_image()  # Load the current image

    def load_current_image(self):
        if self.current_image_index >= 0 and self.current_image_index < len(self.image_paths):
            file_path = self.image_paths[self.current_image_index]
            self.image = Image.open(file_path)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.modified_image = self.image.copy()  # Create a copy for modifications
            self.canvas.config(width=self.image.width, height=self.image.height)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)
            self.clear_measurements()  # Clear the stored measurements
            self.draw_saved_lines()  # Draw the saved lines

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
        line_color = "purple" if self.current_variable == "Heart Line" else "blue"
        self.canvas.delete("line")  # Delete previous line
        self.canvas.create_line(x0, y0, x1, y1, fill=line_color, width=2, tags="line")

    def draw_saved_lines(self):
        for line_data in self.drawn_lines:
            x0, y0, color = line_data
            self.canvas.create_line(x0, y0, x0, y0, fill=color, width=2, tags="line")

    def select_variable(self, variable):
        self.current_variable = variable

    def save_line(self):
        line_color = "purple" if self.current_variable == "Heart Line" else "blue"
        self.drawn_lines.append((self.last_x, self.last_y, line_color))
        if self.current_variable == "Heart Line":
            self.heart_line_length = self.line_length
            heart_line_label.config(text="Heart Line Length: {:}".format(self.heart_line_length))
        elif self.current_variable == "Lung Line":
            self.lung_line_length = self.line_length
            lung_line_label.config(text="Lung Line Length: {:}".format(self.lung_line_length))

        # Reset the line length after saving
        self.line_length = 0.0

        # Recalculate ratio and percentage
        if self.heart_line_length != 0 and self.lung_line_length != 0:
            self.calculate_ratio_and_percentage()

    def calculate_ratio_and_percentage(self):
        ratio = self.heart_line_length / self.lung_line_length
        ratio_label.config(text="Cardiothoracic Ratio: {:} (Heart: {:}, Lung: {:})".format(ratio, self.heart_line_length, self.lung_line_length))
        percentage = round(ratio * 100, 2)
        percentage_label.config(text="Percentage of Ratio: {:.0f}%".format(percentage))

        if ratio > 0.5:
            ratio_label.config(text="This patient's Cardiothoracic Ratio is above 0.5, indicating an enlarged heart.")
        else:
            ratio_label.config(text="This patient's Cardiothoracic Ratio is not above 0.5, indicating a normal heart size.")

    def clear_canvas(self):
        self.canvas.delete("line")  # Delete all items on the canvas
        self.drawn_lines = []  # Clear the stored lines
        self.clear_measurements()  # Clear the stored measurements
        self.current_variable = None

        # Reset the labels
        heart_line_label.config(text="Heart Line Length: 0.0 ")
        lung_line_label.config(text="Lung Line Length: 0.0 ")
        ratio_label.config(text="Cardiothoracic Ratio:")
        percentage_label.config(text="Percentage of Ratio:")

    def clear_measurements(self):
        self.line_length = 0.0
        self.heart_line_length = 0.0
        self.lung_line_length = 0.0

    def next_image(self):
        if self.current_image_index < len(self.image_paths) - 1:
            self.current_image_index += 1
            self.clear_measurements()  # Clear measurements when switching image
            self.load_current_image()

    def previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.clear_measurements()  # Clear measurements when switching image
            self.load_current_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)

    # Create a frame to hold the labels and buttons
    frame = tk.Frame(root)
    frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    heart_line_label = tk.Label(frame, text="Heart Line Length: 0.0")
    heart_line_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    lung_line_label = tk.Label(frame, text="Lung Line Length: 0.0")
    lung_line_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    ratio_label = tk.Label(frame, text="Cardiothoracic Ratio:")
    ratio_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

    percentage_label = tk.Label(frame, text="Percentage of Ratio:")
    percentage_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

    next_button = tk.Button(frame, text="Next", command=app.next_image)
    next_button.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    previous_button = tk.Button(frame, text="Previous", command=app.previous_image)
    previous_button.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    # Move the image canvas to the right side
    app.canvas.grid(row=0, column=1, rowspan=5, padx=10, pady=10, sticky="nsew")

    root.mainloop()

