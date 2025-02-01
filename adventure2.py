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

from game_entities import Key, Location, Item, Player, Puzzle
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
    # _items: list[Item]
    _items: dict[str, Item]
    current_location_id: int  # Suggested attribute, can be removed
    ongoing: bool  # Suggested attribute, can be removed
    _keys: dict[str, Key]
    _puzzles: dict[int, Puzzle]



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
        self._locations, self._items = self._load_game_data1(game_data_file)
        self._keys, self._puzzles = self._load_game_data2(game_data_file)

        # Suggested attributes (you can remove and track these differently if you wish to do so):
        self.current_location_id = initial_location_id  # game begins at this location
        self.ongoing = True  # whether the game is ongoing

    @staticmethod
    def _load_game_data1(filename: str) -> tuple[dict[int, Location], dict[str, Item]]:
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

        items = {}
        # TODO: Add Item objects to the items list; your code should be structured similarly to the loop above
        for item_data in data['items']:
            item_obj = Item(item_data['name'], item_data['description'], item_data['start_position'],
                            item_data['weight'], item_data['the_key'], item_data['puzzle_to_obtain'])
            # items.append(item_obj)
            items[item_data['name']] = item_obj

        return locations, items


    @staticmethod
    def _load_game_data2(filename: str) -> tuple[dict[str, Key], dict[int, Puzzle]]:
        with open(filename, 'r') as f:
            data = json.load(f)  # This loads all the data from the JSON file

        keys = {}
        for key_data in data['keys']:
            key_obj = Key(key_data['key_name'], key_data['description'], key_data['start_position'],
                            key_data['weight'], key_data['puzzle_to_obtain'], key_data['the_item'])

            keys[key_data['key_name']] = key_obj

        puzzles = {}
        for puzzle_data in data['puzzles']:
            puzzle_obj = Puzzle(puzzle_data['id_puzzle'], puzzle_data['description'], puzzle_data['answer'])

            puzzles[puzzle_data['id_puzzle']] = puzzle_obj

        return keys, puzzles


    def get_location(self, loc_id: Optional[int] = None) -> Location:
        """Return Location object associated with the provided location ID.
        If no ID is provided, return the Location object associated with the current location.
        """

        # TODO: Complete this method as specified
        if loc_id is None:
            return self._locations[self.current_location_id]
        return self._locations[loc_id]

    # ADDED JAN 30
    def get_item(self, item_name: str) -> Item:
        return self._items[item_name]


    def get_key(self, key_name: str) -> Key:
        return self._keys[key_name]


    def get_the_items(self) -> list[str]: # ['USB Drive', 'Laptop Charger', 'Monitor', 'Lucky Mug']
        the_list = []
        for item in self._items:
            the_list.append(item)
        return the_list


    def check_weight(self, player: Player, item_str: str) -> bool:
        added_weight = 0
        if item_str in self.get_the_items():
            added_weight = self.get_item(item_str).weight

        if self.sum_inv_weight(player) + added_weight <= 11:
            return True
        return False


    def check_key(self, player: Player, item_str: str) -> bool:
        need_key = None
        if item_str in self.get_the_items():
            need_key = self.get_item(item_str).the_key

        if need_key is None or (need_key is not None and need_key in player.get_inventory()):
            return True
        return False


    def check_puzzle(self, item_str: str, logger: EventList, loc: Location) -> bool:
        if item_str in self.get_the_items():
            need_puzzle = self.get_item(item_str).puzzle_to_obtain
        else:
            need_puzzle = self.get_key(item_str).puzzle_to_obtain

        if need_puzzle is None or (need_puzzle is not None and self.puzzle_choose(need_puzzle, logger, loc)):
            return True
        return False


    def sum_inv_weight(self, player: Player) -> float:
        the_sum = 0.0
        only_items = []
        for item_str in player.get_inventory():
            if item_str in self.get_the_items():
                only_items.append(item_str)

        for item_str in only_items:
            item = self.get_item(item_str)
            the_sum += item.weight
        return the_sum


    def puzzle_choose(self, puzzle_id, logger: EventList, loc: Location) -> bool:
        if puzzle_id == 1:
            return self.logic_puzzle(puzzle_id)
        elif puzzle_id == 2:
            return self.order_puzzle(puzzle_id, logger)
        else: #puzzle_id == 3
            return self.weight_puzzle(puzzle_id, loc)


    def logic_puzzle(self, puzzle_id: int) -> bool: # do this everytime you go to UC
        the_answer = input(self._puzzles[puzzle_id].description).lower()
        while the_answer != self._puzzles[puzzle_id].answer:
            the_answer = input("Wrong Answer! Try again. Enter 'q' if you would want to quit puzzle: ")
            if the_answer.lower() == 'q':
                return False
        return True


    def order_puzzle(self, puzzle_id: int, logger: EventList) -> bool:
        # no need to check logger.last == Robarts because you should be at Robarts to execute
        if logger.last.prev.id_num == self._puzzles[puzzle_id].answer[1] and logger.last.prev.prev.id_num == self._puzzles[puzzle_id].answer[0]:
            return True
        print(self._puzzles[puzzle_id].description + '\n')
        return False


    def weight_puzzle(self, puzzle_id: int, loc: Location) -> bool: # at conv hall 7
        the_sum = 0.0
        only_items = []
        for item_str in loc.items:
            if item_str in self.get_the_items():
                only_items.append(item_str)
        # now only items filtered
        for item_str in only_items:
            item = self.get_item(item_str)
            the_sum += item.weight

        if the_sum == self._puzzles[puzzle_id].answer:
            return True

        print(self._puzzles[puzzle_id].description + '\n')
        return False


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

        # ADDED JAN 30
        if len(location.items) != 0:
            print("This location also has item(s):")
            location.display_items()
        else:
            print("This location has NO items.")
            print()



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
    menu = ["look", "inventory", "score", "undo", "log", "weights", "quit"]  # Regular menu options available at each location
    choice = None
    menu_off = True
    location_change = True

    item_choice = None
    drop_choice = None # for undoing purposes of item restoring
    # Note: You may modify the code below as needed; the following starter code is just a suggestion

    steps_remaining = 30

    while game.ongoing and set(game.get_location(1).items) != set(game.get_the_items()): # while STEP < 19 and game.ongoing and set(location.items) == set(game.get_the_items())
        # Note: If the loop body is getting too long, you should split the body up into helper functions
        # for better organization. Part of your marks will be based on how well-organized your code is.

        location = game.get_location() # Location object

        # YOUR CODE HERE
        # ADDED JAN 30
        if menu_off: # prevent everytime you do menu command, it gives you description again and again
            game.look(location=location)  # perhaps change to only give descripton/location???

        if menu_off and location_change: # if you don't add this, when you undo, it adds another event still, which you don't want happening
            game_log.add_event(Event(game.get_location().id_num, game.get_location().long_description), choice)
            # steps_remaining -= 1

        menu_off = True
        location_change = True

        print("Allowed Moving Steps Remaining: " + str(steps_remaining))

        # testing
        # print(game_log.display_events())

        # TODO: Depending on whether or not it's been visited before,
        #  print either full description (first time visit) or brief description (every subsequent visit) of location
        # YOUR CODE HERE
        # ADDED JAN 26
        # game.look(location=location) # perhaps change to only give descripton/location???

        #previous item in and dropoff was here

        # Display possible actions at this location
        print("What to do? Choose from: look, inventory, score, weights, undo, log, quit")
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
                    steps_remaining += 1
                else:
                    # ADD REVERTING ITEM BACK/INTO INVENTORY AND LOCATIONS AGAIN
                    if 'Picked' in game_log.last.prev.next_command:
                        game.get_location(game_log.last.id_num).items.append(item_choice)
                        player.remove_item(item_choice)
                    else:
                        game.get_location(game_log.last.id_num).items.remove(drop_choice)
                        player.add_item(drop_choice)
                    player.score -= 5
                    game_log.remove_last_event() # duplicate code fix later



            elif choice == "inventory":
                player.display_inventory()
                print("Your current inventory weight is " + str(game.sum_inv_weight(player)) + " lbs")

            elif choice == "weights":
                print("Item Weights: ")
                for item in game.get_the_items():
                    print(item + " Weight: " + str(game.get_item(item).weight))
                print("All the Keys have a Weight of 0 lbs\n")

            elif choice == "quit":
                print("\nSad to see you quit the game. Have a good one!\n")
                game.ongoing = False
            # ENTER YOUR CODE BELOW to handle other menu commands (remember to use helper functions as appropriate)

        elif choice == 'pickitem':
            # Item pickup  ADDED JAN 26, add puzzle functionality later
            location_change = False
            if len(location.items) != 0:
                print("\nThe available items here are: ")
                location.display_items()


                item_choice = input("Pick your item: ")  # .lower().strip(), in future fix case
                while item_choice not in location.items:
                    print("You need to select a valid item from that list. Try again.")
                    item_choice = input("Pick your item: ")  # .lower().strip(), in future fix case
                # assert item_choice in location.items:

                # add here
                # runs once
                weight_ok = game.check_weight(player, item_choice)
                key_ok = game.check_key(player, item_choice)
                puzzle_ok = game.check_puzzle(item_choice, game_log, location)

                if weight_ok and key_ok and puzzle_ok:
                    player.add_item(item_choice)
                    location.items.remove(item_choice)

                    # Add the event only once
                    game_log.add_event(
                        Event(game.get_location().id_num, game.get_location().long_description),
                        "Picked up Item " + item_choice
                    )

                    # Add to the score
                    player.score += 5
                else:
                    if not weight_ok:
                        print("You cannot pick this item because you are overweight.")
                    if not key_ok:
                        print("You don't have a required key for this item.")
                    if not puzzle_ok:
                        print("Failed puzzle")

                player.display_inventory()

            else:
                print("There are no items in this location!\n")

        elif choice == 'dropitem':
            location_change = False

            # Item dropoff ADDED JAN 26
            if len(player.get_inventory()):
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
            if steps_remaining <= 0:
                print("No moving steps remaining. You cannot move to a new location. Game over!")
                game.ongoing = False
            else:
                # Charge one moving step.
                steps_remaining -= 1
                # game_log.add_event(
                #     Event(game.get_location().id_num, game.get_location().long_description),
                #     choice
                # )
                result = location.available_commands[choice]
                game.current_location_id = result

            # TODO: Add in code to deal with actions which do not change the location (e.g. taking or using an item)
            # TODO: Add in code to deal with special locations (e.g. puzzles) as needed for your game


        if menu_off: #previously undo
            location.visited = True # at the end, make visited true, but if there was undo, we want it to be false

    if set(game.get_location(1).items) == set(game.get_the_items()):
        print("Congratulations! You have won the game!")

    print("You had " + str(steps_remaining) + " step(s) remaining.")
    final_score = player.score + steps_remaining # steps remaining serves as bonus points.
    print("Your final score is " + str(final_score))
