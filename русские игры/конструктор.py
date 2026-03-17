import os
import json
from datetime import datetime

class TextGameConstructor:
    def __init__(self):
        self.game_data = {
            "name": "Моя текстовая игра",
            "author": "Неизвестен",
            "start_location": "start",
            "locations": {},
            "variables": {},
            "items": {}
        }
        self.current_location = None
    
    def create_location(self):
        """Создание новой локации"""
        print("\n=== СОЗДАНИЕ ЛОКАЦИИ ===")
        loc_id = input("ID локации (например 'forest'): ").strip()
        
        if loc_id in self.game_data["locations"]:
            print("❌ Локация с таким ID уже существует!")
            return
        
        name = input("Название локации: ").strip()
        desc = input("Описание локации: ").strip()
        
        self.game_data["locations"][loc_id] = {
            "name": name,
            "description": desc,
            "actions": {}
        }
        
        print(f"✅ Локация '{name}' создана!")
        
        if not self.game_data["start_location"]:
            self.game_data["start_location"] = loc_id
            print("⭐ Эта локация установлена как начальная!")
    
    def create_action(self):
        """Создание действия в локации"""
        if not self.game_data["locations"]:
            print("❌ Сначала создайте хотя бы одну локацию!")
            return
        
        print("\n=== СОЗДАНИЕ ДЕЙСТВИЯ ===")
        print("Доступные локации:")
        for loc_id in self.game_data["locations"]:
            print(f"  - {loc_id}: {self.game_data['locations'][loc_id]['name']}")
        
        loc_id = input("\nID локации для действия: ").strip()
        if loc_id not in self.game_data["locations"]:
            print("❌ Локация не найдена!")
            return
        
        action_text = input("Текст действия (например 'пойти налево'): ").strip()
        action_id = f"act_{len(self.game_data['locations'][loc_id]['actions'])}"
        
        print("\nТип действия:")
        print("1. Переход в другую локацию")
        print("2. Взять предмет")
        print("3. Проверить условие")
        print("4. Изменить переменную")
        print("5. Конец игры")
        
        type_choice = input("Выбери тип (1-5): ").strip()
        
        action_data = {
            "text": action_text,
            "type": "goto"
        }
        
        if type_choice == "1":
            print("\nДоступные локации для перехода:")
            for t_loc_id in self.game_data["locations"]:
                print(f"  - {t_loc_id}: {self.game_data['locations'][t_loc_id]['name']}")
            target = input("ID целевой локации: ").strip()
            if target in self.game_data["locations"]:
                action_data["target"] = target
            else:
                print("❌ Локация не найдена!")
                return
        
        elif type_choice == "2":
            item = input("Название предмета: ").strip()
            action_data["type"] = "take"
            action_data["item"] = item
        
        elif type_choice == "3":
            var = input("Имя переменной: ").strip()
            val = input("Значение для проверки: ").strip()
            print("\nДействие при ИСТИНЕ:")
            print("Введи ID локации или 'end' для конца игры")
            true_action = input("→ ").strip()
            print("Действие при ЛЖИ:")
            false_action = input("→ ").strip()
            
            action_data["type"] = "condition"
            action_data["var"] = var
            action_data["value"] = val
            action_data["true"] = true_action
            action_data["false"] = false_action
        
        elif type_choice == "4":
            var = input("Имя переменной: ").strip()
            op = input("Операция (=, +, -): ").strip()
            val = input("Значение: ").strip()
            
            action_data["type"] = "setvar"
            action_data["var"] = var
            action_data["op"] = op
            action_data["val"] = val
        
        elif type_choice == "5":
            action_data["type"] = "end"
            message = input("Финальное сообщение: ").strip()
            action_data["message"] = message
        
        self.game_data["locations"][loc_id]["actions"][action_id] = action_data
        print(f"✅ Действие добавлено в локацию '{loc_id}'!")
    
    def list_locations(self):
        """Показать все локации"""
        print("\n=== ЛОКАЦИИ ===")
        for loc_id, loc in self.game_data["locations"].items():
            print(f"\n📍 {loc_id}: {loc['name']}")
            print(f"   Описание: {loc['description']}")
            if loc['actions']:
                print("   Действия:")
                for act_id, act in loc['actions'].items():
                    print(f"     • {act['text']}")
            else:
                print("   ⚠️ Нет действий!")
    
    def save_game(self):
        """Сохранить игру как .py файл"""
        if not self.game_data["locations"]:
            print("❌ Нет локаций для сохранения!")
            return
        
        filename = input("Имя файла (без .py): ").strip() + ".py"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self._generate_game_code())
        
        print(f"✅ Игра сохранена как '{filename}'!")
        print("📁 Файл можно открыть в Pydroid и запустить!")
    
    def _generate_game_code(self):
        """Генерирует Python код игры"""
        code = f'''# {self.game_data['name']}
# Автор: {self.game_data['author']}
# Создано: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Сгенерировано конструктором текстовых игр

import time

def print_slow(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.02)
    print()

# Игровые данные
locations = {json.dumps(self.game_data['locations'], ensure_ascii=False, indent=2)}
variables = {json.dumps(self.game_data.get('variables', {}), ensure_ascii=False, indent=2)}
inventory = []

def check_condition(condition):
    if condition.startswith('has_item'):
        item = condition.split(':')[1]
        return item in inventory
    elif condition.startswith('var'):
        var_name, op, val = condition.split(':')[1:]
        if op == '==':
            return variables.get(var_name) == val
        elif op == '>':
            return int(variables.get(var_name, 0)) > int(val)
    return False

def play():
    current = '{self.game_data['start_location']}'
    
    while True:
        if current not in locations:
            print(f"❌ Ошибка: локация {{current}} не найдена!")
            break
        
        loc = locations[current]
        print_slow(f"\\n📍 {{loc['name']}}")
        print_slow(loc['description'])
        
        if not loc['actions']:
            print("\\n⏹️ Игра окончена!")
            break
        
        actions = list(loc['actions'].items())
        for i, (act_id, act) in enumerate(actions, 1):
            print(f"{i}. {act['text']}")
        
        try:
            choice = int(input("\\n👉 Выбери действие: ")) - 1
            if choice < 0 or choice >= len(actions):
                print("❌ Неверный выбор!")
                continue
            
            act_id, action = actions[choice]
            
            if action['type'] == 'goto':
                current = action['target']
            
            elif action['type'] == 'take':
                inventory.append(action['item'])
                print(f"✅ Ты взял: {action['item']}")
                current = action.get('next', current)
            
            elif action['type'] == 'setvar':
                var = action['var']
                val = action['val']
                op = action.get('op', '=')
                
                if op == '=':
                    variables[var] = val
                elif op == '+':
                    variables[var] = str(int(variables.get(var, 0)) + int(val))
                elif op == '-':
                    variables[var] = str(int(variables.get(var, 0)) - int(val))
                
                print(f"📊 Переменная {{var}} = {{variables[var]}}")
                current = action.get('next', current)
            
            elif action['type'] == 'condition':
                var_val = variables.get(action['var'], '')
                if str(var_val) == str(action['value']):
                    print("✅ Условие выполнено!")
                    next_loc = action['true']
                else:
                    print("❌ Условие не выполнено!")
                    next_loc = action['false']
                
                if next_loc == 'end':
                    print_slow(f"\\n🎬 {action.get('message', 'Конец игры!')}")
                    break
                else:
                    current = next_loc
            
            elif action['type'] == 'end':
                print_slow(f"\\n🎬 {action['message']}")
                break
            
        except ValueError:
            print("❌ Введи число!")
        except Exception as e:
            print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print(f"🎮 {locations['{self.game_data['start_location']}']['name']}")
    print("=" * 50)
    play()
'''
        return code
    
    def run(self):
        """Главное меню конструктора"""
        while True:
            print("\n" + "=" * 50)
            print("🎮 КОНСТРУКТОР ТЕКСТОВЫХ ИГР")
            print("=" * 50)
            print(f"Название: {self.game_data['name']}")
            print(f"Автор: {self.game_data['author']}")
            print(f"Локаций: {len(self.game_data['locations'])}")
            print("-" * 50)
            print("1. 📍 Создать локацию")
            print("2. ➕ Создать действие")
            print("3. 📋 Список локаций")
            print("4. ✏️ Изменить название/автора")
            print("5. 💾 Сохранить игру (.py)")
            print("6. 🚪 Выход")
            
            choice = input("\n👉 Выбери: ").strip()
            
            if choice == "1":
                self.create_location()
            elif choice == "2":
                self.create_action()
            elif choice == "3":
                self.list_locations()
            elif choice == "4":
                self.game_data['name'] = input("Новое название: ").strip()
                self.game_data['author'] = input("Новый автор: ").strip()
                print("✅ Обновлено!")
            elif choice == "5":
                self.save_game()
            elif choice == "6":
                print("👋 Пока!")
                break
            else:
                print("❌ Неверный выбор")

if __name__ == "__main__":
    constructor = TextGameConstructor()
    constructor.run()