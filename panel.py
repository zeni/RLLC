import tcod


class Panel:
    """
    A panel on main consol
    """

    def __init__(self, x, y, w, h, name, color=tcod.black):
        self.x = x
        self.y = y
        self.name=name
        self.con = tcod.console_new(w, h)
        self.con.default_bg=color
        self.con.default_fg=tcod.white

    def draw(self,message_log,info):
        tcod.console_set_default_foreground(self.con, tcod.white)
        tcod.console_clear(self.con)
        self.con.hline(0,0,self.con.width)
        self.con.hline(0,self.con.height,self.con.width)
        self.con.vline(0,0,self.con.height)
        self.con.vline(self.con.width,0,self.con.height)
        if self.name=='panel':
            tcod.console_set_default_foreground(self.con, tcod.light_gray)
            tcod.console_print_ex(self.con, message_log.x, 0, tcod.BKGND_NONE, tcod.LEFT, info)
            # Print the game messages, one line at a time
            y = 1
            for message in message_log.messages:
                tcod.console_set_default_foreground(self.con, message.color)
                tcod.console_print_ex(self.con, message_log.x, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
                y += 1
        tcod.console_blit(self.con, 0, 0, self.con.width,
                          self.con.height, 0, self.x, self.y)
