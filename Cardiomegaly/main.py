import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import math
from measurement import Measurement
from results import Result
from point import Point
import csv
from typing import List
from tkinter import ttk


class DrawingApp:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("Poo Detector")

        self.root.minsize(width=600, height=500)
    
        self.button_colors = {"Heart Line": "#C1E3ED", "Thorax Line": "#C1E3ED"}  # Button colors based on selected options

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
        self.original_image :Image= None


        self.all_results : List[Result] = []

        # Add a dictionary to store the pixel spacing for each image
        self.pixel_spacing = {}
        self.image_name = []        

        # Create a separate frame for labels and data with a set width
        label_frame = tk.Frame(root, background="#AA9DD", width=400)
        label_frame.pack(side=tk.LEFT,fill=tk.BOTH)

        self.heart_line_label = tk.Label(label_frame, text="Heart Line Length: 0.0", background="#AAC9DD")
        padx = 10
        pady = 10
        self.heart_line_label.pack(side="top", pad=padx, pady=pady, anchor="w")

        self.thorax_line_label = tk.Label(label_frame, text="Thorax Line Length: 0.0", background="#AAC9DD")
        self.thorax_line_label.pack(side="top", padx=padx, pady=pady, anchor="w")

        self.ratio_label = tk.Label(label_frame, text="Cardiothoracic Ratio:", background="#AAC9DD")
        self.ratio_label.pack(side="top", padx=padx, pady=pady, anchor="w")

        self.percentage_label = tk.Label(label_frame, text="Percentage of Ratio:", background="#AAC9D")
        self.percentage_label.pack(side="top", padx=padx, pady=pady, anchor="w")

        self.Diagnosis_label = tk.Label(label_frame, text="Diagnosis:", background="#AAC9DD")
        self.Diagnosis_label.pack(side="top", padx=padx, pady=pady, anchor="w")


        # Create a frame to hold the labels and buttons
        image_frame = tk.Frame(root, background="lightgrey")
        image_frame.pack(side="left", expand=True, fill="both", anchor="w")

        self.canvas = tk.Canvas(image_frame)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.button_release)
        self.canvas.bind("<Configure>", self.canvas_resized)
        

        button_frame = tk.Frame(label_frame, background="#AAC9DD", width=400)
        button_frame.pack(side=tk.TOP,fill=tk.BOTH)

        self.next_button = tk.Button(button_frame, text="Next", command=self.next_image, background="#C1E3ED")
        self.next_button.pack(side="left", padx=padx, pady=pady, anchor="sw")

        self.previous_button = tk.Button(button_frame, text="Previous", command=self.previous_image, background="#C1E3ED")
        self.previous_button.pack(side="left", padx=padx, pady=pady, anchor="sw")

        self.spreadsheet_button = tk.Button(button_frame, text="Save to spreadsheet", command=self.save_to_spreadsheet, background="#C1E3ED")
        self.spreadsheet_button.pack(side="left", padx=padx, pady=pady, anchor="sw")

        self.style = ttk.Style()
        self.style.configure("Selected.TButton", background=Self.button_colors["Heart Line"])  # Set initial button color

    

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
                result.short_image_name = file_path.split('/')[-1]
                self.all_results.append(result)
            self.load_image_metadata()
            self.load_current_image()  # Load the current image


    def load_current_image(self):
        if self.current_image_index >= 0 and self.current_image_index < len(self.image_paths_del):
            self.current_result = self.all_results[self.current_image_index]
            self.current_measurement = self.current_result.heart
            self.original_image = Image.open(self.current_result.image_name)
            self.update_image()

    def start_drawing(self, event):
        self.current_measurement.start = Point(event.x, event.y) / self.calculate_scale_factor()

    def draw(self, event):
        self.current_measurement.end = Point(event.x, event.y) / self.calculate_scale_factor() 

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
        self.update_button_colors()
       

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
        self.current_result.heart.clear()
        self.current_result.thorax.clear()

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

    def save_to_spreadsheet(self):
        with open("Cardiomegaly Data.csv", mode="w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Image Name", "Heart Line", "Thorax Line", "Cardiothoracic Ratio", "Percentage", "Symptomatic"])
            for result in self.all_results:
                writer.writerow([result.image_name, result.heart.length(), result.thorax.length(), result.ratio(), result.percentage(), result.symptoms()])
    
    def update_button_colors(self):
        # Update button colors based on the selected option
        for button_name, button_color in self.button_colors.items():
            style_name = f"{button_name}.TButton"
            if button_name == self.current_measurement.body_part:
                self.style.configure(style_name, background=button_color, relief="sunken")
            else:
                self.style.configure(style_name, background=button_color, relief="raised")

    def canvas_resized(self, event):
        print(f"{self.canvas.winfo_width()}, {self.canvas.winfo_height()}")
        self.update_image()
        self.update_results()


    def update_image(self):
        if self.original_image !=None:
            self.canvas_width = self.canvas.winfo_width()
            self.canvas_height = self.canvas.winfo_height()
            self.image_ratio = self.original_image.size[0] / self.original_image.size[1]
            self.canvas_ratio = self.canvas_width / self.canvas_height

            if self.canvas_ratio > self.image_ratio:
                height = int(self.canvas_height)
                width = int(height * self.image_ratio)
            else:
                width = int(self.canvas_width)
                height = int(width / self.image_ratio)

            size_tuple= (width,height)
            resized_image = self.original_image.resize(size=size_tuple)
            self.tkimage= ImageTk.PhotoImage(image=resized_image)
            print(resized_image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.tkimage)

    def calculate_scale_factor(self):
        if self.original_image !=None:
            self.canvas_width = self.canvas.winfo_width()
            self.canvas_height = self.canvas.winfo_height()
            self.image_width, self.image_height = self.original_image.size
            self.scale_x = self.canvas_width / self.image_width
            self.scale_y = self.canvas_height / self.image_height

            # Choose the smaller scale factor to maintain the image's aspect ratio
            scale_factor = min(self.scale_x, self.scale_y)

            return scale_factor

        return 1.0  # Default scale factor if there is no image
    

    def load_image_metadata(self):        
        with open("Data\BBox_List_2017.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            # For each row in the CSV file...
            for row in reader:
                # Load bits of the row from the CSV file...
                image_name = row["Image Index"]
                self.pixel_spacing_x = float(row["OriginalImagePixelSpacingX"])
                self.pixel_spacing_y = float(row["OriginalImagePixelSpacingY"])
                # Ok, now we want to find which of the images we selected in the File open dialog (all_results) has a image name that matches the image name in the row
                for result in self.all_results:
                    if image_name == result.short_image_name:
                        result.pixel_spacing[0] = self.pixel_spacing_x
                        result.pixel_spacing[1] = self.pixel_spacing_y


    def convert_to_mm(self):
        self.current_measurement.start.x *= self.pixel_spacing_x
        self.current_measurement.start.y *= self.pixel_spacing_y
        self.current_measurement.end.x *= self.pixel_spacing_x
        self.current_measurement.end.y *= self.pixel_spacing_y


    def update_results(self):

        self.update_body_part(self.current_result.heart)
        self.update_body_part(self.current_result.thorax)

        if self.current_result.heart.length() != 0 and self.current_result.thorax.length() != 0:
            self.ratio_label.config(text="Cardiothoracic Ratio: {:.2f}".format(self.current_result.ratio()))
            self.percentage_label.config(text="Percentage of Ratio: {:.0f}%".format(self.current_result.percentage()))

            if self.current_result.symptoms():
                self.Diagnosis_label.config(text="Ratio is > 0.5, indicating an enlarged heart.")
            else:
                self.Diagnosis_label.config(text="Ratio is not > 0.5, indicating a normal heart size.")

        else:
            self.ratio_label.config(text="Cardiothoracic Ratio:")
            self.percentage_label.config(text="Percentage of Ratio:")
            self.Diagnosis_label.config(text="Diagnosis:")
        


    def update_body_part(self, measurement:Measurement): 
        self.scale_factor = self.calculate_scale_factor()
       
        x0 = measurement.start.x * self.scale_factor
        y0 = measurement.start.y * self.scale_factor
        x1 = measurement.end.x * self.scale_factor
        y1 = measurement.end.y * self.scale_factor

        self.heart_length_mm = self.current_result.heart.length() * self.current_result.pixel_spacing[0]
        self.thorax_length_mm = self.current_result.thorax.length() * self.current_result.pixel_spacing[0]

        # Draw the straight line
        line_color = "purple" if measurement == self.current_result.heart else "blue"
        self.canvas.delete(measurement.body_part)  # Delete previous line
        self.canvas.create_line(x0, y0, x1, y1, fill=line_color, width=2, tags=measurement.body_part)

        self.heart_line_label.config(text="Heart Line Length: {:.2f} mm".format(self.heart_length_mm))
        self.thorax_line_label.config(text="Thorax Line Length: {:.2f} mm".format(self.thorax_length_mm))

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()

