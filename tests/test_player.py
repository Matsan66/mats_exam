import pytest
import game_state
from src.player import Player
from pickups import Item

"""
Funktionella krav: 
Som spelare vill jag kunna se vad jag har i min inventarielista så att jag kan använda mina saker

Icke Funktionella krav:
Då en spelare skapas ska inventarielistan vara tom
Listan som returneras ska vara identisk ned den lagrade listan
Då inventarielistan returneras ska varje item utgöra en indexposition
Då inventarielistan returneras ska den innehålla samma items som lagts i listan

"""


def test_get_player_inventory():
    """
    Testar att get_player_inventory() returnerar en spelares inventarielista
    med korrekt innehåll, längd och items.
    """

    # Skapa en spelare
    tested_player = Player(18, 5)

    # Skapa en inventarielista för spelaren med default "values"
    tested_player.inventory = [
        Item("spade", symbol="!"),
        Item("morot", symbol="?"),
        Item("äpple", symbol="?"),
        Item("fälla", symbol=".")
    ]

    result = tested_player.get_player_inventory()

    assert result == tested_player.inventory
    assert len(result) == 4
    assert result[0].item_name == "spade"
    assert result[1].item_name == "morot"
    assert result[2].item_name == "äpple"
    assert result[3].item_name == "fälla"

# -------------------------------------------------------------------------------

def test_get_player_inventory_empty():
    """
        Testar att get_player_inventory() returnerar en tom spelares inventarielista
        då spelaren skapas.
    """
    tested_player = Player(18, 5)

    assert tested_player.get_player_inventory() == []
