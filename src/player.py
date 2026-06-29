class Player:
    """
        Klassen representerar spalarens ikon på spelplanen
    """
    marker = "@"

    def __init__(self, x, y):
        """
            Placera spelarikonen på spelplanen
        """
        self.pos_x = x
        self.pos_y = y
        self.inventory = []

    # Returnerar spelarens inventarielista
    def get_player_inventory(self):
        return self.inventory

    # Flyttar spelaren. "dx" och "dy" är skillnaden
    def move(self, dx, dy):
        """
        Flyttar spelaren.
        dx = horisontell förflyttning, från vänster till höger
        dy = vertikal förflyttning, uppifrån och ned
        """
        self.pos_x += dx
        self.pos_y += dy

    def can_move(self, x, y, grid):
        """
            Kontrollerar om rutan spelaren går till inte är en vägg.
            Return: Om ej vägg
        """
        new_pos_x = self.pos_x + x
        new_pos_y = self.pos_y + y

        # use existing grid.get() to detect walls
        return grid.get(new_pos_x, new_pos_y) != grid.wall





