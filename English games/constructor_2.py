import os
import json
from datetime import datetime

class GameBuilderEnglish:
    def __init__(self):
        self.game_data = {
            "name": "My Text Adventure",
            "author": "Unknown",
            "start_location": None,
            "locations": {},
            "variables": {},
            "items": {}
        }
        self.games_folder = "My_Games"
        if not os.path.exists(self.games_folder):
            os.makedirs(self.games_folder)
    
    def create_location(self):
        """Create a new location"""
        print("\n=== CREATE LOCATION ===")
        loc_id = input("Location ID: ").strip()
        
        if loc_id in self.game_data["locations"]:
            print("❌ Location already exists!")
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
            print("⭐ Starting location!")
    
    def create_action(self):
        """Create an action in a location"""
        if not self.game_data["locations"]:
            print("❌ Create a location first!")
            return
        
        print("\n=== CREATE ACTION ===")
        print("Available locations:")
        for loc_id in self.game_data["locations"]:
            print(f"  - {loc_id}: {self.game_data['locations'][loc_id]['name']}")
        
        loc_id = input("\nLocation ID: ").strip()
        if loc_id not in self.game_data["locations"]:
            print("❌ Location not found!")
            return
        
        action_text = input("Action text: ").strip()
        action_id = f"act_{len(self.game_data['locations'][loc_id]['actions'])}"
        
        print("\nAction type:")
        print("1. Go to location")
        print("2. Take item")
        print("3. Check condition")
        print("4. Change variable")
        print("5. End game")
        
        type_choice = input("Choose type (1-5): ").strip()
        
        action_data = {"text": action_text, "type": "goto"}
        
        if type_choice == "1":
            print("Available locations:")
            for t_loc_id in self.game_data["locations"]:
                print(f"  - {t_loc_id}")
            target = input("Target location ID: ").strip()
            if target in self.game_data["locations"]:
                action_data["target"] = target
            else:
                print("❌ Location not found!")
                return
        elif type_choice == "2":
            action_data["type"] = "take"
            action_data["item"] = input("Item name: ").strip()
        elif type_choice == "3":
            action_data["type"] = "condition"
            action_data["var"] = input("Variable name: ").strip()
            action_data["value"] = input("Value: ").strip()
            action_data["true"] = input("If TRUE (location ID): ").strip()
            action_data["false"] = input("If FALSE (location ID): ").strip()
        elif type_choice == "4":
            action_data["type"] = "setvar"
            action_data["var"] = input("Variable name: ").strip()
            action_data["op"] = input("Operation (=, +, -): ").strip()
            action_data["val"] = input("Value: ").strip()
        elif type_choice == "5":
            action_data["type"] = "end"
            action_data["message"] = input("Final message: ").strip()
        
        self.game_data["locations"][loc_id]["actions"][action_id] = action_data
        print(f"✅ Action added!")
    
    def delete_action(self):
        """Delete an action from a location"""
        if not self.game_data["locations"]:
            print("❌ No locations!")
            return
        
        print("\n=== DELETE ACTION ===")
        print("Available locations:")
        for loc_id, loc in self.game_data["locations"].items():
            print(f"\n📍 {loc_id}: {loc['name']}")
            if loc['actions']:
                for act_id, act in loc['actions'].items():
                    print(f"   [{act_id}] {act['text']}")
            else:
                print("   ⚠️ No actions")
        
        loc_id = input("\nLocation ID: ").strip()
        if loc_id not in self.game_data["locations"]:
            print("❌ Location not found!")
            return
        
        if not self.game_data["locations"][loc_id]['actions']:
            print("❌ No actions in this location!")
            return
        
        print("\nActions in this location:")
        actions = list(self.game_data["locations"][loc_id]['actions'].items())
        for i, (act_id, act) in enumerate(actions, 1):
            print(f"{i}. {act['text']}")
        
        try:
            choice = int(input("\nWhich action to delete? (number): ")) - 1
            if 0 <= choice < len(actions):
                act_id, action = actions[choice]
                del self.game_data["locations"][loc_id]['actions'][act_id]
                print(f"✅ Action '{action['text']}' deleted!")
            else:
                print("❌ Invalid number!")
        except ValueError:
            print("❌ Enter a number!")
    
    def save_game(self):
        filename = input("File name (without .py): ").strip()
        full_path = os.path.join(self.games_folder, filename + ".py")
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_code())
        
        print(f"✅ Game saved to '{full_path}'!")
    
    def _generate_code(self):
        locations_json = json.dumps(self.game_data['locations'], ensure_ascii=False, indent=2)
        start_loc = self.game_data['start_location']
        
        code = '# ' + self.game_data['name'] + '\n'
        code += '# Author: ' + self.game_data['author'] + '\n'
        code += '# Created: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n\n'
        code += 'import time\n\n'
        code += 'def print_slow(text):\n'
        code += '    for char in text:\n'
        code += '        print(char, end=\'\', flush=True)\n'
        code += '        time.sleep(0.02)\n'
        code += '    print()\n\n'
        code += 'locations = ' + locations_json + '\n'
        code += 'variables = {}\n'
        code += 'inventory = []\n\n'
        code += 'def play():\n'
        code += '    current = "' + start_loc + '"\n\n'
        code += '    while True:\n'
        code += '        if current not in locations:\n'
        code += '            print("Error!")\n'
        code += '            break\n\n'
        code += '        loc = locations[current]\n'
        code += '        print_slow("\\n📍 " + loc["name"])\n'
        code += '        print_slow(loc["description"])\n\n'
        code += '        if not loc["actions"]:\n'
        code += '            print("\\n⏹️ The End!")\n'
        code += '            break\n\n'
        code += '        actions = list(loc["actions"].items())\n'
        code += '        for i, (act_id, act) in enumerate(actions, 1):\n'
        code += '            print(f"{i}. {act["text"]}")\n\n'
        code += '        try:\n'
        code += '            choice = int(input("\\n👉 Choose: ")) - 1\n'
        code += '            if choice < 0 or choice >= len(actions):\n'
        code += '                print("❌ Invalid choice!")\n'
        code += '                continue\n\n'
        code += '            act_id, action = actions[choice]\n\n'
        code += '            if action["type"] == "goto":\n'
        code += '                current = action["target"]\n'
        code += '            elif action["type"] == "take":\n'
        code += '                inventory.append(action["item"])\n'
        code += '                print(f"✅ Took: {action["item"]}")\n'
        code += '            elif action["type"] == "setvar":\n'
        code += '                var = action["var"]\n'
        code += '                val = action["val"]\n'
        code += '                op = action.get("op", "=")\n'
        code += '                if op == "=":\n'
        code += '                    variables[var] = val\n'
        code += '                elif op == "+":\n'
        code += '                    variables[var] = str(int(variables.get(var, 0)) + int(val))\n'
        code += '                elif op == "-":\n'
        code += '                    variables[var] = str(int(variables.get(var, 0)) - int(val))\n'
        code += '                print(f"📊 {var} = {variables[var]}")\n'
        code += '            elif action["type"] == "condition":\n'
        code += '                if str(variables.get(action["var"], "")) == str(action["value"]):\n'
        code += '                    next_loc = action["true"]\n'
        code += '                else:\n'
        code += '                    next_loc = action["false"]\n'
        code += '                if next_loc == "end":\n'
        code += '                    print_slow("\\n🎬 " + action.get("message", "The End!"))\n'
        code += '                    break\n'
        code += '                else:\n'
        code += '                    current = next_loc\n'
        code += '            elif action["type"] == "end":\n'
        code += '                print_slow("\\n🎬 " + action["message"])\n'
        code += '                break\n'
        code += '        except:\n'
        code += '            print("❌ Error!")\n\n'
        code += 'if __name__ == "__main__":\n'
        code += '    print("=" * 50)\n'
        code += '    print("🎮 " + locations["' + start_loc + '"]["name"])\n'
        code += '    print("=" * 50)\n'
        code += '    play()\n'
        return code
    
    def run(self):
        while True:
            print("\n" + "=" * 50)
            print("🎮 TEXT ADVENTURE BUILDER (ENG)")
            print("=" * 50)
            print(f"📁 Folder: {self.games_folder}")
            print(f"Name: {self.game_data['name']}")
            print(f"Locations: {len(self.game_data['locations'])}")
            print("-" * 50)
            print("1. 📍 Create location")
            print("2. ➕ Create action")
            print("3. ❌ Delete action")
            print("4. 📋 List locations")
            print("5. 💾 Save game")
            print("6. 🚪 Exit")
            
            choice = input("\n👉 Choose: ").strip()
            
            if choice == "1":
                self.create_location()
            elif choice == "2":
                self.create_action()
            elif choice == "3":
                self.delete_action()
            elif choice == "4":
                for loc_id, loc in self.game_data["locations"].items():
                    print(f"\n📍 {loc_id}: {loc['name']}")
                    print(f"   Desc: {loc['description']}")
                    if loc['actions']:
                        for act_id, act in loc['actions'].items():
                            print(f"     • {act['text']}")
            elif choice == "5":
                self.save_game()
            elif choice == "6":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice")

if __name__ == "__main__":
    game = GameBuilderEnglish()
    game.run()