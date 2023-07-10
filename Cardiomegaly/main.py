import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import math
from measurement import Measurement
from results import Result
from point import Point

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

        self.line_length_del = 0.0
        self.heart_line_length = 0.0
        self.thorax_line_length = 0.0
        self.current_variable_del = None

        self.ratio = 0.0

        self.current_result = Result()
        self.current_measurement = None

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
            self.current_result.image_name = self.image_paths[self.current_image_index]
            self.image = Image.open(self.current_result.image_name)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.modified_image = self.image.copy()  # Create a copy for modifications
            self.canvas.config(width=self.image.width, height=self.image.height)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)
            self.clear_measurements()  # Clear the stored measurements
            self.draw_saved_lines()  # Draw the saved lines

    def start_drawing(self, event):
        self.current_measurement.start = Point(event.x, event.y)

    def draw(self, event):
        # Calculate the coordinates for a straight line
        self.current_measurement.end = Point(event.x, event.y)
        
        x0 = self.current_measurement.start.x
        y0 = self.current_measurement.start.y
        x1 = self.current_measurement.end.x
        y1 = self.current_measurement.end.y

        # Draw the straight line
        line_color = "purple" if self.current_variable_del == "Heart Line" else "blue"
        self.canvas.delete("line")  # Delete previous line
        self.canvas.create_line(x0, y0, x1, y1, fill=line_color, width=2, tags="line")

    def draw_saved_lines(self):
        for line_data in self.drawn_lines:
            x0, y0, color = line_data
            self.canvas.create_line(x0, y0, fill=color, width=2, tags="line")

    def select_variable(self, variable):
        if variable == "Heart Line":
            self.current_measurement = self.current_result.heart
        else:
            self.current_measurement = self.current_result.thorax
        self.current_variable_del = variable

    def save_line(self):
        line_color = "purple" if self.current_variable_del == "Heart Line" else "blue"
        self.drawn_lines.append((self.current_measurement.end.x, self.current_measurement.end.y, line_color))
        heart_line_label.config(text="Heart Line Length: {:}".format(self.current_result.heart.length()))
        thorax_line_label.config(text="Lung Line Length: {:}".format(self.current_result.thorax.length()))

        # Reset the line length after saving
        self.line_length_del = 0.0

        # Recalculate ratio and percentage
        if self.current_result.heart.length() != 0 and self.current_result.thorax.length() != 0:
            self.calculate_ratio_and_percentage()

    def calculate_ratio_and_percentage(self):
        ratio_label.config(text="Cardiothoracic Ratio: {:} (Heart: {:}, Lung: {:})".format(self.current_result.ratio(), self.current_result.heart.length(), self.current_result.thorax.length()))
        percentage_label.config(text="Percentage of Ratio: {:.0f}%".format(self.current_result.percentage()))

        if self.current_result.ratio() > 0.5:
            ratio_label.config(text="This patient's Cardiothoracic Ratio is above 0.5, indicating an enlarged heart.")
        else:
            ratio_label.config(text="This patient's Cardiothoracic Ratio is not above 0.5, indicating a normal heart size.")

    def clear_canvas(self):
        self.canvas.delete("line")  # Delete all items on the canvas
        self.drawn_lines = []  # Clear the stored lines
        self.clear_measurements()  # Clear the stored measurements
        self.current_variable_del = None

        # Reset the labels
        heart_line_label.config(text="Heart Line Length: 0.0 ")
        thorax_line_label.config(text="Lung Line Length: 0.0 ")
        ratio_label.config(text="Cardiothoracic Ratio:")
        percentage_label.config(text="Percentage of Ratio:")

    def clear_measurements(self):
        self.current_measurement.clear()

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

    thorax_line_label = tk.Label(frame, text="Lung Line Length: 0.0")
    thorax_line_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

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

