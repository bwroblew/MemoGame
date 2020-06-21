import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from GameViewGtk import GameViewGtk

if __name__ == '__main__':
    game_view = GameViewGtk()
    game_view.connect("destroy", Gtk.main_quit)
    game_view.show_all()
    Gtk.main()