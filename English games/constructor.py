import os
import json
import re
from datetime import datetime

class TextGameConstructor:
    def __init__(self):
        self.game_data = {
            "name": "My Text Game",
            "author": "Unknown",
            "start_location": None,
            "locations": {},
            "variables": {},
            "items": {}
        }
        self.current_location = None
        
        # Create games folder
        self.games_folder = "My_Games"
        if not os.path.exists(self.games_folder):
            os.makedirs(self.games_folder)
            print(f"📁 Created folder: {self.games_folder}")
    
    def create_location(self):
        """Create new location"""
        print("\n=== CREATE LOCATION ===")
        loc_id = input("Location ID (e.g. 'forest'): ").strip()
        
        if loc_id in self.game_data["locations"]:
            print("❌ Location with this ID already exists!")
            return
        
        name = input("Location name: ").strip()
        desc = input("Location description: ").strip()
        
        self.game_data["locations"][loc_id] = {
            "name": name,
            "description": desc,
            "actions": {}
        }
        
        print(f"✅ Location '{name}' created!")
        
        if not self.game_data.get("start_location"):
            self.game_data["start_location"] = loc_id
            print("⭐ This location set as starting point!")
    
    def create_action(self):
        """Create action in location"""
        if not self.game_data["locations"]:
            print("❌ Create at least one location first!")
            return
        
        print("\n=== CREATE ACTION ===")
        print("Available locations:")
        for loc_id in self.game_data["locations"]:
            print(f"  - {loc_id}: {self.game_data['locations'][loc_id]['name']}")
        
        loc_id = input("\nLocation ID for action: ").strip()
        if loc_id not in self.game_data["locations"]:
            print("❌ Location not found!")
            return
        
        action_text = input("Action text (e.g. 'go left'): ").strip()
        action_id = f"act_{len(self.game_data['locations'][loc_id]['actions'])}"
        
        print("\nAction type:")
        print("1. Go to another location")
        print("2. Take item")
        print("3. Check condition")
        print("4. Change variable")
        print("5. End game")
        
        type_choice = input("Choose type (1-5): ").strip()
        
        action_data = {
            "text": action_text,
            "type": "goto"
        }
        
        if type_choice == "1":
            print("\nAvailable locations to go:")
            for t_loc_id in self.game_data["locations"]:
                print(f"  - {t_loc_id}: {self.game_data['locations'][t_loc_id]['name']}")
            target = input("Target location ID: ").strip()
            if target in self.game_data["locations"]:
                action_data["target"] = target
            else:
                print("❌ Location not found!")
                return
        
        elif type_choice == "2":
            item = input("Item name: ").strip()
            action_data["type"] = "take"
            action_data["item"] = item
        
        elif type_choice == "3":
            var = input("Variable name: ").strip()
            val = input("Value to check: ").strip()
            print("\nAction if TRUE:")
            print("Enter location ID or 'end' for game over")
            true_action = input("→ ").strip()
            print("Action if FALSE:")
            false_action = input("→ ").strip()
            
            action_data["type"] = "condition"
            action_data["var"] = var
            action_data["value"] = val
            action_data["true"] = true_action
            action_data["false"] = false_action
        
        elif type_choice == "4":
            var = input("Variable name: ").strip()
            op = input("Operation (=, +, -): ").strip()
            val = input("Value: ").strip()
            
            action_data["type"] = "setvar"
            action_data["var"] = var
            action_data["op"] = op
            action_data["val"] = val
        
        elif type_choice == "5":
            action_data["type"] = "end"
            message = input("Final message: ").strip()
            action_data["message"] = message
        
        self.game_data["locations"][loc_id]["actions"][action_id] = action_data
        print(f"✅ Action added to location '{loc_id}'!")
    
    def list_locations(self):
        """Show all locations"""
        print("\n=== LOCATIONS ===")
        for loc_id, loc in self.game_data["locations"].items():
            print(f"\n📍 {loc_id}: {loc['name']}")
            print(f"   Description: {loc['description']}")
            if loc['actions']:
                print("   Actions:")
                for act_id, act in loc['actions'].items():
                    print(f"     • {act['text']}")
            else:
                print("   ⚠️ No actions!")
    
    def sanitize_filename(self, filename):
        """Remove invalid characters from filename"""
        filename = re.sub(r'[<>:"/\\|?*!]', '_', filename)
        return filename
    
    def save_game(self):
        """Save game as .py file in My_Games folder"""
        if not self.game_data["locations"]:
            print("❌ No locations to save!")
            return
        
        if not self.game_data.get("start_location"):
            print("❌ No starting location!")
            return
        
        filename = input("File name (without .py): ").strip()
        filename = self.sanitize_filename(filename)
        
        if not filename:
            print("❌ Invalid filename!")
            return
        
        full_path = os.path.join(self.games_folder, filename + ".py")
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_game_code())
        
        print(f"✅ Game saved as '{full_path}'!")
        print("📁 File is in 'My_Games' folder")
    
    def _generate_game_code(self):
        """Generate Python game code"""
        locations_json = json.dumps(self.game_data['locations'], ensure_ascii=False, indent=2)
        variables_json = json.dumps(self.game_data.get('variables', {}), ensure_ascii=False, indent=2)
        start_loc = self.game_data['start_location']
        
        code = '# ' + self.game_data['name'] + '\n'
        code += '# Author: ' + self.game_data['author'] + '\n'
        code += '# Created: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n'
        code += '# Generated by Text Game Constructor\n\n'
        code += 'import time\n\n'
        code += 'def print_slow(text):\n'
        code += '    for char in text:\n'
        code += '        print(char, end=\'\', flush=True)\n'
        code += '        time.sleep(0.02)\n'
        code += '    print()\n\n'
        code += '# Game data\n'
        code += 'locations = ' + locations_json + '\n'
        code += 'variables = ' + variables_json + '\n'
        code += 'inventory = []\n\n'
        code += 'def play():\n'
        code += '    current = "' + start_loc + '"\n\n'
        code += '    while True:\n'
        code += '        if current not in locations:\n'
        code += '            print(f"Error: location {current} not found!")\n'
        code += '            break\n\n'
        code += '        loc = locations[current]\n'
        code += '        print_slow("\\n📍 " + loc["name"])\n'
        code += '        print_slow(loc["description"])\n\n'
        code += '        if not loc["actions"]:\n'
        code += '            print("\\n⏹️ Game over!")\n'
        code += '            break\n\n'
        code += '        actions = list(loc["actions"].items())\n'
        code += '        for i, (act_id, act) in enumerate(actions, 1):\n'
        code += '            print(f"{i}. {act[\'text\']}")\n\n'
        code += '        try:\n'
        code += '            choice = int(input("\\n👉 Choose action: ")) - 1\n'
        code += '            if choice < 0 or choice >= len(actions):\n'
        code += '                print("❌ Wrong choice!")\n'
        code += '                continue\n\n'
        code += '            act_id, action = actions[choice]\n\n'
        code += '            if action["type"] == "goto":\n'
        code += '                current = action["target"]\n\n'
        code += '            elif action["type"] == "take":\n'
        code += '                inventory.append(action["item"])\n'
        code += '                print(f"✅ You took: {action[\'item\']}")\n'
        code += '                current = action.get("next", current)\n\n'
        code += '            elif action["type"] == "setvar":\n'
        code += '                var = action["var"]\n'
        code += '                val = action["val"]\n'
        code += '                op = action.get("op", "=")\n\n'
        code += '                if op == "=":\n'
        code += '                    variables[var] = val\n'
        code += '                elif op == "+":\n'
        code += '                    variables[var] = str(int(variables.get(var, 0)) + int(val))\n'
        code += '                elif op == "-":\n'
        code += '                    variables[var] = str(int(variables.get(var, 0)) - int(val))\n\n'
        code += '                print(f"📊 Variable {var} = {variables[var]}")\n'
        code += '                current = action.get("next", current)\n\n'
        code += '            elif action["type"] == "condition":\n'
        code += '                var_val = variables.get(action["var"], "")\n'
        code += '                if str(var_val) == str(action["value"]):\n'
        code += '                    print("✅ Condition met!")\n'
        code += '                    next_loc = action["true"]\n'
        code += '                else:\n'
        code += '                    print("❌ Condition not met!")\n'
        code += '                    next_loc = action["false"]\n\n'
        code += '                if next_loc == "end":\n'
        code += '                    print_slow("\\n🎬 " + action.get("message", "Game over!"))\n'
        code += '                    break\n'
        code += '                else:\n'
        code += '                    current = next_loc\n\n'
        code += '            elif action["type"] == "end":\n'
        code += '                print_slow("\\n🎬 " + action["message"])\n'
        code += '                break\n\n'
        code += '        except ValueError:\n'
        code += '            print("❌ Enter a number!")\n'
        code += '        except Exception as e:\n'
        code += '            print(f"❌ Error: {e}")\n\n'
        code += 'if __name__ == "__main__":\n'
        code += '    print("=" * 50)\n'
        code += '    print("🎮 " + locations[\'' + start_loc + '\']["name"])\n'
        code += '    print("=" * 50)\n'
        code += '    play()\n'
        
        return code
    
    def run(self):
        """Main menu"""
        while True:
            print("\n" + "=" * 50)
            print("🎮 TEXT GAME CONSTRUCTOR")
            print("=" * 50)
            print(f"📁 Folder: {self.games_folder}")
            print(f"Title: {self.game_data['name']}")
            print(f"Author: {self.game_data['author']}")
            print(f"Locations: {len(self.game_data['locations'])}")
            if self.game_data.get("start_location"):
                start = self.game_data["start_location"]
                print(f"Start: {self.game_data['locations'][start]['name']}")
            print("-" * 50)
            print("1. 📍 Create location")
            print("2. ➕ Create action")
            print("3. 📋 List locations")
            print("4. ✏️ Change title/author")
            print("5. 💾 Save game (.py)")
            print("6. 🚪 Exit")
            
            choice = input("\n👉 Choose: ").strip()
            
            if choice == "1":
                self.create_location()
            elif choice == "2":
                self.create_action()
            elif choice == "3":
                self.list_locations()
            elif choice == "4":
                new_name = input("New title: ").strip()
                if new_name:
                    self.game_data['name'] = new_name
                new_author = input("New author: ").strip()
                if new_author:
                    self.game_data['author'] = new_author
                print("✅ Updated!")
            elif choice == "5":
                self.save_game()
            elif choice == "6":
                print("👋 Bye!")
                break
            else:
                print("❌ Wrong choice")

if __name__ == "__main__":
    constructor = TextGameConstructor()
    constructor.run()