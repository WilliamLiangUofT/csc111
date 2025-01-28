"""CSC111 Project 1: Text Adventure Game - Game Manager

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code for Project 1. Please consult
the project handout for instructions and details.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC111 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2025 CSC111 Teaching Team
"""
from __future__ import annotations
import json
from typing import Optional

from game_entities import Location, Item, Player
from proj1_event_logger import Event, EventList


# Note: You may add in other import statements here as needed

# Note: You may add helper functions, classes, etc. below as needed


class AdventureGame:
    """A text adventure game class storing all location, item and map data.

    Instance Attributes:
        - # TODO add descriptions of public instance attributes as needed

    Representation Invariants:
        - # TODO add any appropriate representation invariants as needed
    """

    # Private Instance Attributes (do NOT remove these two attributes):
    #   - _locations: a mapping from location id to Location object.
    #                       This represents all the locations in the game.
    #   - _items: a list of Item objects, representing all items in the game.

    _locations: dict[int, Location]
    _items: list[Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed

    def __init__(self, game_data_file: str, initial_location_id: int) -> None:
        """
        Initialize a new text adventure game, based on the data in the given file, setting starting location of game
        at the given initial location ID.
        (note: you are allowed to modify the format of the file as you see fit)

        Preconditions:
        - game_data_file is the filename of a valid game data JSON file
        """

        # NOTES:
        # You may add parameters/attributes/methods to this class as you see fit.

        # Requirements:
        # 1. Make sure the Location class is used to represent each location.
        # 2. Make sure the Item class is used to represent each item.

        # Suggested helper method (you can remove and load these differently if you wish to do so):
        self._locations, self._items = self._load_game_data(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing

    @staticmethod
    def _load_game_data(filename: str) -> tuple[dict[int, Location], list[Item]]:
        """Load locations and items from a JSON file with the given filename and
        return a tuple consisting of (1) a dictionary of locations mapping each game location's ID to a Location object,
        and (2) a list of all Item objects."""

        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        locations = {}
        for loc_data in data['locations']:  # Go through each element associated with the 'locations' key in the file
            location_obj = Location(loc_data['id'], loc_data['name'], loc_data['brief_description'],
                                    loc_data['long_description'],
                                    loc_data['available_commands'], loc_data['items'])
            locations[loc_data['id']] = location_obj

        items = []
        # TODO: Add Item objects to the items list; your code should be structured similarly to the loop above
        for item_data in data['items']:
            item_obj = Item(item_data['name'], item_data['description'], item_data['start_position'],
                            item_data['weight'], item_data['the_key'], item_data['puzzle_to_obtain'])
            items.append(item_obj)

        return locations, items

    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        # TODO: Complete this method as specified
        if loc_id is None:
            return self._locations[self.current_location_id]
        return self._locations[loc_id]

    # ADDED JAN 26
    def look(self, location: Location) -> None:  # pass in location variable from below
        # the_location = self.get_location(loc_id=location.id_num) # Location object, passed in Location
        print("Location " + str(location.id_num))
        if location.visited:
            print(
                "You are now at " + location.name + "! Since you have been here before, here's a BRIEF description of "
                                                    "this place.\n" + location.brief_description + "\n")
        else:
            print("You are now at " + location.name + "! Since you have NEVER been here before, here's a LONG "
                                                      "description of this fabulous place!\n"
                  + location.long_description + "\n")


if __name__ == "__main__":

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (Delete the "#" and space before each line.)
    # IMPORTANT: keep this code indented inside the "if __name__ == '__main__'" block
    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['R1705', 'E9998', 'E9999']
    # })
    player = Player([], 0.0, 0)

    game_log = EventList()  # This is REQUIRED as one of the baseline requirements
    game = AdventureGame('game_data.json', 1)  # load data, setting initial location ID to 1
    menu = ["look", "inventory", "score", "undo", "log", "quit"]  # Regular menu options available at each location
    choice = None
    menu_off = True
    location_change = True

    item_choice = None
    drop_choice = None # for undoing purposes of item restoring
    # Note: You may modify the code below as needed; the following starter code is just a suggestion
    while game.ongoing:
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        location = game.get_location()

        # TODO: Add new Event to game log to represent current game location
        #  Note that the <choice> variable should be the command which led to this event
        # YOUR CODE HERE
        # ADDED JAN 26
        if menu_off and location_change: # if you don't add this, when you undo, it adds another event still, which you don't want happening
            game_log.add_event(Event(game.get_location().id_num, game.get_location().long_description), choice)
        menu_off = True
        location_change = True
        # testing
        # print(game_log.display_events())

        # TODO: Depending on whether or not it's been visited before,
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        # YOUR CODE HERE
        # ADDED JAN 26
        game.look(location=location) # perhaps change to only give descripton/location???

        #previous item in and dropoff was here

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, undo, log, quit")
        print("At this location, you can also:")
        for action in location.available_commands:
            print("-", action)
        print("- Pick item (enter pickitem): ")
        print("- Drop item (enter dropitem): ")

        # Validate choice
        choice = input("\nEnter action: ").lower().strip()
        while choice not in location.available_commands and choice not in menu and choice != 'pickitem' and choice != 'dropitem':
            print("That was an invalid option; try again.")
            choice = input("\nEnter action: ").lower().strip()

        print("========")
        print("You decided to:", choice)

        if choice in menu:
            # TODO: Handle each menu command as appropriate
            # ADDED JAN 26
            # Note: For the "undo" command, remember to manipulate the game_log event list to keep it up-to-date
            menu_off = False
            if choice == "log":
                game_log.display_events()
                print()
            elif choice == "look": # SHOULD ADD LOCATION ITEMS IF PRESENT
                game.look(location)
            elif choice == "score":
                print("\nPlayers Score: " + str(player.score))
            elif choice == "undo": # need to add undo for items

                if game_log.last.id_num != game_log.last.prev.id_num: # if locations  changed, item
                    game.get_location(game_log.last.id_num).visited = False # Sets to be removed event visited back to false
                    game_log.remove_last_event()
                    game.current_location_id = game_log.last.id_num
                    game.get_location(game_log.last.id_num).visited = False # Sets the new last event visited back to false
                else:
                    # ADD REVERTING ITEM BACK/INTO INVENTORY AND LOCATIONS AGAIN
                    if 'Picked' in game_log.last.prev.next_command:
                        game.get_location(game_log.last.id_num).items.append(item_choice)
                        player.remove_item(item_choice)
                    else:
                        game.get_location(game_log.last.id_num).items.remove(drop_choice)
                        player.add_item(drop_choice)
                    game_log.remove_last_event() # duplicate code fix later



            elif choice == "inventory":
                player.display_inventory()

            elif choice == "quit":
                print("\nSad to see you quit the game. Have a good one!\n")
                game.ongoing = False
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)

        elif choice == 'pickitem':
            # Item pickup  ADDED JAN 26, add puzzle functionality later
            location_change = False
            if len(location.items) != 0:
                print("\nThe available items here are: ")
                for item in location.items:
                    print("- " + item)
                item_or_not = input(
                    "You may choose to pickup zero, one or multiple items right here. Enter (y/n): ").lower()
                if item_or_not == 'y':
                    item_choice = input("Pick your item: ")  # .lower().strip(), in future fix case
                    while item_choice not in location.items:
                        print("You need to select a valid item from that list. Try again.")
                        item_choice = input("Pick your item: ")  # .lower().strip(), in future fix case
                    # assert item_choice in location.items:
                    player.add_item(item_choice)
                    location.items.remove(item_choice)

                    player.display_inventory()

                    game_log.add_event(Event(game.get_location().id_num, game.get_location().long_description),
                                       "Picked up Item " + item_choice)
            else:
                print("There are no items in this location!\n")

        elif choice == 'dropitem':
            location_change = False

            # Item dropoff ADDED JAN 26
            if len(player.get_inventory()):
                drop_item_cond = input("Would you like to drop zero, one/multiple item(s)? (y/n): ").lower()
                if drop_item_cond == 'y':
                    player.display_inventory()
                    drop_choice = input("Pick item to drop: ")  # .lower().strip(), in future fix case
                    while drop_choice not in player.get_inventory():
                        print("You need to select a valid item from your inventory. Try again.")
                        drop_choice = input("Pick item to drop: ")  # .lower().strip(), in future fix case
                    # assert drop_choice in player.get_inventory()
                    location.items.append(drop_choice)
                    player.remove_item(drop_choice)

                    player.display_inventory()

                    game_log.add_event(Event(game.get_location().id_num, game.get_location().long_description),
                                       "Dropped Item " + drop_choice)
            else:
                print("You have no items do drop!\n")

        else:
            # Handle non-menu actions
            result = location.available_commands[choice]
            game.current_location_id = result

            # TODO: Add in code to deal with actions which do not change the location (e.g. taking or using an item)
            # TODO: Add in code to deal with special locations (e.g. puzzles) as needed for your game


        if menu_off: #previously undo
            location.visited = True # at the end, make visited true, but if there was undo, we want it to be false
