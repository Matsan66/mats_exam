from src.pickups import Item
from src.game_state import GameState
from src import pickups
import msvcrt


class Game():
    """
    Game startar och kontrollerar spelet Fruit Loopd
    """
    def __init__(self, game_state):
        self.game_state = game_state
        self.game_over = False
        self.grace_period_counter = 0
        self.fertile_soil_counter = 0
        self.original_fruits = 8
        self.exit_open = False

    def start(self):
        """
        Kontrollerar spelets huvudloop
        """
        command = "a"
        # Loopa tills användaren trycker Q eller X eller game_over sätts till True.
        while not self.game_over and command.casefold() not in ["q", "x"]:
            self.game_state.game_grid.print_status(self.game_state.game_grid, self.game_state)

            print("Använd WASD för att flytta, Q/X för att avsluta. ")

            pressed_key = msvcrt.getch()
            if pressed_key in (b'\x00', b'\xe0'):  # Ignore special characters
                msvcrt.getch()
                continue
            command = pressed_key.decode().casefold()

            self.act_on_player_input(command)

        # Hit kommer vi när while-loopen slutar
        print("\nTack för att du spelade Fruit Loop!")

    def disarm_trap(self):
        """
        Tar bort en fälla från spelplan när spelaren trycker "t" och aktuell
        ruta innehåller en fälla.
        """
        x = self.game_state.player.pos_x
        y = self.game_state.player.pos_y

        grid_spot_status = self.game_state.game_grid.get(x, y)

        if isinstance(grid_spot_status, pickups.Item) and grid_spot_status.name == "fälla":
            self.game_state.game_grid.clear(x, y)
            return True
        return False


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

        # Om spelaren vill se inventarielistan
        if command == "i":
            player_inventory = self.game_state.player.get_player_inventory()

            for item in player_inventory:
                if item == player_inventory[-1]:
                    print(f"{item.item_name}.")
                else:
                    print(f"{item.item_name}, ", end="")
            print()
            return

        # Om spelaren försöker desarmera en fälla
        if command == "t":
            disarm_result = self.disarm_trap()

            if disarm_result:
                print("Du har desarmerat en fälla!")
            else:
                print("Ingen fälla här!")
            return

        # Om kommandot inte är en riktning
        if command not in directions:
            return

        dx, dy = directions[command]

        # Om inte en vägg eller om spelaren har en spade. Kontrollera om det finns item på rutan.
        if self.game_state.player.can_move(dx, dy, self.game_state.game_grid) or any(item.name == "spade" for item in self.game_state.player.inventory):
            maybe_item = self.game_state.game_grid.get(
                self.game_state.player.pos_x + dx,
                self.game_state.player.pos_y + dy
            )

            # -----------------------------------------------------
            # SPELAREN HAR EN SPADE OCH ANVÄNDER DEN PÅ EN VÄGG
            # -----------------------------------------------------

            # Om rutan att gå till var en vägg men spelaren har spade
            if not self.game_state.player.can_move(dx, dy, self.game_state.game_grid):

                # Ta bort spaden ur inventory
                for item in self.game_state.player.inventory:
                    if item.name == "spade":
                        self.game_state.player.inventory.remove(item)
                        break

                # Töm rutan spelaren gått till (väggen)
                self.game_state.game_grid.set(self.game_state.player.pos_x + dx, self.game_state.player.pos_y + dy, self.game_state.game_grid.empty)

            # -----------------------------------------------------
            # FLYTTA SPELARIKONEN, HANTERA BÖRDIG JORD och EXIT
            # -----------------------------------------------------
            self.game_state.player.move(dx, dy)

            self.fertile_soil_counter += 1

            if self.fertile_soil_counter == 25:
                fruits =  ["banan", "mango", "persika", "nektarin", "apelsin", "clementin", "kiwi", "citron", "plommon", "päron"]
                if len(fruits) > 0:
                    pickups.add_extra_fruit(game_state.game_grid, Item(fruits[0], value = 20, symbol = "o"))
                    self.fertile_soil_counter = 0
                    fruits.remove(fruits[0])
                else:
                    print("Inga fler frukter att lägga till")

            x = self.game_state.player.pos_x
            y = self.game_state.player.pos_y
            grid_spot_status = self.game_state.game_grid.get(x, y)

            if grid_spot_status == "E" and not self.exit_open:
                print("Du står på utgången, men har inte tagit alla ursprungliga frukter!")
            elif grid_spot_status == "E" and self.exit_open:
                print("Du har lämnat spelet.")
                self.game_over = True


            # -----------------------------------------------------
            # GOLVET ÄR LAVA OCH GRACE PERIOD KONTROLL
            # -----------------------------------------------------

            if self.grace_period_counter == 0:
                self.game_state.score -= 1 # Golvet är lava - 1 poäng för varje steg
            else:
                self.grace_period_counter -= 1
                print(f"Grace period = {self.grace_period_counter}")

        if isinstance(maybe_item, pickups.Item):
            # En inventraie item är hittad och grace period startar
            if maybe_item.name != "kista" and maybe_item.name != "fälla":
                print("Grace period är aktiverad")
                self.grace_period_counter = 5

            # -----------------------------------------------------
            # HANTERA HITTAD ITEM SOM INTE ÄR EN KISTA
            # -----------------------------------------------------
            if maybe_item.name != "kista":
                self.game_state.score += maybe_item.value # Poäng för hittat item utom kista

                if maybe_item.value > 0:
                    print(f"Du har hittat en {maybe_item.name}, +{maybe_item.value} poäng.")  # Positiv poäng
                else:
                    print(f"Du har hittat en {maybe_item.name}, {maybe_item.value} poäng.")  # Negativ poäng

                # -----------------------------------------------------
                # HANTERA ÖPPPNING AV EXIT DÅ ALLA ORIGINAL FRUKTER HITTATS
                # -----------------------------------------------------

                if maybe_item.symbol == "?":
                    self.original_fruits -= 1
                    if self.original_fruits == 0:
                        self.exit_open = True

            # -----------------------------------------------------
            # HANTERA HITTAD ITEM SOM ÄR EN KISTA OCH SPELAREN HAR EN NYCKEL
            # ----------------------------------------------------
            elif maybe_item.name == "kista" and any(item.name == "nyckel" for item in self.game_state.player.inventory):
                self.game_state.score += maybe_item.value  # Poäng för kista med nyckel
                print(f"Du låste upp kistan med din nyckel! +{maybe_item.value} poäng.")

                # Ta bort nyckeln från inventarielistan då den är förbrukad
                for item in self.game_state.player.inventory:
                    if item.name == "nyckel":
                        self.game_state.player.inventory.remove(item)

                # Ta bort kistan från spelplanen då den är öppnad
                self.game_state.game_grid.clear(self.game_state.player.pos_x, self.game_state.player.pos_y)

            # -----------------------------------------------------
            # HANTERA HITTAD ITEM SOM ÄR EN KISTA DÅ SPELAREN INTE HAR EN NYCKEL
            # ----------------------------------------------------
            elif maybe_item.name == "kista":
                print("Kistan är låst! Du måste hitta en nyckel först.")

            # -----------------------------------------------------
            # HANTERA HITTAD ITEM SOM INTE INVOLVERAR KISTA ELLER FÄLLA
            # ----------------------------------------------------
            # Cleara rutan från item och lägg item i Inventory om inte item är en fälla eller kista
            if maybe_item.name != "fälla" and maybe_item.name != "kista":
                self.game_state.player.inventory.append(maybe_item)  # Lägg till hittat item i Inventory
                self.game_state.game_grid.clear(self.game_state.player.pos_x, self.game_state.player.pos_y) # Töm rutan


# __name__ skapas av Python och sätts till "__main__" om man startar game.py
# direkt. Detta är för att undvika att start-funktionen körs om man importerar
# saker från game.py i en annan fil, till exempel vid testning.
if __name__ == "__main__":
    game_state = GameState()
    game = Game(game_state)
    game.start()