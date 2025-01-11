from typing import List, Dict
import configparser
import subprocess
import os


class Theme:
    def __init__(self):
        print("Initializing Theme class")
        self.current_theme: str = None
        self.wallpaper: str = None
        self.tools: List[str] = None
        self.colors: Dict[str, str] = {}
        self.tool_images: Dict[str, str] = {}
        user = os.environ.get("USER")
        self.path_to_config: str = f"/home/{user}/.config"
        self.current_theme_config = None
        self.global_config = None
        if not os.path.exists(f"{self.path_to_config}/theme_manager"):
            print("Creating base config")
            self.create_base_config()
        print("Fetching settings")
        self.fetch_settings()

    def create_base_config(self):
        print("create_base_config called")
        path = f"{self.path_to_config}/theme_manager"
        try:
            os.mkdir(path)
            print(f"Directory created: {path}")
        except PermissionError:
            print(f"Permission denied: Unable to create '{path}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
        config = configparser.ConfigParser()
        config["DEFAULT"] = {
            "SelectedTheme": "theme_example",
            "Tools": "/home/yourname/.config/example/config, /home/yourname/.config/example_2/config"
        }
        try:
            with open(f"{path}/config.ini", "w") as configfile:
                config.write(configfile)
            print(f"Config file created: {path}/config.ini")
        except Exception as e:
            print(f"An error occurred while writing config.ini: {e}")
        self.create_example_theme()

    def create_example_theme(self):
        print("create_example_theme called")
        theme_path_dir = f"{self.path_to_config}/theme_manager/themes"
        if not os.path.exists(theme_path_dir):
            try:
                os.mkdir(theme_path_dir)
                print(f"Directory created: {theme_path_dir}")
            except Exception as e:
                print(f"An error occurred: {e}")
        path = f"{theme_path_dir}/theme_example.ini"
        config = configparser.ConfigParser()
        try:
            with open(path, "w") as f:
                config.write(f)
            print(f"Example theme file created: {path}")
        except PermissionError:
            print(f"Permission denied: Unable to create '{path}'.")
        except Exception as e:
            print(f"An error occurred: {e}")
        config = configparser.ConfigParser()
        config["Colors"] = {}
        config["Colors"]["PrimaryColor"] = ""
        config["Colors"]["SecondaryColor"] = ""
        config["Colors"]["TextColor"] = ""
        config["Colors"]["AccentColor"] = ""
        config["Wallpaper"] = {}
        config["Wallpaper"]["Path"] = ""
        try:
            with open(path, "w") as f:
                config.write(f)
            print("Example theme content written")
        except Exception as e:
            print(f"An error occurred while writing to '{path}': {e}")

    def set_wallpaper(self):
        print(f"Setting wallpaper: {self.wallpaper}")
        command = ["feh", "--bg-center", self.wallpaper]
        try:
            subprocess.run(command, capture_output=True, check=True, text=True)
            print("Wallpaper set successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error detected: {e.stderr}")
        except FileNotFoundError:
            print("Error: 'feh' command not found. Please ensure 'feh' is installed and available in PATH.")

    def set_colors(self):
        print("Setting colors")
        for path in self.tools:
            path = path.strip()
            print(f"Processing tool config: {path}")
            if not os.path.exists(path):
                print(f"File not found: {path}")
                continue
            filename = os.path.basename(path)
            ext = filename.rsplit('.', 1)[1] if '.' in filename else ''
            try:
                with open(path, 'r') as file:
                    lines = file.readlines()
                updated = False
                with open(path, 'w') as file:
                    for line in lines:
                        updated_line = line
                        line_stripped = line.strip()
                        if ext == 'ini':
                            for key, value in self.colors.items():
                                if line_stripped.startswith(f"{key}"):
                                    # Handle spaces around "="
                                    key_part, _, value_part = line_stripped.partition("=")
                                    if key_part.strip() == key:
                                        updated_line = f"{key} = {value}\n"
                                        updated = True
                                        break
                        elif ext == 'rasi':
                            for key, value in self.colors.items():
                                if line_stripped.startswith(f"{key}"):
                                    # Handle spaces around ":"
                                    key_part, _, value_part = line_stripped.partition(":")
                                    if key_part.strip() == key:
                                        updated_line = f"{key}: {value};\n"
                                        updated = True
                                        break
                        else:
                            for key, value in self.colors.items():
                                if line_stripped.startswith(f"{key}"):
                                    # Handle spaces around "="
                                    key_part, _, value_part = line_stripped.partition("=")
                                    if key_part.strip() == key:
                                        updated_line = f"{key} = {value}\n"
                                        updated = True
                                        break
                        file.write(updated_line)
                if updated:
                    print(f"Updated colors in {path}")
                else:
                    print(f"No matching keys to update in {path}")
            except Exception as e:
                print(f"Error processing {path}: {e}")


    def set_tool_images(self):
        print("Setting tool images")
        for config_path, image_path in self.tool_images.items():
            config_path = config_path.strip()
            image_path = image_path.strip()
            if not os.path.exists(config_path):
                print(f"File not found: {config_path}")
                continue
            filename = os.path.basename(config_path)
            ext = filename.rsplit('.', 1)[1] if '.' in filename else ''
            try:
                with open(config_path, 'r') as file:
                    lines = file.readlines()
                updated = False
                with open(config_path, 'w') as file:
                    for line in lines:
                        updated_line = line
                        line_stripped = line.strip()
                        if ext == 'rasi':  # Rofi file
                            if line_stripped.startswith("background-image"):
                                # Replace the line with the new image path
                                updated_line = f"\tbackground-image: url(\"{image_path}\", width);\n"
                                updated = True
                        else:  # Default file (e.g., .conf, .ini)
                            if line_stripped.startswith("image_source"):
                                # Replace the line with the new image path
                                key_part, _, value_part = line_stripped.partition("=")
                                if key_part.strip() == "image_source":
                                    updated_line = f"image_source = {image_path}\n"
                                    updated = True
                        file.write(updated_line)
                if updated:
                    print(f"Updated image_source in {config_path}")
                else:
                    print(f"No matching 'image_source' key to update in {config_path}")
            except Exception as e:
                print(f"Error processing {config_path}: {e}")

    def fetch_settings(self):
        print("fetch_settings called")
        self.global_config = configparser.ConfigParser()
        self.global_config.read(f"{self.path_to_config}/theme_manager/config.ini")
        print("Reading global config")
        self.current_theme = self.global_config["DEFAULT"]["SelectedTheme"]
        print(self.current_theme)
        self.tools = self.global_config["DEFAULT"]["Tools"].split(',')
        self.current_theme_config = configparser.ConfigParser()
        self.current_theme_config.read(f"{self.path_to_config}/theme_manager/themes/{self.current_theme}.ini")
        print(f"Current theme file: {self.current_theme}.ini")
        try:
            self.wallpaper = self.current_theme_config["Wallpaper"]["path"]
            print(f"Wallpaper path: {self.wallpaper}")
        except KeyError:
            print("KeyError: 'path' not found in Wallpaper section")
            self.wallpaper = None

        for key, value in self.current_theme_config["Colors"].items():
            self.colors[key] = value
            print(f"Color setting: {key} = {value}")

        if "ToolImages" in self.current_theme_config:
            for config_path, image_path in self.current_theme_config["ToolImages"].items():
                # For safety, strip whitespace
                config_path = config_path.strip()
                image_path = image_path.strip()
                self.tool_images[config_path] = image_path
                print(f"Tool image mapping: {config_path} => {image_path}")

    def set_config(self):
        print("Setting config")
        print(self.tool_images)
        self.set_wallpaper()
        self.set_colors()
        self.set_tool_images()


def main():
    print("Running main function")
    theme = Theme()
    print("Applying theme settings")
    theme.set_config()
    print("Done applying theme settings")


if __name__ == "__main__":
    main()
