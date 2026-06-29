
class Item:
    """Representerar saker man kan plocka upp."""
    def __init__(self, name, value=10, symbol="?"):
        self.name = name
        self.value = value
        self.symbol = symbol

    @property
    def item_name(self):
        return self.name

    def __str__(self):
        return self.symbol


pickups = [
    Item("spade", value = 0, symbol = "!"), Item("fälla", value = -10, symbol = "."), Item("morot"),
    Item("äpple", value = 20), Item("jordgubb"), Item("körsbär"), Item("vattenmelon", value = 20),
    Item("rädisa"), Item("gurka"), Item("köttbulle"), Item("nyckel", value = 0, symbol = "⌂"),
    Item("kista", value = 100, symbol = "$")]


def randomize(grid):
    for item in pickups:
        while True:
            # slumpa en position tills vi hittar en som är ledig
            x = grid.get_random_x()
            y = grid.get_random_y()
            if grid.is_empty(x, y):
                grid.set(x, y, item)
                break  # avbryt while-loopen, fortsätt med nästa varv i for-loopen

def add_extra_fruit(grid, item):
    """
    Lägger till en item på en slumpmässig plats på spelplan
    """
    while True:
        # slumpa en position tills vi hittar en som är ledig
        x = grid.get_random_x()
        y = grid.get_random_y()
        if grid.is_empty(x, y):
            grid.set(x, y, item)
            break  # avbryt while-loopen, fortsätt med nästa varv i for-loopen


