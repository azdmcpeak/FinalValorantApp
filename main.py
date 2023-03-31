import os
import shutil
from kivy.app import App
from PIL import Image, ImageDraw as PILImage
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from numpy import random
from kivy.uix.image import Image as Kimage


class LandingScreen(Screen):
    pass


class ColorGenerator(Screen):

    def set_hex_code(self):
        hex_code_path = 'Saved Crosshair Colors.txt'

        # initialize an empty list for the hex codes
        hex_codes = []

        # loop through all files in the hex codes file
        with open(hex_code_path, 'r') as f:
            for line in f:
                # remove any trailing newline characters
                line = line.rstrip('\n')
                # add the line to the list
                hex_codes.append(line)

    def generate_new_crosshair_color(self, *args):
        map_Images = ["Ascent.PNG", "Icebox.PNG"]

        # Generates the random color to be applied to photos
        maxRed = random.randint(0, 255)
        maxGreen = random.randint(0, 255)
        maxBlue = random.randint(0, 255)

        for Images in map_Images:
            # Open the image file
            image = Image.open(Images)

            # Get the size of the image
            width = image.width
            height = image.height

            # Create a new image with the same size as the original
            new_image = Image.new("RGB", (width, height), (255, 255, 255))

            # Paste the original image onto the new image
            new_image.paste(image, (0, 0))

            draw = PILImage.Draw(new_image)
            center_x = width // 2
            center_y = height // 2
            radius = 5
            color = (maxRed, maxGreen, maxBlue)  # Change the color to the desired color
            draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=color)

            # Set the image source of the Image widget
            new_image_name = "Crosshair backgrounds/" + Images
            new_image.save(new_image_name)
            rgb = (maxRed, maxGreen, maxBlue)
            hex_value = str('#{:02x}{:02x}{:02x}'.format(*rgb))
            self.ids.hexcode_Value.text = hex_value
            self.ids.Ascent.source = "Crosshair backgrounds/Ascent.png"
            self.ids.Icebox.source = "Crosshair backgrounds/Icebox.png"
            image.close()
            self.ids.Ascent.reload()
            self.ids.Icebox.reload()

    def saveCrosshair(self, *args):
        # writing the hex codes to a text file
        color_Code = self.manager.get_screen("color generator").ids.hexcode_Value.text + "\n"
        opened_File_Crosshair_codes = open("Saved Crosshair Colors.txt", "a")
        opened_File_Crosshair_codes.write(color_Code)
        opened_File_Crosshair_codes.close()

        # Define the source and destination folders
        source_folder = 'Crosshair backgrounds'
        destination_folder = 'Saved Crosshair Screenshots'

        # Create the destination folder if it does not exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Loop through all files in the source folder
        for filename in os.listdir(source_folder):
            # Check if the file is a PNG
            if filename.endswith('.PNG'):
                # Construct the full path of the source and destination files
                source_file = os.path.join(source_folder, filename)
                destination_file = os.path.join(destination_folder, filename)
                # Check if the destination file already exists
                if os.path.exists(destination_file):
                    # Append a counter to the filename
                    counter = 0
                    while True:
                        new_destination_file = os.path.join(destination_folder,
                                                            f"{os.path.splitext(filename)[0]}_{counter}.png")
                        if os.path.exists(new_destination_file):
                            counter += 1
                        else:
                            destination_file = new_destination_file
                            break
                # Copy the source file to the destination folder
                shutil.copy(source_file, destination_file)


class ShowSavedColors(Screen):
    def on_enter(self, *args):

        screen_shots_path = 'Saved Crosshair Screenshots'
        hex_code_path = 'Saved Crosshair Colors.txt'

        # initialize an empty list for the hex codes
        hex_codes = []
        # initialize an empty list for files with "Ascent" in their name
        ascent_files = []
        # initialize an empty list for files with "Icebox" in their name
        icebox_files = []

        # loop through all files in the hex codes file
        with open(hex_code_path, 'r') as f:
            for line in f:
                # remove any trailing newline characters
                line = line.rstrip('\n')
                # add the line to the list
                hex_codes.append(line)

            # loop through all files in the screenshots folder
        for filename in os.listdir(screen_shots_path):
            file_path = os.path.join(screen_shots_path, filename)
            if os.path.isfile(file_path):
                if 'Ascent' in filename:
                    ascent_files.append("Saved Crosshair Screenshots/" + filename)
                elif 'Icebox' in filename:
                    icebox_files.append("Saved Crosshair Screenshots/" + filename)

        for i in range(len(hex_codes)):
            hex_code_label = Label(text=hex_codes[i])
            self.ids.container.add_widget(hex_code_label)

            ascent_files_screenshots = Kimage(source=ascent_files[i], size_hint=(None, None), size=(350, 200))
            self.ids.container.add_widget(ascent_files_screenshots)

            icebox_files_screenshots = Kimage(source=icebox_files[i], size_hint=(None, None), size=(350, 200))
            self.ids.container.add_widget(icebox_files_screenshots)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('Design.kv')


class MainApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    MainApp().run()
