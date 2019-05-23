import tcod as libtcod

from constants import SCREEN_HEIGHT, SCREEN_WIDTH, CAMERA_WIDTH, CAMERA_HEIGHT

def menu(con, options, width):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')
    # calculate total height for the header (after auto-wrap) and one line per option
    #header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options)+1
    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height+1)
    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    #libtcod.console_print_rect_ex(window, 1, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)
    libtcod.console_print_frame(window, 0, 0, width, height+1, fmt="Inventory")
    # print all the options
    y = 1
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 1, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1
    # blit the contents of "window" to the root console
    x = int(CAMERA_WIDTH / 2 - width / 2)
    y = int(CAMERA_HEIGHT / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height+1, 0, x, y, 1.0, 0.7)

def inventory_menu(con, inventory, inventory_width):
    # show a menu with each item of the inventory as an option
    if len(inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory.items]
    menu(con, options, inventory_width)

def main_menu(options, width,title):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')
    height = len(options)+1
    window = libtcod.console_new(width, height+1)
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_frame(window, 0, 0, width, height+1, fmt=title)
    y = 1
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        #libtcod.console_set_default_background(window, libtcod.red)
        libtcod.console_print_ex(window, 1, y, libtcod.BKGND_OVERLAY, libtcod.LEFT, text)
        y += 1
        letter_index += 1
    x = int(SCREEN_WIDTH / 2 - width / 2)
    y = int(SCREEN_HEIGHT / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height+1, 0, x, y, 1.0, 0.7)