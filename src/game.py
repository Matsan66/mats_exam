from src.game_state import GameState
from src import pickups
import msvcrt


class Game():
    """
    Game startar och kontrollerar spelet Fruit Loopd
    """
    def __init__(self, game_state):
        self.game_state = game_state

    def start(self):
        """
        Kontrollerar spelets huvudloop
        """
        command = "a"
        # Loopa tills användaren trycker Q eller X.
        while not command.casefold() in ["q", "x"]:
            self.game_state.game_grid.print_status(self.game_state.game_grid, self.game_state)

            print("Använd WASD för att flytta, Q/X för att avsluta. ")

            pressed_key = msvcrt.getch()
            if pressed_key in (b'\x00', b'\xe0'):  # Ignore special characters
                msvcrt.getch()
                continue
            command = pressed_key.decode().casefold()

            self.act_on_player_input(command)

        # Hit kommer vi när while-loopen slutar
        print("\nTack för att su spelade Fruit Loop!")

    def act_on_player_input(self, command):
        """
        Analyserar spelarens kommandon och exekverar dem
        """
        maybe_item = None

        directions = {
            "d": (1, 0),
            "a": (-1, 0),
            "w": (0, -1),
            "s": (0, 1)
        }

        # Om spelaren vill se inventory
        if command == "i":
            self.game_state.display_inventory()
            return

        # Om kommandot inte är en riktning
        if command not in directions:
            return

        dx, dy = directions[command]

        # Kontrollera att rutan att går till inte är en vägg och om positionen har en item.
        if self.game_state.player.can_move(dx, dy, self.game_state.game_grid):
            maybe_item = self.game_state.game_grid.get(
                self.game_state.player.pos_x + dx,
                self.game_state.player.pos_y + dy
            )

            self.game_state.player.move(dx, dy) # Flytta spelarikonen
            self.game_state.score -= 1 # Golvet är lava - 1poäng för varje steg

        if isinstance(maybe_item, pickups.Item):
            # we found something
            self.game_state.score += maybe_item.value # Poäng för hittat item
            print(f"Du har hittat en {maybe_item.name}, +{maybe_item.value} poäng.")
            self.game_state.inventory.append(maybe_item) # Lägg till hittat item i Inventory
            self.game_state.game_grid.clear(self.game_state.player.pos_x, self.game_state.player.pos_y) # Töm rutan



# __name__ skapas av Python och sätts till "__main__" om man startar game.py
# direkt. Detta är för att undvika att start-funktionen körs om man importerar
# saker från game.py i en annan fil, till exempel vid testning.
if __name__ == "__main__":
    game_state = GameState()
    game = Game(game_state)
    game.start()