import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


class ThemeApp(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Theme Manager")
        self.set_default_size(600, 500)

        # Main layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_top(10)
        main_box.set_margin_bottom(10)
        main_box.set_margin_start(10)
        main_box.set_margin_end(10)
        self.set_child(main_box)

        # Add sections
        self.add_theme_management_section(main_box)
        self.add_separator(main_box)
        self.add_wallpaper_section(main_box)
        self.add_separator(main_box)
        self.add_color_selector_section(main_box)
        self.add_separator(main_box)
        self.add_tools_section(main_box)

    def add_theme_management_section(self, parent):
        """Add the theme management section."""
        header = self.create_section_header("Theme Management")
        parent.append(header)

        theme_frame = Gtk.Frame(label="Manage Themes")
        theme_frame.set_margin_top(5)
        theme_frame.set_margin_bottom(5)

        theme_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        theme_combo = Gtk.ComboBoxText()
        theme_combo.append("default", "Default Theme")
        theme_combo.append("dark", "Dark Theme")
        theme_combo.append("custom", "Custom Theme")
        theme_combo.set_active(0)

        create_theme_button = Gtk.Button(label="Create New Theme")
        theme_box.append(theme_combo)
        theme_box.append(create_theme_button)
        theme_frame.set_child(theme_box)

        parent.append(theme_frame)

    def add_wallpaper_section(self, parent):
        """Add the wallpaper section."""
        header = self.create_section_header("Associated Wallpaper")
        parent.append(header)

        wallpaper_frame = Gtk.Frame()
        wallpaper_frame.set_margin_bottom(5)

        wallpaper_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        wallpaper_button = Gtk.Button(label="Select Wallpaper")
        wallpaper_preview = Gtk.Label(label="(No wallpaper selected)")
        wallpaper_box.append(wallpaper_button)
        wallpaper_box.append(wallpaper_preview)
        wallpaper_frame.set_child(wallpaper_box)

        parent.append(wallpaper_frame)

    def add_color_selector_section(self, parent):
        """Add the color selector section."""
        header = self.create_section_header("Theme Colors")
        parent.append(header)

        color_grid = Gtk.Grid()
        color_grid.set_column_spacing(10)
        color_grid.set_row_spacing(5)

        # Create buttons and labels for colors
        primary_button = Gtk.Button(label="Select Primary Color")
        secondary_button = Gtk.Button(label="Select Secondary Color")
        accent_button = Gtk.Button(label="Select Accent Color")

        primary_preview = Gtk.Label(label="(None)")
        secondary_preview = Gtk.Label(label="(None)")
        accent_preview = Gtk.Label(label="(None)")

        # Attach widgets to the grid
        color_grid.attach(Gtk.Label(label="Primary Color:"), 0, 0, 1, 1)
        color_grid.attach(primary_button, 1, 0, 1, 1)
        color_grid.attach(primary_preview, 2, 0, 1, 1)

        color_grid.attach(Gtk.Label(label="Secondary Color:"), 0, 1, 1, 1)
        color_grid.attach(secondary_button, 1, 1, 1, 1)
        color_grid.attach(secondary_preview, 2, 1, 1, 1)

        color_grid.attach(Gtk.Label(label="Accent Color:"), 0, 2, 1, 1)
        color_grid.attach(accent_button, 1, 2, 1, 1)
        color_grid.attach(accent_preview, 2, 2, 1, 1)

        color_frame.set_child(color_grid)
        parent.append(color_frame)

    def add_tools_section(self, parent):
        """Add the tools section."""
        header = self.create_section_header("Tools to Update")
        parent.append(header)

        tools_frame = Gtk.Frame()
        tools_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        gtk_check = Gtk.CheckButton(label="GTK Theme")
        rofi_check = Gtk.CheckButton(label="Rofi Theme")
        terminal_check = Gtk.CheckButton(label="Terminal Colors")

        tools_box.append(gtk_check)
        tools_box.append(rofi_check)
        tools_box.append(terminal_check)
        tools_frame.set_child(tools_box)

        parent.append(tools_frame)

    def add_separator(self, parent):
        """Add a separator between sections."""
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        parent.append(separator)

    def create_section_header(self, title):
        """Create a styled section header."""
        header = Gtk.Label(label=title)
        header.set_xalign(0)
        header.set_margin_bottom(5)
        header.set_margin_top(10)
        return header


class ThemeManagerApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.theme_manager")

    def do_activate(self):
        win = ThemeApp(self)
        win.present()


if __name__ == "__main__":
    app = ThemeManagerApp()
    app.run()
