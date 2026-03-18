import os
import json
from datetime import datetime

class КонструкторИгрРусский:
    def __init__(self):
        self.game_data = {
            "name": "Моя текстовая игра",
            "author": "Неизвестен",
            "start_location": None,
            "locations": {},
            "variables": {},
            "items": {}
        }
        self.games_folder = "Мои_игры"
        if not os.path.exists(self.games_folder):
            os.makedirs(self.games_folder)
    
    def create_location(self):
        """Создание новой локации"""
        print("\n=== СОЗДАНИЕ ЛОКАЦИИ ===")
        loc_id = input("ID локации: ").strip()
        
        if loc_id in self.game_data["locations"]:
            print("❌ Локация уже существует!")
            return
        
        name = input("Название локации: ").strip()
        desc = input("Описание локации: ").strip()
        
        self.game_data["locations"][loc_id] = {
            "name": name,
            "description": desc,
            "actions": {}
        }
        
        print(f"✅ Локация '{name}' создана!")
        
        if not self.game_data.get("start_location"):
            self.game_data["start_location"] = loc_id
            print("⭐ Начальная локация!")
    
    def create_action(self):
        """Создание действия в локации"""
        if not self.game_data["locations"]:
            print("❌ Сначала создай локацию!")
            return
        
        print("\n=== СОЗДАНИЕ ДЕЙСТВИЯ ===")
        print("Доступные локации:")
        for loc_id in self.game_data["locations"]:
            print(f"  - {loc_id}: {self.game_data['locations'][loc_id]['name']}")
        
        loc_id = input("\nID локации: ").strip()
        if loc_id not in self.game_data["locations"]:
            print("❌ Локация не найдена!")
            return
        
        action_text = input("Текст действия: ").strip()
        action_id = f"act_{len(self.game_data['locations'][loc_id]['actions'])}"
        
        print("\nТип действия:")
        print("1. Переход")
        print("2. Взять предмет")
        print("3. Проверить условие")
        print("4. Изменить переменную")
        print("5. Конец игры")
        
        type_choice = input("Выбери тип (1-5): ").strip()
        
        action_data = {"text": action_text, "type": "goto"}
        
        if type_choice == "1":
            print("Доступные локации:")
            for t_loc_id in self.game_data["locations"]:
                print(f"  - {t_loc_id}")
            target = input("ID целевой локации: ").strip()
            if target in self.game_data["locations"]:
                action_data["target"] = target
            else:
                print("❌ Локация не найдена!")
                return
        elif type_choice == "2":
            action_data["type"] = "take"
            action_data["item"] = input("Название предмета: ").strip()
        elif type_choice == "3":
            action_data["type"] = "condition"
            action_data["var"] = input("Имя переменной: ").strip()
            action_data["value"] = input("Значение: ").strip()
            action_data["true"] = input("Если ДА (ID локации): ").strip()
            action_data["false"] = input("Если НЕТ (ID локации): ").strip()
        elif type_choice == "4":
            action_data["type"] = "setvar"
            action_data["var"] = input("Имя переменной: ").strip()
            action_data["op"] = input("Операция (=, +, -): ").strip()
            action_data["val"] = input("Значение: ").strip()
        elif type_choice == "5":
            action_data["type"] = "end"
            action_data["message"] = input("Финальное сообщение: ").strip()
        
        self.game_data["locations"][loc_id]["actions"][action_id] = action_data
        print(f"✅ Действие добавлено!")
    
    # ===== НОВАЯ ФУНКЦИЯ УДАЛЕНИЯ =====
    def delete_action(self):
        """Удаление действия из локации"""
        if not self.game_data["locations"]:
            print("❌ Нет локаций!")
            return
        
        print("\n=== УДАЛЕНИЕ ДЕЙСТВИЯ ===")
        print("Доступные локации:")
        for loc_id, loc in self.game_data["locations"].items():
            print(f"\n📍 {loc_id}: {loc['name']}")
            if loc['actions']:
                for act_id, act in loc['actions'].items():
                    print(f"   [{act_id}] {act['text']}")
            else:
                print("   ⚠️ Нет действий")
        
        loc_id = input("\nID локации: ").strip()
        if loc_id not in self.game_data["locations"]:
            print("❌ Локация не найдена!")
            return
        
        if not self.game_data["locations"][loc_id]['actions']:
            print("❌ В этой локации нет действий!")
            return
        
        print("\nДействия в локации:")
        actions = list(self.game_data["locations"][loc_id]['actions'].items())
        for i, (act_id, act) in enumerate(actions, 1):
            print(f"{i}. {act['text']}")
        
        try:
            choice = int(input("\nКакое действие удалить? (номер): ")) - 1
            if 0 <= choice < len(actions):
                act_id, action = actions[choice]
                del self.game_data["locations"][loc_id]['actions'][act_id]
                print(f"✅ Действие '{action['text']}' удалено!")
            else:
                print("❌ Неверный номер!")
        except ValueError:
            print("❌ Введи число!")
    
    def save_game(self):
        filename = input("Имя файла (без .py): ").strip()
        full_path = os.path.join(self.games_folder, filename + ".py")
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(self._generate_code())
        
        print(f"✅ Игра сохранена в '{full_path}'!")
    
    def _generate_code(self):
        locations_json = json.dumps(self.game_data['locations'], ensure_ascii=False, indent=2)
        start_loc = self.game_data['start_location']
        
        code = '# ' + self.game_data['name'] + '\n'
        code += '# Автор: ' + self.game_data['author'] + '\n'
        code += '# Создано: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n\n'
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
        code += '            print("Ошибка!")\n'
        code += '            break\n\n'
        code += '        loc = locations[current]\n'
        code += '        print_slow("\\n📍 " + loc["name"])\n'
        code += '        print_slow(loc["description"])\n\n'
        code += '        if not loc["actions"]:\n'
        code += '            print("\\n⏹️ Конец!")\n'
        code += '            break\n\n'
        code += '        actions = list(loc["actions"].items())\n'
        code += '        for i, (act_id, act) in enumerate(actions, 1):\n'
        code += '            print(f"{i}. {act["text"]}")\n\n'
        code += '        try:\n'
        code += '            choice = int(input("\\n👉 Выбери: ")) - 1\n'
        code += '            if choice < 0 or choice >= len(actions):\n'
        code += '                print("❌ Неверный выбор!")\n'
        code += '                continue\n\n'
        code += '            act_id, action = actions[choice]\n\n'
        code += '            if action["type"] == "goto":\n'
        code += '                current = action["target"]\n'
        code += '            elif action["type"] == "take":\n'
        code += '                inventory.append(action["item"])\n'
        code += '                print(f"✅ Взял: {action["item"]}")\n'
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
        code += '                    print_slow("\\n🎬 " + action.get("message", "Конец!"))\n'
        code += '                    break\n'
        code += '                else:\n'
        code += '                    current = next_loc\n'
        code += '            elif action["type"] == "end":\n'
        code += '                print_slow("\\n🎬 " + action["message"])\n'
        code += '                break\n'
        code += '        except:\n'
        code += '            print("❌ Ошибка!")\n\n'
        code += 'if __name__ == "__main__":\n'
        code += '    print("=" * 50)\n'
        code += '    print("🎮 " + locations["' + start_loc + '"]["name"])\n'
        code += '    print("=" * 50)\n'
        code += '    play()\n'
        return code
    
    def run(self):
        while True:
            print("\n" + "=" * 50)
            print("🎮 КОНСТРУКТОР ТЕКСТОВЫХ ИГР (RUS)")
            print("=" * 50)
            print(f"📁 Папка: {self.games_folder}")
            print(f"Название: {self.game_data['name']}")
            print(f"Локаций: {len(self.game_data['locations'])}")
            print("-" * 50)
            print("1. 📍 Создать локацию")
            print("2. ➕ Создать действие")
            print("3. ❌ Удалить действие")  # НОВОЕ!
            print("4. 📋 Список локаций")
            print("5. 💾 Сохранить игру")
            print("6. 🚪 Выход")
            
            choice = input("\n👉 Выбери: ").strip()
            
            if choice == "1":
                self.create_location()
            elif choice == "2":
                self.create_action()
            elif choice == "3":  # НОВОЕ!
                self.delete_action()
            elif choice == "4":
                for loc_id, loc in self.game_data["locations"].items():
                    print(f"\n📍 {loc_id}: {loc['name']}")
                    print(f"   Опис: {loc['description']}")
                    if loc['actions']:
                        for act_id, act in loc['actions'].items():
                            print(f"     • {act['text']}")
            elif choice == "5":
                self.save_game()
            elif choice == "6":
                print("👋 Пока!")
                break
            else:
                print("❌ Неверный выбор")

if __name__ == "__main__":
    game = КонструкторИгрРусский()
    game.run()