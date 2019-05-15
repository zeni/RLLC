import tcod


class Panel:
    """
    A panel on main consol
    """

    def __init__(self, x, y, w, h, color=tcod.black):
        self.x = x
        self.y = y
        self.con = tcod.console_new(w, h)
        self.con.default_bg=color
        self.con.default_fg=tcod.white

    def draw(self):
        #tcod.console_clear(self.con)
        self.con.hline(0,0,self.con.width)
        self.con.hline(0,self.con.height,self.con.width)
        self.con.vline(0,0,self.con.height)
        self.con.vline(self.con.width,0,self.con.height)
        tcod.console_blit(self.con, 0, 0, self.con.width,
                          self.con.height, 0, self.x, self.y)
