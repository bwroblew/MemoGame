import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

from GameModel import GameModel
import Settings


class GameViewGtk(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=Settings.GAME_TITLE)
        self.game = GameModel()
        self.set_default_size(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT + Settings.GTK_EXTRA_FOOTER)
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.main_box)
        self.initialize_menu()
        self.initialize_board()
        self.add_start_button()
        self.add_points_view()
        self.load_css_layout()
        self.start_game()

    def initialize_board(self):
        self.frame_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.cards_layout = Gtk.Grid()
        self.cards_layout.set_size_request(Settings.BOARD_WIDTH, Settings.BOARD_HEIGHT)
        self.frame_box.pack_start(self.cards_layout, False, False, 0)
        self.main_box.pack_start(self.frame_box, False, False, 0)

        row_size, col_size = Settings.CARDS_LAYOUT
        for card_id in range(row_size * col_size):
            button = Gtk.Button()
            button.set_hexpand(True)
            button.set_vexpand(True)
            x, y = self.card_id_to_coord(card_id)
            button.set_name("card_reverse")
            button.set_label(Settings.REVERSE_CARD_MARK)
            button.connect("pressed", self.card_clicked)
            self.cards_layout.attach(button, x, y, 1, 1)

    def initialize_menu(self):
        menu_bar = Gtk.MenuBar()
        menu = Gtk.Menu()
        info_item = Gtk.MenuItem(Settings.MENU_INFO_TITLE)
        info_item.set_submenu(menu)
        help_item = Gtk.MenuItem(Settings.MENU_HELP_TITLE)
        help_item.connect("activate", self.help_display)
        menu.append(help_item)
        menu_bar.append(info_item)
        quit_item = Gtk.MenuItem(Settings.MENU_QUIT_TITLE)
        def destroy(widget):
            Gtk.main_quit()
        quit_item.connect("activate", destroy)
        menu_bar.append(quit_item)
        menu_box = Gtk.VBox()
        menu_box.pack_start(menu_bar, False, False, 0)
        self.main_box.pack_start(menu_box, True, True, 0)

    def help_display(self, widget):
        help_dialog = Gtk.MessageDialog(
            self,
            0,
            Gtk.MessageType.OTHER,
            Gtk.ButtonsType.OK,
            Settings.HELP_TITLE,
        )
        help_dialog.format_secondary_text(Settings.HELP_TEXT)
        def dialog_response(widget, response_id):
            widget.destroy()
        help_dialog.connect("response", dialog_response)
        help_dialog.show()

    def add_start_button(self):
        self.start_button = Gtk.Button(Settings.NEW_GAME_BUTTON_TEXT,)
        self.start_button.connect("clicked", self.start_clicked)
        self.start_button.set_name("start_button")
        self.main_box.pack_start(self.start_button, False, False, 0)

    def add_points_view(self):
        points_layout = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True)
        self.points_label_key = Gtk.Label(Settings.POINTS_LABEL)
        self.points_label_key.set_name("points_label")
        self.points_label_value = Gtk.Label("0")
        self.points_label_value.set_name("points_label")
        points_layout.add(self.points_label_key)
        points_layout.add(self.points_label_value)
        self.main_box.pack_start(points_layout, False, False, 0)

    def start_game(self):
        self.start_button.set_label(Settings.NEW_GAME_BUTTON_TEXT)
        self.game.restart_game()
        self.clear_board()
        self.points_label_value.set_label(str(self.game.get_points()))

    def start_clicked(self, btn):
        self.start_game()

    def card_clicked(self, btn):
        if not self.game.is_game_runnning():
            return

        x = self.cards_layout.child_get_property(btn, "left-attach")
        y = self.cards_layout.child_get_property(btn, "top-attach")
        if self.game.was_collected(x, y):
            return
        
        self.game.select_card(x, y)
        visible_cards = self.game.get_visible_cards()
        self.points_label_value.set_label(str(self.game.get_points()))
        self.clear_board()
        self.show_cards(visible_cards)
        
        if self.game.is_game_finished():
            self.start_game()
        
    def clear_board(self):
        row_size, col_size = Settings.CARDS_LAYOUT
        for card_id in range(row_size * col_size):
            x, y = self.card_id_to_coord(card_id)
            button = self.cards_layout.get_child_at(x, y)
            if self.game.was_collected(x, y):
                button.set_name("collected_card")
            else:
                button.set_name("card_reverse")
            button.set_label(Settings.REVERSE_CARD_MARK)

    def show_cards(self, cards):
        for card in cards:
            x, y = card
            button = self.cards_layout.get_child_at(x, y)
            button.set_name("visible_card")
            button.set_label(str(self.game.get_card_sign(x, y)))

    def card_id_to_coord(self, number):
        row_size, _ = Settings.CARDS_LAYOUT
        return number % row_size, number // row_size

    def coord_to_card_id(self, x, y):
        row_size, _ = Settings.CARDS_LAYOUT
        return y * row_size + x

    def load_css_layout(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(Settings.Gtk.CSS_LAYOUT)
        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)