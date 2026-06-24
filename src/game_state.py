from src.grid import Grid
from src.player import Player
from src import pickups

class GameState:
    """Samla spelets variabler i en klass."""
    def __init__(self):
        self.player = Player(18, 5)
        self.score = 0
        self.inventory = []

        self.game_grid = Grid()
        self.game_grid.set_player(self.player)
        self.game_grid.make_walls()
        self.game_grid.make_obstacle_walls()
        pickups.randomize(self.game_grid)

    def display_inventory(self):
        """
            Skriver ut innehållet i spelaren inventory
        """
        print("\nDin Inventory:")
        for item in self.inventory:
            if item == self.inventory[-1]:
                print(f"{item.item_name}.")
            else:
                print(f"{item.item_name}, ", end = "")
        print()