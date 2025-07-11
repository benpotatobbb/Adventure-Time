import random
import datetime
import json
import re
from collections import defaultdict
from itertools import cycle
from functools import reduce

# Custom Exceptions
class AdventureError(Exception):
    """Custom exception for adventure-related errors"""
    pass

class CharacterNotFoundError(AdventureError):
    """Raised when a character is not found"""
    pass

class InsufficientFundsError(AdventureError):
    """Raised when a character cannot afford an item"""
    pass

# Base Character Class
class Character:
    def __init__(self, name, health=100, strength=10, gold=50):
        self.name = name
        self.health = health
        self.strength = strength
        self.gold = gold
        self.inventory = []

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)
        return self.health

    def add_item(self, item):
        self.inventory.append(item)
        return f"{self.name} added {item} to inventory"

    def spend_gold(self, amount):
        if amount > self.gold:
            raise InsufficientFundsError(f"{self.name} needs {amount} gold but only has {self.gold}")
        self.gold -= amount
        return f"{self.name} spent {amount} gold"

    def __str__(self):
        role = type(self).__name__
        return f"{self.name} [{role}] (Health: {self.health}, Strength: {self.strength}, Gold: {self.gold}, Inventory: {self.inventory})"

# Subclasses with Polymorphism
class Hero(Character):
    def attack(self, enemy):
        damage = random.randint(self.strength // 2, self.strength)
        enemy.take_damage(damage)
        return f"{self.name} attacks {enemy.name} for {damage} damage!"

class Princess(Character):
    def heal(self, target):
        heal_amount = random.randint(10, 20)
        target.health = min(100, target.health + heal_amount)
        return f"{self.name} heals {target.name} for {heal_amount} health!"

class Villain(Character):
    def taunt(self):
        taunts = ["You'll never defeat me!", "Ooo will be mine!"]
        return f"{self.name} says: {random.choice(taunts)}"

class Shopkeeper(Character):
    def offer_deal(self):
        return f"{self.name} offers a weird gadget from the shop!"

# Shop Class
class GoosesShop:
    def __init__(self):
        self.name = "Choose Goose's Shop"
        self.items = {
            "Magic Sword": {"cost": 30, "effect": lambda char: setattr(char, "strength", char.strength + 5)},
            "Banana Guard Armor": {"cost": 40, "effect": lambda char: setattr(char, "health", char.health + 20)},
            "Weird Gizmo": {"cost": 25, "effect": lambda char: char.add_item("Gizmo") or "Gizmo sparks mysteriously!"},
            "Enchiridion Shard": {"cost": 50, "effect": lambda char: char.add_item("Enchiridion Shard") or "Power surges!"},
            "Candy Cane Blaster": {"cost": 35, "effect": lambda char: setattr(char, "strength", char.strength + 3)},
            "Magic Dog Biscuit": {"cost": 20, "effect": lambda char: setattr(char, "health", char.health + 10) if isinstance(char, Hero) else None}
        }

    def offer_deal(self):
        rhymes = [
            "Buy a sword, fight a horde!",
            "Shiny gear, have no fear!",
            "Gold you toss, for gear that's boss!"
        ]
        return f"{self.name} says: '{random.choice(rhymes)}'"

    def display_items(self):
        return "Available items:\n" + "\n".join([f"- {item}: {details['cost']} gold" for item, details in self.items.items()])

    def buy_item(self, character, item_name):
        if item_name not in self.items:
            raise AdventureError(f"Item '{item_name}' not in shop")
        item = self.items[item_name]
        character.spend_gold(item["cost"])
        result = item["effect"](character)
        return f"{character.name} bought {item_name}! {result or ''}"

# Simulation Manager
class AdventureSimulation:
    def __init__(self):
        self.characters = {}
        self.shop = GoosesShop()
        self.log_file = "adventure_log.json"
        self.event_log = []

    def initialize_characters(self):
        self.characters = {
            "Finn": Hero("Finn", 120, 15, 100),
            "Jake": Hero("Jake", 100, 12, 80),
            "Princess-Bubblegum": Princess("Princess Bubblegum", 80, 8, 120),
            "Marceline": Hero("Marceline", 110, 14, 90),
            "Ice-King": Villain("Ice King", 90, 10, 70),
            "BMO": Character("BMO", 50, 5, 60),
            "NEPTR": Character("NEPTR", 40, 4, 50),
            "Lumpy-Space-Princess": Princess("Lumpy Space Princess", 70, 7, 100),
            "Magic-Man": Villain("Magic Man", 60, 9, 80),
            "Flame-Princess": Princess("Flame Princess", 100, 13, 90),
            "Tree-Trunks": Character("Tree Trunks", 30, 3, 40),
            "Lady-Rainicorn": Character("Lady Rainicorn", 80, 8, 70),
            "Gunter": Character("Gunter", 40, 6, 50),
            "Choose-Goose": Shopkeeper("Choose Goose", 60, 5, 200)
        }

    def apply_random_event(self):
        events = [
            lambda c: c.add_item(random.choice(["Magic Sword", "Candy Cane", "Enchiridion"])),
            lambda c: c.take_damage(random.randint(5, 15)),
            lambda c: f"{c.name} finds a secret path!" if isinstance(c, Hero) else f"{c.name} sets a trap!",
            lambda c: c.spend_gold(10) if c.gold >= 10 else f"{c.name} is too poor for this event!"
        ]
        characters = list(self.characters.values())
        results = list(map(lambda char: random.choice(events)(char), characters))
        self.event_log.extend(results)
        return results

    def calculate_team_strength(self, team):
        return reduce(lambda total, char: total + char.strength, team, 0)

    def save_log(self):
        try:
            with open(self.log_file, 'w') as f:
                json.dump({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "events": self.event_log
                }, f, indent=2)
        except IOError as e:
            raise AdventureError(f"Failed to save log: {e}")

    def load_log(self):
        try:
            with open(self.log_file, 'r') as f:
                data = json.load(f)
                self.event_log = data["events"]
                return data
        except FileNotFoundError:
            return {"events": [], "timestamp": None}
        except json.JSONDecodeError as e:
            raise AdventureError(f"Corrupted log file: {e}")

    def give_quest(self):
        quests = [
            "Rescue BMO from the Ice Kingdom.",
            "Retrieve the Enchiridion from the forest of mystery.",
            "Defeat the Magic Man's Hat before sundown.",
            "Deliver a Candy Cane Blaster to Bubblegum.",
            "Escort Tree Trunks safely to her orchard."
        ]
        quest = random.choice(quests)
        self.event_log.append(f"{datetime.datetime.now().isoformat()}: Quest - {quest}")
        return f"New Quest: {quest}"

    def find_character(self, name):
        """Case-insensitive character lookup"""
        for char_name in self.characters:
            if char_name.lower() == name.lower():
                return self.characters[char_name]
        raise CharacterNotFoundError(f"Character '{name}' not found")

    def validate_command(self, command):
        """Validate and parse commands with multi-word character and item names"""
        # Pattern for commands with two arguments
        pattern_args = r"^(attack|heal|add_item|buy)\s+(.+?)\s+(.+)$"
        # Pattern for commands with no arguments
        pattern_no_args = r"^(event|status|shop|quest|characters|help|exit)$"
        command = command.strip()
        match_args = re.match(pattern_args, command, re.IGNORECASE)
        match_no_args = re.match(pattern_no_args, command, re.IGNORECASE)
        if match_args:
            action, char_name, item_or_target = match_args.groups()
            char_name = " ".join(char_name.split())
            item_or_target = " ".join(item_or_target.split()) if item_or_target else None
            return action.lower(), char_name, item_or_target
        elif match_no_args:
            action = match_no_args.group(1).lower()
            return action, None, None
        else:
            raise AdventureError("Invalid command format. Type 'help' for commands.")

    def display_help(self):
        help_text = """
Available Commands:
  - attack <hero> <target>       : Hero attacks a target (e.g., attack Finn Ice King)
  - heal <princess> <target>     : Princess heals a target (e.g., heal Princess Bubblegum Finn)
  - add_item <character> <item>   : Add item to character's inventory (e.g., add_item Jake Sword)
  - buy <character> <item>        : Buy item from shop (e.g., buy Finn Magic Sword)
  - shop                         : Display shop items
  - event                        : Trigger a random event for all characters
  - quest                        : Receive a random quest
  - status                       : Show all character statuses
  - characters                   : List all playable characters
  - help                         : Show this help message
  - exit                         : Save and quit

Available Characters:
{}
""".format(
            "\n".join([f"- {name} ({type(char).__name__})" for name, char in self.characters.items()]),
            "\n".join([f"- {item}" for item in self.shop.items.keys()])
        )
        return help_text

    def run_simulation(self):
        self.initialize_characters()
        print("Welcome to the Adventure Time Simulation in the Land of Ooo!")
        print(self.display_help())

        while True:
            try:
                command = input("Enter command (type 'help' for commands): ")
                if not command.strip():
                    print("Please enter a command.")
                    continue

                action, arg1, arg2 = self.validate_command(command)

                if action == "exit":
                    self.save_log()
                    print("Adventure saved! Goodbye!")
                    break

                if action == "status":
                    for char in self.characters.values():
                        print(char)
                    continue

                if action == "characters":
                    print("Available Characters:")
                    for name, char in self.characters.items():
                        role = type(char).__name__
                        print(f"- {name} ({role})")
                    continue

                if action == "shop":
                    print(self.shop.offer_deal())
                    print(self.shop.display_items())
                    continue

                if action == "event":
                    results = self.apply_random_event()
                    for result in results:
                        print(result)
                    continue

                if action == "quest":
                    print(self.give_quest())
                    continue

                if action == "help":
                    print(self.display_help())
                    continue

                if not arg1:
                    raise AdventureError("Character name required.")

                # Find character with case-insensitive lookup
                character = self.find_character(arg1)

                if action == "attack":
                    if not arg2:
                        raise AdventureError("Target character required.")
                    target = self.find_character(arg2)
                    if isinstance(character, Hero):
                        print(character.attack(target))
                    else:
                        raise AdventureError(f"{character.name} cannot attack!")

                elif action == "heal":
                    if not arg2:
                        raise AdventureError("Target character required.")
                    target = self.find_character(arg2)
                    if isinstance(character, Princess):
                        print(character.heal(target))
                    else:
                        raise AdventureError(f"{character.name} cannot heal!")

                elif action == "add_item":
                    if not arg2:
                        raise AdventureError("Item name required.")
                    print(character.add_item(arg2))

                elif action == "buy":
                    if not arg2:
                        raise AdventureError("Item name required.")
                    # Case-insensitive item lookup
                    item_name = None
                    for item in self.shop.items:
                        if item.lower() == arg2.lower():
                            item_name = item
                            break
                    if not item_name:
                        raise AdventureError(f"Item '{arg2}' not found in shop. Available items: {', '.join(self.shop.items.keys())}")
                    print(self.shop.buy_item(character, item_name))

                self.event_log.append(f"{datetime.datetime.now().isoformat()}: {command}")

            except (AdventureError, CharacterNotFoundError, InsufficientFundsError) as e:
                print(f"Error: {e}")
                self.event_log.append(f"{datetime.datetime.now().isoformat()}: Error - {e}")

if __name__ == "__main__":
    sim = AdventureSimulation()
    sim.run_simulation()