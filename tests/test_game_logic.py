import pytest
from src.game_state import GameState
from src.game import Game
from src.pickups import Item

"""
Funktionella krav: 
Som spelare vill jag kunna använda en spade jag hittat så att jag kan ta bort en vägg
Om jag som spelare hittar en fälla vill jag kunna desarmera den så att jag inte går på den igen

Icke Funktionella krav:
Då spelaren använder spaden ska den tas bort från inventarielistan
Då spelaren använder en spade för att ta bort en vägg ska spelaren kunna flytta till väggens position
Då spaden använts på en vägg ska väggens position på spalplanen bli tom

Då spelaren står på en fälla och använder kommandot "t" ska fällan ersättas med en tom ruta
"""

def test_spade_remove_walls():
    """
    Testar att spelaren kan flytta till positionen för en vägg om det finns en
    spade i inventarielistan. Testar att spaden tas bort från listan och att
    väggens position på spelplanen görs tom.
    """

    # Skapa ett nytt spel
    game_state = GameState()
    game = Game(game_state)

    # Skapa en ny spade
    new_spade = Item("spade", value = 0, symbol = "!")

    # Lägg till spaden i spelarens inventarielista
    game.game_state.player.inventory.append(new_spade)

    # Placera en vägg till höger om spelaren
    player_start_position_x = game.game_state.player.pos_x
    player_start_position_y = game.game_state.player.pos_y

    game.game_state.game_grid.set(player_start_position_x + 1,
                                  player_start_position_y,
                                  game.game_state.game_grid.wall)

    # Flytta spelaren ett steg till höger
    game.act_on_player_input("d")

    # Kontrollera att spaden försvunnit ur spelaren invetarielista
    assert new_spade not in game.game_state.player.inventory

    # Kontrollera att spelarem lyckats flytta till positionen där väggen var tidigare
    assert game.game_state.player.pos_x == player_start_position_x + 1

    # Kontrollera att väggen ersatts med en "tom" ruta
    assert game.game_state.game_grid.get(player_start_position_x + 1, player_start_position_y) == game.game_state.game_grid.empty

# -------------------------------------------------------------------------------

def test_disarm_trap():

    # Skapa ett nytt spel
    game_state = GameState()
    game = Game(game_state)

    # Skapa en ny fälla
    new_trap = Item("trap", value = -10, symbol = ".")






