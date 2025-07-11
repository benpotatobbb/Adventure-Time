Adventure Time Simulation
Overview
This project is a text-based simulation inspired by Adventure Time, set in the Land of Ooo. Players can control characters like Finn, Jake, and Princess Bubblegum, engage in actions such as attacking, healing, and buying items from Choose Goose's Shop, and participate in random events and quests. The simulation uses object-oriented programming (OOP) principles, custom exceptions, and a command-line interface to manage character interactions and game state.
Features

Character Classes: Includes Hero, Princess, Villain, Shopkeeper, and generic Character classes with unique abilities (e.g., attack, heal, taunt, offer_deal).
Shop System: Choose Goose's Shop allows characters to buy items like Magic Sword or Banana Guard Armor, which modify character attributes or add to inventory.
Random Events: Events like finding items, taking damage, or discovering paths are applied to all characters.
Quest System: Random quests are generated, such as rescuing BMO or retrieving the Enchiridion.
Command-Line Interface: Supports commands like attack, heal, buy, shop, event, quest, status, characters, help, and exit.
Logging: Game events are logged to a JSON file (adventure_log.json) for persistence.
Error Handling: Custom exceptions (AdventureError, CharacterNotFoundError, InsufficientFundsError) ensure robust error management.

Requirements

Python 3.6+
Standard libraries: random, datetime, json, re, collections, itertools, functools

Installation

Clone or download the project files.
Ensure Python 3.6+ is installed.
Place the main script (AhmedAmeen_2405045037_BasicProgrammingFinals_DGD1.py) in a directory.
No additional dependencies are required.

Usage

Run the script:python AhmedAmeen_2405045037_BasicProgrammingFinals_DGD1.py


The simulation starts with a welcome message and help text.
Enter commands to interact with the game (e.g., attack Finn Ice King, buy Jake Magic Sword, quest).
Type help to see available commands and characters.
Type exit to save the event log and quit.

Commands

attack <hero> <target>: Hero attacks a target (e.g., attack Finn Ice King).
heal <princess> <target>: Princess heals a target (e.g., heal Princess Bubblegum Finn).
add_item <character> <item>: Adds an item to a character's inventory.
buy <character> <item>: Buys an item from the shop.
shop: Displays shop items and a fun rhyme.
event: Triggers random events for all characters.
quest: Generates a random quest.
status: Shows all characters' stats.
characters: Lists all characters and their roles.
help: Displays command help.
exit: Saves the log and exits.

File Structure

AhmedAmeen_2405045037_BasicProgrammingFinals_DGD1.py: Main simulation script.
adventure_log.json: Generated log file for game events (created on exit).

Notes

Character and item names are case-insensitive.
The shop's items have specific effects, such as increasing strength or health.
The simulation logs events to adventure_log.json, which can be loaded in future sessions.
Invalid commands or actions trigger descriptive error messages.

Example Interaction
Welcome to the Adventure Time Simulation in the Land of Ooo!
[Help text displayed]
Enter command: shop
Choose Goose's Shop says: 'Gold you toss, for gear that's boss!'
Available items:
- Magic Sword: 30 gold
- Banana Guard Armor: 40 gold
...
Enter command: buy Finn Magic Sword
Finn bought Magic Sword! Finn's strength increased!
Enter command: status
Finn [Hero] (Health: 120, Strength: 20, Gold: 70, Inventory: [])
...
Enter command: exit
Adventure saved! Goodbye!

License
This project is for educational purposes and inspired by Adventure Time. No official affiliation with the franchise exists.
