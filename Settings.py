GAME_TITLE = "Liczbowe Memory"

REVERSE_CARD_MARK = "X"

CARDS_LAYOUT = (8, 4)
CARD_SIZE = (60, 100)
CARD_REVERSE_COLOR = "green"
COLLECTED_CARD_COLOR = "red"
VISIBLE_CARD_COLOR = "white"

FOOTER_HEIGHT = 100
MARGIN = 25

BOARD_WIDTH = CARD_SIZE[0] * CARDS_LAYOUT[0]
BOARD_HEIGHT = CARD_SIZE[1] * CARDS_LAYOUT[1]

WINDOW_WIDTH = BOARD_WIDTH + 2 * MARGIN
WINDOW_HEIGHT = BOARD_HEIGHT + FOOTER_HEIGHT + 2 * MARGIN

NEW_GAME_BUTTON_TEXT = "Rozpocznij nową grę!"
POINTS_LABEL = "Znalezione pary:"

MENU_INFO_TITLE = "Informacje"
MENU_HELP_TITLE = "Pomoc"
MENU_QUIT_TITLE = "Wyjdź"
HELP_TITLE = "Pomoc"
HELP_TEXT = "Zdobywaj punkty poprzez odkrywanie i łączenie w pary kart z takimi samymi liczbami!"\
        " Gra ma na celu trening pamięci i koncentracji, dlatego nie jest w niej liczony czas!"\
        " Nie spiesz się! Gdy połączysz ze sobą wszystie karty, gra rozpocznie się ponownie."

class Gtk:
    CSS_LAYOUT_TEXT = """
            
            #start_button {
                border: 2px solid gray;
                background: green;
                color: white;
                margin: 0px 10px 0px 10px;
            }
            
            #points_label {
                border: 2px solid gray;
                background: green;
                color: white;
                margin: 10px;
            }

            #help_label {
                border: 2px solid gray;
                padding: 0 15px;
                background: gray;
                color: white;
                font-family: Arial;
                font-size: 15px;
                margin: 10px;
            }
            
            #visible_card {
                background: %s;
                color: black;
                border-style: solid;
                border-color: black;
                border-width: 1px;
            }

            #card_reverse {
                background: %s;
                color: black;
                border-style: solid;
                border-color: black;
                border-width: 1px;
            }
            
            #collected_card {
                background: %s;
                color: black;
                border-style: solid;
                border-color: black;
                border-width: 1px;
            }
            """ % (VISIBLE_CARD_COLOR, CARD_REVERSE_COLOR, COLLECTED_CARD_COLOR)

    CSS_LAYOUT = str.encode(CSS_LAYOUT_TEXT)

class Qt:
    HELP_STYLE = """ 
        border: 2px solid gray;
        padding: 0 15px;
        background: gray;
        color: white;
        """

    POINTS_STYLE = """ 
        text-align: center;
        border: 2px solid gray;
        background: green;
        color: white;
        """

    START_BUTTON_STYLE = """ 
        border: 2px solid gray;
        background: green;
        color: white;
        """

    REVERSE_CARD_STYLE = "background-color: {}".format(CARD_REVERSE_COLOR)
    COLLECTED_CARD_STYLE = "background-color: {}".format(COLLECTED_CARD_COLOR)
    VISIBLE_CARD_STYLE = "background-color: {}".format(VISIBLE_CARD_COLOR)