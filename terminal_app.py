from typing import List, Dict
import configparser
import subprocess
import os


class Theme:
    def __init__(self):
        self.current_theme: str = None
        self.wallpaper: str = None
        self.tools: List[str] = None
        self.colors: Dict[str, str] = {}
        user = os.environ.get("USER")
        self.path_to_config: str = f"/home/{user}/.config"
        self.current_theme_config = None
        self.global_config = None

        if (not os.path.exists(f"{self.path_to_config}/theme_manager")):
            self.create_base_config()

        self.fetch_settings()

    def create_base_config(self):
        path = f"{self.path_to_config}/theme_manager"
        try:
            os.mkdir(path)
        except PermissionError:
            print(f"Permission denied: Unable to create '{path}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

        config = configparser.ConfigParser()
        config["DEFAULT"] = {
            "SelectedTheme": "theme_example",
            "Tools": "/home/yourname/.config/example/config, /home/yourname/.config/example_2/config"
        }

        self.create_example_theme()

    def create_example_theme(self):
        config = configparser.ConfigParser()
        path = f"{self.path_to_config}/theme_manager/themes/theme_example.ini"
        try:
            with open(path, "w") as f:
                config.write(f)
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

    def set_wallpaper(self):
        command = "feh --bg-center {}".format(self.wallpaper)
        try:
            subprocess.run(command, capture_output=True, check=True, text=True)
        except subprocess.CalledProcessError as e:
            print("Error dectected: {}".format(e.stderr))

    def set_colors(self):
        for path in self.tools:
            path = path.strip()
            if not os.path.exists(path):
                print(f"File not found: {path}")
                continue

            with open(path, 'r') as file:
                lines = file.readlines()

            with open(path, 'w') as file:
                for line in lines:
                    updated_line = line
                    for key, value in self.colors.items():
                        if line.strip().startswith(f"{key}="):
                            updated_line = f"{key}={value}\n"
                            break
                    file.write(updated_line)

    def fetch_settings(self):
        self.global_config = configparser.ConfigParser()
        self.global_config.read(f"{self.path_to_config}/theme_manager/config.ini")
        self.current_theme = self.global_config["SelectedTheme"]
        self.tools = self.global_config["Tools"].split(',')

        self.current_theme_config = configparser.ConfigParser()
        self.current_theme_config.sections()
        self.current_theme_config.read(f"{self.path_to_config}/theme_manager/themes/{self.current_theme}.ini")
        self.wallpaper = self.current_theme_config["Wallpaper"]["Path"]
        for key, value in self.current_theme_config["Colors"].items():
            self.colors[key] = value
        return

    def set_config(self):
        self.set_wallpaper()
        self.set_colors()
