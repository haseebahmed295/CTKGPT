
import json
class Settings(object):
    def __init__(self ,root):
        self.root = root
        settings_file_path = 'prefs/settings.json'

        # Load settings from the JSON file
        with open(settings_file_path, 'r') as file:
            settings = json.load(file)
        
        # Assign the settings to instance attributes
        self.model = settings.get("Model", "default-model")  # Provide a default value if the key doesn't exist
        self.bubble_color = settings.get("Bubble_color", "#FFFFFF")  # Default white color
        self.code_color = settings.get("code_color", "#ff5d5d")  # Default red color
        self.code_lable = settings.get("code_lable", "#737d7d")  # Default gray color
        self.font_size = settings.get("font_size", 15)  # Default font size
        self.theme = settings.get("theme", "Dark")  # Default theme
        self.scaling = settings.get("scaling", "100%")  # Default theme
        self.frame_color = settings.get("frame_color", "#111827")  # Default theme
    