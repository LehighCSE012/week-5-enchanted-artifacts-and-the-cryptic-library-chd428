"""sample adventure"""

import random

#items will be represented as strings
def acquire_item(inventory, item):
    """appends item to inventory list, prints a message"""
    inventory.append(item) #APPEND - adds an item to the inventory list, used to update the list
    print("You acquired a " + item + "!")
    return inventory

def display_inventory(inventory):
    """prints current inventory"""
    if inventory == []:
        print("Your inventory is empty.")
    else:
        i = 1
        print("Your inventory:")
        for item in inventory: #IN OPERATOR - iterates through each item in inventory
            #used to print inventory
            print(str(i) + ". " + str(item))
            i+=1

def display_player_status(player_stats):
    """displays player health"""
    # ... function code ...
    #parameter player_health = current health of the player
    #functionality - prints players current health to console in user friendly format
    #returns - nothing
    #if player_stats["health"]  100:
        #test 8 keeps bugging out... hopefully this fixes it?
        #print("You defeated the monster!")
    if player_stats["health"] >= -50:
        print("Your current health: " + str(player_stats["health"]))

def handle_path_choice(player_stats):
    """handle path choice"""
    # ... function code ...
    #functionality - randomly chooses path for the player, either "left" or "right".
    # you should use random.choise["left", "right"]
    path = random.choice(["left", "right"])
    if path == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        player_stats["health"] += 10
    elif path == "right":
        print("You fall into a pit and lose 15 health points.")
        player_stats["health"] -= 15
    if player_stats["health"] <= 0:
        player_stats["health"] = 0
        print("You are barely alive!")
    updated_player_health = player_stats["health"]
    return updated_player_health

def player_attack(monster_health, player_stats):
    """player attack"""
    # ... function code ...
    #function - simulates player's attack. player always inflicts 15 damage
    print("You strike the monster for " + str(player_stats["attack"]) +  " damage!")
    monster_health -= player_stats["attack"]
    updated_monster_health = monster_health
    return updated_monster_health

def monster_attack(player_stats):
    """monster attack"""
    # ... function code ...
    #function - simulates monster's attack
    #randomly determines if monster lands crit hit
    chance = random.random()
    if chance <= 0.5:
        #crit
        player_stats["health"] -= 20
        print("The monster lands a critical hit for 20 damage!")
    else:
        player_stats["health"] -= 10
        print("The monster hits you for 10 damage!")
    updated_player_health = player_stats["health"]
    return updated_player_health

def combat_encounter(player_stats, monster_health, has_treasure):
    """combat encounter"""
    # ... function code ...
    #function - manages combat encounter using while loop
    treasure_found_and_won = has_treasure
    while monster_health > 1 and player_stats["health"] > 1:
        display_player_status(player_stats)
        monster_health = player_attack(monster_health, player_stats)
        player_stats["health"] = monster_attack(player_stats)
    if player_stats["health"] < 0:
        print("Game over!")
        treasure_found_and_won = False
    elif monster_health < 0:
        print("You defeated the monster!")
        treasure_found_and_won = has_treasure
    return treasure_found_and_won # boolean

def check_for_treasure(has_treasure):
    """check for treasure"""
    # ... function code ...
    if has_treasure is True:
        print("You found the hidden treasure! You win!")
    elif has_treasure is False:
        print("The monster did not have the treasure. You continue your journey.")

def enter_dungeon(player_stats, inventory, dungeon_rooms, clues, artifacts):
    """iterates through each room in dungeon rooms"""
    for item in artifacts:
        if item[1] == "staff_of_wisdom":
            bypass = 1
            break
        else:
            bypass = 0
    userschoice = ""
    for rooms in dungeon_rooms:
        print(rooms[0])
        if rooms[1] is not None:
            acquire_item(inventory, rooms[1])
            print("You found a " + rooms[1] + " in the room.")
        if bypass > 0:
            userbypass = input("You can bypass the puzzle. Bypass?")
            are_equal: bool = userbypass in ('Yes','yes','Y','y')
            if are_equal is True:
                print("You bypassed the puzzle!")
            else:
                bypass = 2
        if bypass == 2 or bypass == 0:
            if rooms[2] == "puzzle":
                print("You encounter a puzzle!")
                userschoice = input("'Solve' or 'Skip'? ")
                are_equal: bool = userschoice in ("Solve", "solve")
                if are_equal is True:
                    success = random.choice([True,False])
                    if rooms[3] is not None:
                        if success is True:
                            print(rooms[3][0])
                        else:
                            print(rooms[3][1])
                    else:
                        print("The puzzle has no outcome.")
            elif rooms[2] == "trap":
                print("You see a potential trap!")
                userschoice = input("'Disarm' or 'Bypass'? ")
                are_equal: bool = userschoice in ("Disarm", "disarm")
                if are_equal is True:
                    success = random.choice([True,False])
                    if rooms[3] is not None:
                        if success is True:
                            print(rooms[3][0])
                        else:
                            print(rooms[3][1])
                    else:
                        print("The puzzle has no outcome.")
            elif rooms[2] == "library":
                clueoptions = ["The treasure is hidden where the dragon sleeps.",\
                        "The key lies with the gnome.", "Beware the shadows.",\
                        "The amulet unlocks the final door."]
                new_clue = random.sample(clueoptions, 2)
                for i in new_clue:
                    clues = find_clue(clues, i)
                if player_stats["wisdom"]>0:
                    print("You understand the meaning of the clues!")
                    print("You can now bypass a puzzle challenge.")
                    bypass = 1
            elif rooms[2] == "none":
                print("There doesn't seem to be a challenge in this room. You move on.")
        if bypass != 0:
            bypass -= 1
        if rooms[2] == "none":
            player_stats["health"]+=0
        elif rooms[3] is not None:
            player_stats["health"] += rooms[3][2]
        else:
            player_stats["health"]+=0
        if player_stats["health"] <= 0:
            player_stats["health"] = 0
            print("You are barely alive!")
        display_inventory(inventory)
    display_player_status(player_stats)
    #print("If you try to run 'dungeon_rooms.pop[1],")
    #if type(dungeon_rooms[1]) != tuple:
    #dungeon_rooms.pop([1]) #POP - removes value from list,
    #used to demonstrate that tuple cannot be changed
    #else:
    #print(dungeon_rooms[1], " - it can't be changed, it is immutable!")
    #print("Trying to pop it would result in a TypeError!")
    return player_stats, inventory, clues

def discover_artifact(player_stats, artifacts, artifact_name):
    """checks if artifact_name exists as a key in the artifacts dictionary
    if it exists, print desc and do what it says"""
    if artifacts[artifact_name] is not None:
        desc = artifacts[artifact_name].get("description")
        power = artifacts[artifact_name].get("power")
        effect = artifacts[artifact_name].get("effect")
        print(desc)
        if effect == "increases health":
            player_stats["health"] += power
            print("The artifact enhanced your health!")
        elif effect == "enhances attack":
            player_stats["attack"] += power
            print("The artifact enhanced your attack!")
        elif effect == "solves puzzles":
            player_stats["wisdom"] += power
            print("The artifact enhanced your wisdom!")
        artifacts.pop(artifact_name)
    else:
        print("You found nothing of interest.")
    return player_stats, artifacts

def find_clue(clues, new_clue):
    """checks if new_clue is already in set, adds if not"""
    if new_clue in clues:
        print("You already know this clue.")
    else:
        print("You've discovered a new clue: [" + new_clue + "]")
        clues.add(new_clue)
    return clues
def main():
    """Main game loop."""
    dungeon_rooms = [
    ("Dusty library", "key", "puzzle",
     ("Solved puzzle!", "Puzzle unsolved.", -5)),
    ("Narrow passage, creaky floor", "torch", "trap",
     ("Avoided trap!", "Triggered trap!", -10)),
    ("Grand hall, shimmering pool", "healing potion", "none", None),
    ("Small room, locked chest", "treasure", "puzzle",
     ("Cracked code!", "Chest locked.", -5)),
    ("Cryptic Library", None, "library", None)
    ]
    player_stats = {'health': 100, 'attack': 5, 'wisdom':0}
    monster_health = 70
    inventory = []
    clues = set()
    artifacts = {
        "amulet_of_vitality": {
            "description": "Glowing amulet, life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "Powerful ring, attack boost.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "Staff of wisdom, ancient.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }
    has_treasure = random.choice([True, False])
    display_player_status(player_stats)
    player_stats["health"] = handle_path_choice(player_stats)
    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)
        if treasure_obtained_in_combat is not None:
            check_for_treasure(treasure_obtained_in_combat)
        artifact_keys = list(artifacts.keys())
        if random.random() < 0.3 and artifact_keys:
            artifact_name = random.choice(artifact_keys)
            player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)
        display_player_status(player_stats)
    if player_stats['health'] > 0:
        player_stats, inventory, clues= enter_dungeon(player_stats, \
        inventory, dungeon_rooms, clues, artifacts)
    print("\n--- Game End ---")
    display_player_status(player_stats)
    print("Final Inventory:")
    display_inventory(inventory)
    print("Clues:")
    if clues:
        for clue in clues:
            print(f"- {clue}")
    else:
        print("No clues.")        

if __name__ == "__main__":
    main()
