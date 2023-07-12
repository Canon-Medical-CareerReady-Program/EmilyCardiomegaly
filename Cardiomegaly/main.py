import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import math
from measurement import Measurement
from results import Result
from point import Point

class DrawingApp:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("Cardiomegaly Detector")

        self.root.minsize(width=600, height=500)
    
        

        self.image_paths_del = []  # List to store the paths of opened images
        self.current_image_index = -1  # Index of the currently displayed image

        self.image = None
        self.image_tk = None
        self.modified_image = None
        self.drawn_lines = []

        self.create_menu()

        self.ratio = 0.0

        self.current_result:Result = None
        self.current_measurement:Measurement = None

        self.all_results = []

        # Create a separate frame for labels and data with a set width
        label_frame = tk.Frame(root, background="#797EF6", width=500)
        label_frame.pack(side="left", expand=False, fill="y", anchor="w")

        self.heart_line_label = tk.Label(label_frame, text="Heart Line Length: 0.0", background="#797EF6")
        padx = 10
        pady = 10
        self.heart_line_label.pack(side="top", padx=padx, pady=pady, anchor="w")

        self.thorax_line_label = tk.Label(label_frame, text="Thorax Line Length: 0.0", background="#797EF6")
        self.thorax_line_label.pack(side="top", padx=padx, pady=pady, anchor="w")

        self.ratio_label = tk.Label(label_frame, text="Cardiothoracic Ratio:", background="#797EF6")
        self.ratio_label.pack(side="top", padx=padx, pady=pady, anchor="w")

        self.percentage_label = tk.Label(label_frame, text="Percentage of Ratio:", background="#797EF6")
        self.percentage_label.pack(side="top", padx=padx, pady=pady, anchor="w")

        self.Diagnosis_label = tk.Label(label_frame, text="Diagnosis:", background="#797EF6")
        self.Diagnosis_label.pack(side="top", padx=padx, pady=pady, anchor="w")


        # Create a frame to hold the labels and buttons
        image_frame = tk.Frame(root, background="green")
        image_frame.pack(side="left", expand=True, fill="both", anchor="w")

        self.canvas = tk.Canvas(image_frame, background="blue")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.button_release)
        

        button_frame = tk.Frame(image_frame, background="purple")
        button_frame.pack()

        self.next_button = tk.Button(image_frame, text="Next", command=self.next_image, background="#797EF6")
        self.next_button.pack(side="bottom", padx=padx, pady=pady, anchor="se")

        self.previous_button = tk.Button(image_frame, text="Previous", command=self.previous_image, background="#797EF6")
        self.previous_button.pack(side="bottom", padx=padx, pady=pady, anchor="sw")

    

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
            #self.canvas.config(width=self.image.width, height=self.image.height)
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

    def button_release(self, event):
        if self.current_measurement == self.current_result.heart:
            self.current_measurement = self.current_result.thorax


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
        self.heart_line_label.config(text="Heart Line Length: 0.0 ")
        self.thorax_line_label.config(text="Thorax Line Length: 0.0 ")
        self.ratio_label.config(text="Cardiothoracic Ratio:")
        self.percentage_label.config(text="Percentage of Ratio:")
        self.Diagnosis_label.config(text="Diagnosis:")

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
            self.ratio_label.config(text="Cardiothoracic Ratio: {:.2f}".format(self.current_result.ratio(), self.current_result.heart.length(), self.current_result.thorax.length()))
            self.percentage_label.config(text="Percentage of Ratio: {:.0f}%".format(self.current_result.percentage()))

            if self.current_result.ratio() > 0.5:
                self.Diagnosis_label.config(text="Ratio is > 0.5, indicating an enlarged heart.")
            else:
                self.Diagnosis_label.config(text="Ratio is not > 0.5, indicating a normal heart size.")

        else:
            self.ratio_label.config(text="Cardiothoracic Ratio:")
            self.percentage_label.config(text="Percentage of Ratio:")
            self.Diagnosis_label.config(text="Diagnosis:")



    def update_body_part(self, measurement:Measurement): 

        x0 = measurement.start.x
        y0 = measurement.start.y
        x1 = measurement.end.x
        y1 = measurement.end.y

        # Draw the straight line
        line_color = "purple" if measurement == self.current_result.heart else "blue"
        self.canvas.delete(measurement.body_part)  # Delete previous line
        self.canvas.create_line(x0, y0, x1, y1, fill=line_color, width=2, tags=measurement.body_part)

        self.heart_line_label.config(text="Heart Line Length: {:.2f}".format(self.current_result.heart.length()))
        self.thorax_line_label.config(text="Thorax Line Length: {:.2f}".format(self.current_result.thorax.length()))




if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

