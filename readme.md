# Theme Manager

**Theme Manager** is a tool that enables dynamic theme switching by recognizing predefined variables in configuration files. It allows you to update colors or images across multiple tools by editing a single theme file.

---

### Theme Configuration
- Define variables in `~/.config/theme_manager/themes/<yourtheme>.ini`.
- Example:
  ```ini
  [Colors]
  background=#1F1F28
  ```
- The tool searches for matching variables in the specified configuration paths and replaces them. You can add any variable you want, you do not need to use the default ones.

### Global Configuration
- Set the active theme and config paths where you want the variables to be updated in `~/.config/theme_manager/config.ini`.
- Example:
  ```ini
  [DEFAULT]
  SelectedTheme=yourtheme
  Tools=/path/to/config1, /path/to/config2
  ```

### Image Updates (Experimental)
- Specify image paths in the theme file:
  ```ini
  [ToolImages]
  /path/to/tool_config=/path/to/image
  ```
For the moment I only tried it with rofi and neofetch.

---

## Installation

1. **Clone the repository**

2. **Install dependencies:**
- gtk, pil, feh

3. **Run the GUI:**
   ```bash
   python3 gui.py
   ```
Once you run the tool a default configuration will be created in ~/.config/theme_manager/

4. **Set permissions:**
   If needed, grant read and write permissions:
   ```bash
   chmod +rw <path_to_configs>
   ```

Make sure to backup your configuration before using the tool since it is pretty experimental.

---

## Example Theme File
```ini
[Colors]
background=#1F1F28
text=#C0C0C0

[Wallpaper]
Path=/path/to/wallpaper.jpg

[ToolImages]
/path/to/tool_config=/path/to/image
```

## Example Theme File
```ini
[DEFAULT]
selectedtheme=monochrome
tools=/path/to/polybar/config, /path/to/rofi/config
``` 
