"""CSC111 Project 1: Text Adventure Game - Game Entities

Instructions (READ THIS FIRST!)
===============================

This Python module contains the entity classes for Project 1, to be imported and used by
 the `adventure` module.
 Please consult the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Player:
    _inventory: list[str] # encapsulation
    current_weight: float
    score: int
    #ADDED JAN 26 and JAN 27
    def add_item(self, item_to_be_added: str) -> None:
        self._inventory.append(item_to_be_added)


    def remove_item(self, item_to_be_removed: str) -> None:
        self._inventory.remove(item_to_be_removed)


    def get_inventory(self) -> list[str]: #used or not?
        return self._inventory


    def display_inventory(self) -> None:
        print("Your inventory has items")
        for item in self._inventory:
            print("- " + item)



@dataclass
class Location:
    """A location in our text adventure game world.

    Instance Attributes:
        - # TODO Describe each instance attribute here

    Representation Invariants:
        - # TODO Describe any necessary representation invariants
    """

    # This is just a suggested starter class for Location.
    # You may change/add parameters and the data available for each Location object as you see fit.
    #
    # The only thing you must NOT change is the name of this class: Location.
    # All locations in your game MUST be represented as an instance of this class.

    id_num: int
    name: str
    brief_description: str
    long_description: str
    available_commands: dict[str, int]
    items: list[str]
    visited: bool

    def __init__(self, location_id, name, brief_description, long_description, available_commands, items,
                 visited=False) -> None:
        """Initialize a new location.

        # TODO Add more details here about the initialization if needed
        """

        self.id_num = location_id
        self.name = name
        self.brief_description = brief_description
        self.long_description = long_description
        self.available_commands = available_commands
        self.items = items
        self.visited = visited


@dataclass
class Puzzle:
    id_puzzle: int
    description: str


@dataclass
class LogicPuzzle(Puzzle):
    answer: str  # .lower to prevent case sensitive issues


@dataclass
class WeightPuzzle(Puzzle):
    weight_needed: float


@dataclass
class OrderPuzzle(Puzzle):
    order_of_location_needed: list[int] # list[Location]


@dataclass
class Item:
    """An item in our text adventure game world.

    Instance Attributes:
        - # TODO Describe each instance attribute here

    Representation Invariants:
        - # TODO Describe any necessary representation invariants
    """

    # NOTES:
    # This is just a suggested starter class for Item.
    # You may change these parameters and the data available for each Item object as you see fit.
    # (The current parameters correspond to the example in the handout).
    #
    # The only thing you must NOT change is the name of this class: Item.
    # All item objects in your game MUST be represented as an instance of this class.

    name: str
    description: str
    start_position: int # might be unnecessary
    weight: float
    the_key: Optional[str] # needed key, need this key to get the item
    puzzle_to_obtain: Optional[int] # like mug, you need weight puzzle to get item mug


@dataclass
class Key:
    key_name: str
    description: str
    start_position: int
    weight: float
    puzzle_to_obtain: int
    the_item: str # Item
    # room_location_key_in: Location
    # weight is 0lbs


# Note: Other entities you may want to add, depending on your game plan:
# - Puzzle class to represent special locations (could inherit from Location class if it seems suitable)
# - Player class
# etc.

if __name__ == "__main__":
    pass
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })
