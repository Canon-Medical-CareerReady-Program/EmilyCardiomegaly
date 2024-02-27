import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from measurement import Measurement
from results import Result
from point import Point
from database import Database
import csv
from typing import List
from tkinter import ttk

#main class. this program uses object orientated programming as it have 4 classes; DrawingApp, Measurement, Result, and Point. 
class DrawingApp:
    def __init__(self, root:tk.Tk):
        self.root = root
        self.root.title("Cardiomegaly Detector")
        self.root.minsize(width=600, height=500)

        #if data folder does'nt exist what happens??? create a folder to fix 
        self.database = Database("Data/results.sqlite")
        Measurement.initialise_database(self.database)
    
        self.button_colors = {"Heart Line": "#C1E3ED", "Thorax Line": "#C1E3ED"} 
         # Button colors based on selected options

        self.image_paths_del = []  # List to store the paths of opened images
        self.current_patient_id = None
        self.current_patient_images = []
        self.current_image_index = -1  # Index of the currently displayed image
        self.image = None
        self.image_tk = None
        self.modified_image = None
        self.drawn_lines = []

        self.create_menu()

        self.ratio = 0.0
        #setting current values for the arrays of values
        self.current_result:Result = None 
        self.current_measurement:Measurement = None
        self.original_image :Image= None


        #saving all the information found in result to the array all_results
        #List does.....
        self.all_results : List[Result] = Measurement.from_database(self.database)

        # Add a dictionary to store the information for each image
        self.pixel_spacing = {} #pixel spacing is used for the resizing of images for different screen sizes
        self.patient_ID = {}
        self.patient_images = {}
        self.patient_gender = {}
        self.patient_age = {}
        self.image_name = [] #an array of the names that the images are stored as in the csv file       


        # Create a separate frame for labels and data with a set width
        label_frame = tk.Frame(root, background="#AAC9DD", width=400)
        label_frame.pack(side=tk.LEFT,fill=tk.BOTH)

        padx = 5
        pady = 5

        #using tkinter i have created labels for all the buttons used in the program    
        self.measurement_label = tk.Label(label_frame, text="Measurements", background="#AAC9DD", font=("Arial", 10))
        self.measurement_label.pack(side="top", padx=padx, pady=pady, anchor="nw")

        self.heart_line_label = tk.Label(label_frame, text="Heart Line Length: 0.0 mm", background="#AAC9DD", font=("Arial", 10))
        self.heart_line_label.pack(side="top", padx=padx, pady=pady, anchor="w")

        self.thorax_line_label = tk.Label(label_frame, text="Thorax Line Length: 0.0 mm", background="#AAC9DD", font=("Arial", 10))
        self.thorax_line_label.pack(side="top", padx=padx, pady=pady, anchor="w")

        self.ratio_label = tk.Label(label_frame, text="Cardiothoracic Ratio:", background="#AAC9DD", font=("Arial", 10))
        self.ratio_label.pack(side="top", padx=padx, pady=pady, anchor="w")

        self.percentage_label = tk.Label(label_frame, text="Percentage of Ratio:", background="#AAC9DD", font=("Arial", 10))
        self.percentage_label.pack(side="top", padx=padx, pady=pady, anchor="w")

        self.Diagnosis_label = tk.Label(label_frame, text="Symptomatic:", background="#AAC9DD", font=("Arial", 10))
        self.Diagnosis_label.pack(side="top", padx=padx, pady=pady, anchor="w")


        # Create a frame to hold the labels and buttons
        image_frame = tk.Frame(root, background="lightgrey")
        image_frame.pack(side="left", expand=True, fill="both", anchor="w")

        self.canvas = tk.Canvas(image_frame)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        #connecting an action to a function. e.g, when a button is in motion, it will call the function draw 
        #which is what makes the lines appear as the user is moving the mouse across the image
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.button_release)
        self.canvas.bind("<Configure>", self.canvas_resized)
        
        #using tkinter to create a frame for the buttons in the program.
        button_frame = tk.Frame(label_frame, background="#AAC9DD", width=400)
        button_frame.pack(side=tk.TOP,fill=tk.BOTH)
        
        self.database_button = tk.Button(button_frame, text="Save to spreadsheet", command=self.save_to_database, background="#C1E3ED", font=("Arial", 10))
        self.database_button.pack(side="top", padx=padx, pady=pady, anchor="sw")

        self.previous_image_button = tk.Button(button_frame, text="Previous Image", command=self.previous_image, background="#C1E3ED", font=("Arial", 10))
        self.previous_image_button.pack(side="left", padx=padx, pady=10, anchor="nw")

        self.next_image_button = tk.Button(button_frame, text="Next Image", command=self.next_image, background="#C1E3ED", font=("Arial", 10))
        self.next_image_button.pack(side="left", padx=padx, pady=10, anchor="nw")
        
    
        self.Info_label = tk.Label(label_frame, text="Patient Info", background="#AAC9DD", font=("Arial", 10))
        self.Info_label.pack(side="top", padx=padx, pady=pady, anchor="nw")

        self.ID_label = tk.Label(label_frame, text="ID:", background="#AAC9DD", font=("Arial", 10))
        self.ID_label.pack(side="top", padx=padx, pady=pady, anchor="nw")

        self.Gender_label = tk.Label(label_frame, text="Gender:", background="#AAC9DD", font=("Arial", 10))
        self.Gender_label.pack(side="top", padx=padx, pady=pady, anchor="nw")

        self.Age_label = tk.Label(label_frame, text="Age:", background="#AAC9DD", font=("Arial", 10))
        self.Age_label.pack(side="top", padx=padx, pady=pady, anchor="nw")


        other_button_frame = tk.Frame(label_frame, background="#AAC9DD", width=400)
        other_button_frame.pack(side=tk.TOP,fill=tk.BOTH)
                
        self.previous_patient_button = tk.Button(other_button_frame, text="Previous Patient", command=self.previous_patient, background="#C1E3ED", font=("Arial", 10))
        self.previous_patient_button.pack(side="left", padx=padx, pady=10, anchor="w")

        self.next_patient_button = tk.Button(other_button_frame, text="Next Patient", command=self.next_patient, background="#C1E3ED", font=("Arial", 10))
        self.next_patient_button.pack(side="left", padx=padx, pady=10, anchor="w")

        self.style = ttk.Style()
        self.style.configure("Selected.TButton", background=self.button_colors["Heart Line"])  # Set initial button color

    #creating a menu to appear at the top of the screen with commands calling on functions 
    #throughout the program when the corresponding button is pressed
    def create_menu(self):
        menubar = tk.Menu(self.root, background="light blue", foreground="black")
        menubar.add_command(label="Open Image", command=self.open_image, background="light blue", foreground="black", font=("Arial", 75))
        menubar.add_command(label="Clear Lines", command=self.clear_canvas, background="light blue", foreground="black", font=("Arial", 75))
        menubar.add_command(label="Heart Line", command=lambda: self.select_variable("Heart Line"), background="light blue", foreground="black", font=("Arial", 75))
        menubar.add_command(label="Thorax Line", command=lambda: self.select_variable("Thorax Line"), background="light blue", foreground="black", font=("Arial", 75))

        self.root.config(menu=menubar)
    
    #this function is executed when the "Open Image" button is pressed in the menu.
    #it stores the images that the user opens and stored it and its name. 
    #it then calls on the functions to load the data that is found with the current image in the data csv file, "Data\BBox_List_2017.csv"
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

    #load and display the image and the data found to go with it in the csv and display them with the corresponding labels on the screen
    def load_current_image(self):
        if 0 <= self.current_image_index < len(self.current_patient_images):
            self.current_result = self.current_patient_images[self.current_image_index]
            self.current_measurement = self.current_result.heart
            self.original_image = Image.open(self.current_result.image_name)
            self.update_image()
                  
            self.ID_label.config(text="ID: {}".format(self.current_result.patient_ID))
            self.Gender_label.config(text="Gender: {}".format(self.current_result.patient_gender))
            self.Age_label.config(text="Age: {}".format(self.current_result.patient_age))

    #this function is called when you mouse or trackpad button is pushed down.
    #it saves the points that the drawing is started at so a line can be drawn starting at that point      
    def start_drawing(self, event):
        self.current_measurement.start = Point(event.x, event.y) / self.calculate_scale_factor()
    
    #similar to the start_drawing function, this saves the coordinate of when the button is relased, so the end of the line
    #it also saves the current body_part (either the heart or the thorax) and saves it as the measurement
    #and calls the calculate_ratio_and_percentage function if there is now measurements stored for both the heart and thorax length
        
    def draw(self, event):
        #store the point (x,y) when the mouse lifts at the end of the drawn lines
        self.current_measurement.end = Point(event.x, event.y) / self.calculate_scale_factor() 

        self.update_body_part(self.current_measurement)

        # Recalculate ratio and percentage
        # The function to calculate the ratio and percentage will be called only when
        # there is values stored for both the heart and thorax line length e.g. when they dont equal 0
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
        self.current_measurement = self.current_result.heart

        # Reset the labels
        self.heart_line_label.config(text="Heart Line Length: 0.0 mm")
        self.thorax_line_label.config(text="Thorax Line Length: 0.0 mm")
        self.ratio_label.config(text="Cardiothoracic Ratio:")
        self.percentage_label.config(text="Percentage of Ratio:")
        self.Diagnosis_label.config(text="Symptomatic:")
        self.ID_label.config(text="ID:")
        self.Gender_label.config(text="Gender:")
        self.Age_label.config(text="Age:")

    def clear_measurements(self):
        self.current_result.heart.clear()
        self.current_result.thorax.clear()

    def next_image(self):
        if self.current_image_index < len(self.image_paths_del) - 1:
            self.current_image_index += 1
            self.load_current_image()
            self.update_results()

        self.update_navigation_buttons()

    def previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_current_image()
            self.update_results()

        self.update_navigation_buttons()

    def save_to_database(self):
        with open("Cardiomegaly Data.csv", mode="a", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Image Name", "Heart Line", "Thorax Line", "Cardiothoracic Ratio", "Percentage", "Symptomatic"])
            for result in self.all_results:
                writer.writerow([result.image_name, self.heart_length_mm, self.thorax_length_mm, result.ratio(), result.percentage(), result.symptoms()])
    
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
                self.ID = int(row["Patient ID"])
                self.gender = str(row["Patient Gender"])
                self.age = int(row["Patient Age"])
                
                # Ok, now we want to find which of the images we selected in the File open dialog (all_results) has a image name that matches the image name in the row
                for result in self.all_results:
                    if image_name == result.short_image_name:
                        result.pixel_spacing[0] = self.pixel_spacing_x
                        result.pixel_spacing[1] = self.pixel_spacing_y
                        result.patient_ID = self.ID
                        result.patient_gender = self.gender
                        result.patient_age = self.age

                        if self.ID not in self.patient_ID:
                            self.patient_ID[self.ID] = []
                        self.patient_ID[self.ID].append(result)

        # Update the image list for the first patient ID (if available)
        if len(self.patient_ID) > 0:
            self.current_patient_id = sorted(self.patient_ID.keys())[0]
            self.update_current_patient_images()

    def update_current_patient_images(self):
        self.current_patient_images = self.patient_ID.get(self.current_patient_id, [])
        if len(self.current_patient_images) > 0:
            self.current_image_index = 0
            self.load_current_image()
        else:
            self.current_image_index = -1
            self.current_result = None
            self.current_measurement = None
            self.original_image = None
            self.canvas.delete("all")
        
        self.update_results()
        self.update_navigation_buttons()

    def next_patient(self):
        if self.current_patient_id is not None:
            patient_ids = sorted(self.patient_ID.keys())
            next_index = patient_ids.index(self.current_patient_id) + 1
            if next_index < len(patient_ids):
                self.current_patient_id = patient_ids[next_index]
                self.update_current_patient_images()
                self.update_results()

    def previous_patient(self):
        if self.current_patient_id is not None:
            patient_ids = sorted(self.patient_ID.keys())
            prev_index = patient_ids.index(self.current_patient_id) - 1
            if prev_index >= 0:
                self.current_patient_id = patient_ids[prev_index]
                self.update_current_patient_images()
                self.update_results()

    def update_navigation_buttons(self):
        if self.current_patient_id is not None:
            patient_ids = sorted(self.patient_ID.keys())
            current_index = patient_ids.index(self.current_patient_id)
            self.next_patient_button.config(state="normal" if current_index < len(patient_ids) - 1 else "disabled")
            self.previous_patient_button.config(state="normal" if current_index > 0 else "disabled")
        if self.current_patient_images is not None:
            self.next_image_button.config(state="normal" if self.current_image_index < len(self.current_patient_images) - 1 else "disabled")
            self.previous_image_button.config(state="normal" if self.current_image_index > 0 else "disabled")

    def update_results(self):
        self.update_body_part(self.current_result.heart)
        self.update_body_part(self.current_result.thorax)

        if self.current_result.heart.length() != 0 and self.current_result.thorax.length() != 0:
            self.ratio_label.config(text="Cardiothoracic Ratio: {:.2f}".format(self.current_result.ratio()))
            self.percentage_label.config(text="Percentage of Ratio: {:.0f}%".format(self.current_result.percentage()))

            if self.current_result.symptoms():
                self.Diagnosis_label.config(text="indicates an enlarged heart.")
            else:
                self.Diagnosis_label.config(text="indicates a normal heart size.")

        else:
            self.ratio_label.config(text="Cardiothoracic Ratio:")
            self.percentage_label.config(text="Percentage of Ratio:")
            self.Diagnosis_label.config(text="Symptomatic:")
        
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