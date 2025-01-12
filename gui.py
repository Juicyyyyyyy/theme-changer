import gi
import os
import configparser
from terminal_app import Theme

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf


class ThemeGalleryApp(Gtk.Window):
    def __init__(self, theme_manager):
        super().__init__(title="Theme Gallery")
        self.theme_manager = theme_manager
        self.selected_theme = None  # Keep track of the currently selected theme
        self.selected_event_box = None  # Store the currently selected EventBox
        self.theme_event_boxes = {}  # Maps theme_name -> event_box

        self.set_default_size(800, 600)
        self.set_border_width(10)

        # Load custom CSS for highlighting selected theme
        self.load_css()

        # Vertical box to hold the gallery (top) and the apply button (bottom)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Scrolled window for the gallery
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scrolled_window, True, True, 0)

        # FlowBox to lay out images in a responsive grid
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_max_children_per_line(4)  # Number of images per row
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        scrolled_window.add(self.flowbox)

        # "Apply" button at the bottom
        apply_button = Gtk.Button(label="Apply")
        apply_button.connect("clicked", self.on_apply_clicked)
        vbox.pack_end(apply_button, False, False, 0)

        # Populate gallery with themes
        self.populate_gallery()

    def load_css(self):
        """
        Load a small CSS snippet that defines a .selected-theme style.
        """
        css = b"""
            .selected-theme {
                border: 3px solid #A020F0; /* Vibrant purple border color */
                border-radius: 8px;       /* Smooth rounded corners */
                box-shadow: 0px 4px 8px rgba(160, 32, 240, 0.4); /* Subtle purple shadow */
                transition: all 0.3s ease; /* Smooth transition effect */
            }
            .selected-theme:hover {
                border-color: #DA70D6; /* Lighter purple on hover */
                box-shadow: 0px 6px 12px rgba(218, 112, 214, 0.6); /* Enhanced shadow on hover */
            }
            GtkEventBox {
                padding: 0;
                margin: 0;
            }
        """

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css)

        screen = Gdk.Screen.get_default()
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def populate_gallery(self):
        # Directory containing *.ini theme files
        themes_dir = os.path.join(self.theme_manager.path_to_config, "theme_manager", "themes")

        if not os.path.exists(themes_dir):
            self.show_error_dialog(f"Theme directory not found: {themes_dir}")
            return

        for theme_file in sorted(os.listdir(themes_dir)):
            if theme_file.endswith(".ini"):
                theme_name = os.path.splitext(theme_file)[0]
                config = configparser.ConfigParser()
                config.read(os.path.join(themes_dir, theme_file))

                wallpaper_path = config.get("Wallpaper", "Path", fallback="")
                if wallpaper_path and os.path.exists(wallpaper_path):
                    self.create_theme_widget(theme_name, wallpaper_path)

    def create_theme_widget(self, theme_name, wallpaper_path):
        """
        Creates a widget (image + theme label) for a specific theme.
        Clicking on it will mark the theme as selected (and highlight the border).
        """
        # Outer box for image + label
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        # --- Create a scaled thumbnail preserving aspect ratio ---
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
            filename=wallpaper_path,
            width=200,   # The max width of your thumbnail
            height=200,  # The max height of your thumbnail
            preserve_aspect_ratio=True
        )
        image = Gtk.Image.new_from_pixbuf(pixbuf)

        # Use an AspectFrame to ensure a fixed bounding box (200x200) 
        # and preserve aspect ratio without distorting the image.
        aspect_frame = Gtk.AspectFrame(
            label=None,       # no label
            xalign=0.5,       # center horizontally
            yalign=0.5,       # center vertically
            ratio=1.0,        # target aspect ratio (square)
            obey_child=False  # do not let the child override the frame's size
        )
        aspect_frame.set_size_request(200, 200)
        aspect_frame.add(image)

        # EventBox to capture clicks & allow style changes (border highlight)
        event_box = Gtk.EventBox()
        event_box.add(aspect_frame)
        event_box.connect("button-press-event", self.on_theme_clicked, theme_name)
        box.pack_start(event_box, False, False, 0)

        # Theme name label
        label = Gtk.Label(label=theme_name)
        label.set_justify(Gtk.Justification.CENTER)
        box.pack_start(label, False, False, 0)

        # Keep a reference for later to highlight border
        self.theme_event_boxes[theme_name] = event_box

        # Finally, add the complete box (image + label) to the flowbox
        self.flowbox.add(box)

    def on_theme_clicked(self, widget, event, theme_name):
        """
        Callback for clicking on a theme's image.
        Updates the selected_theme variable and highlights the selected theme's border.
        """
        self.selected_theme = theme_name
        print(f"Selected theme: {self.selected_theme}")

        # Remove highlight from previously selected EventBox
        if self.selected_event_box:
            self.selected_event_box.get_style_context().remove_class("selected-theme")

        # Add highlight to newly selected EventBox
        new_selected = self.theme_event_boxes.get(theme_name)
        if new_selected:
            new_selected.get_style_context().add_class("selected-theme")
            self.selected_event_box = new_selected

    def on_apply_clicked(self, button):
        """
        Applies the currently selected theme (if any).
        """
        if not self.selected_theme:
            self.show_error_dialog("Please select a theme first.")
            return

        # Update the global config with the selected theme
        self.theme_manager.global_config["DEFAULT"]["SelectedTheme"] = self.selected_theme
        with open(os.path.join(self.theme_manager.path_to_config,
                               "theme_manager", "config.ini"), "w") as configfile:
            self.theme_manager.global_config.write(configfile)

        # Now fetch and apply the theme
        self.theme_manager.fetch_settings()
        self.theme_manager.set_config()

        self.show_info_dialog(f"Theme '{self.selected_theme}' applied successfully!")

    def show_error_dialog(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=message,
        )
        dialog.run()
        dialog.destroy()

    def show_info_dialog(self, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=message,
        )
        dialog.run()
        dialog.destroy()


def main():
    theme_manager = Theme()
    app = ThemeGalleryApp(theme_manager)
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()


if __name__ == "__main__":
    main()
