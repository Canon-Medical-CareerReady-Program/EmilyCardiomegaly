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

        self.image_paths_del = []  # List to store the paths of opened images
        self.current_image_index = -1  # Index of the currently displayed image

        self.image = None
        self.image_tk = None
        self.modified_image = None
        self.drawn_lines = []

        self.create_menu()

        self.ratio = 0.0

        self.current_result = None
        self.current_measurement = None

        self.all_results = []

    def create_menu(self):
        menubar = tk.Menu(self.root, background="light blue", foreground="black")
        menubar.add_cascade(label="Open", command=self.open_image, background="light blue", foreground="black")
        menubar.add_cascade(label="Clear", command=self.clear_canvas, background="light blue", foreground="black")
        menubar.add_cascade(label="Heart Line", command=lambda: self.select_variable("Heart Line"), background="light blue", foreground="black")
        menubar.add_cascade(label="Thorax Line", command=lambda: self.select_variable("Thorax Line"), background="light blue", foreground="black")

        self.root.config(menu=menubar)

    def open_image(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])
        if file_paths:
            self.image_paths_del = list(file_paths)  # Store the selected image paths
            self.current_image_index = 0  # Set the current image index to the first image
            for file_path in file_paths:
                result = Result()
                result.image_name = file_path
                self.all_results.append(result)
            self.load_current_image()  # Load the current image


    def load_current_image(self):
        if self.current_image_index >= 0 and self.current_image_index < len(self.image_paths_del):
            self.current_result = self.all_results[self.current_image_index]
            self.current_measurement = self.current_result.heart
            self.image = Image.open(self.current_result.image_name)
            self.image_tk = ImageTk.PhotoImage(self.image)
            self.canvas.config(width=self.image.width, height=self.image.height)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

    def start_drawing(self, event):
        self.current_measurement.start = Point(event.x, event.y)

    def draw(self, event):
        # Calculate the coordinates for a straight line
        self.current_measurement.end = Point(event.x, event.y)
        
        self.update_body_part(self.current_measurement)

        # Recalculate ratio and percentage
        if self.current_result.heart.length() != 0 and self.current_result.thorax.length() != 0:
            self.calculate_ratio_and_percentage()


    def select_variable(self, variable):
        if variable == "Heart Line":
            self.current_measurement = self.current_result.heart
        else:
            self.current_measurement = self.current_result.thorax
       

    def calculate_ratio_and_percentage(self):
        self.update_results()

    def clear_canvas(self):
        self.canvas.delete(self.current_result.heart.body_part) 
        self.canvas.delete(self.current_result.thorax.body_part) # Delete all items on the canvas
        self.drawn_lines = []  # Clear the stored lines
        self.clear_measurements()  # Clear the stored measurements

        # Reset the labels
        heart_line_label.config(text="Heart Line Length: 0.0 ")
        thorax_line_label.config(text="Thorax Line Length: 0.0 ")
        ratio_label.config(text="Cardiothoracic Ratio:")
        percentage_label.config(text="Percentage of Ratio:")
        Diagnosis_label.config(text="Diagnosis:")

    def clear_measurements(self):
        self.current_measurement.clear()

    def next_image(self):
        if self.current_image_index < len(self.image_paths_del) - 1:
            self.current_image_index += 1
            self.load_current_image()
            self.update_results()

    def previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_current_image()
            self.update_results()


    def update_results(self):

        self.update_body_part(self.current_result.heart)
        self.update_body_part(self.current_result.thorax)

        if self.current_result.heart.length() != 0 and self.current_result.thorax.length() != 0:
            ratio_label.config(text="Cardiothoracic Ratio: {:.2f}".format(self.current_result.ratio(), self.current_result.heart.length(), self.current_result.thorax.length()))
            percentage_label.config(text="Percentage of Ratio: {:.0f}%".format(self.current_result.percentage()))

            if self.current_result.ratio() > 0.5:
                Diagnosis_label.config(text="Ratio is > 0.5, indicating an enlarged heart.")
            else:
                Diagnosis_label.config(text="Ratio is not > 0.5, indicating a normal heart size.")

        else:
            ratio_label.config(text="Cardiothoracic Ratio:")
            percentage_label.config(text="Percentage of Ratio:")
            Diagnosis_label.config(text="Diagnosis:")



    def update_body_part(self, measurement):

        x0 = measurement.start.x
        y0 = measurement.start.y
        x1 = measurement.end.x
        y1 = measurement.end.y

        # Draw the straight line
        line_color = "purple" if measurement == self.current_result.heart else "blue"
        self.canvas.delete(measurement.body_part)  # Delete previous line
        self.canvas.create_line(x0, y0, x1, y1, fill=line_color, width=2, tags=measurement.body_part)

        heart_line_label.config(text="Heart Line Length: {:.2f}".format(self.current_result.heart.length()))
        thorax_line_label.config(text="Thorax Line Length: {:.2f}".format(self.current_result.thorax.length()))




if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)

    root.option_add("*Menu.background", "blue")
    root.option_add("*Menu.foreground", "white")

    # Create a frame to hold the labels and buttons
    frame = tk.Frame(root)
    frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    # Create a separate frame for labels and data with a set width
    label_frame = tk.Frame(frame, width=500, height=800)
    label_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    heart_line_label = tk.Label(label_frame, text="Heart Line Length: 0.0")
    heart_line_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    thorax_line_label = tk.Label(label_frame, text="Thorax Line Length: 0.0")
    thorax_line_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    ratio_label = tk.Label(label_frame, text="Cardiothoracic Ratio:")
    ratio_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

    percentage_label = tk.Label(label_frame, text="Percentage of Ratio:")
    percentage_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

    Diagnosis_label = tk.Label(label_frame, text="Diagnosis:")
    Diagnosis_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

    next_button = tk.Button(label_frame, text="Next", command=app.next_image)
    next_button.grid(row=10, column=0, padx=10, pady=5, sticky="w")

    previous_button = tk.Button(label_frame, text="Previous", command=app.previous_image)
    previous_button.grid(row=10, column=0, padx=10, pady=5, sticky="s")



    # Move the image canvas to the right side
    app.canvas.grid(row=0, column=1, rowspan=5, padx=10, pady=10, sticky="nsew")

    root.mainloop()

