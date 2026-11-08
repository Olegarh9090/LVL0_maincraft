import random

chance_enemys = {"Зомби": 2, "Скелет": 2, "Крипер": 4}
strength_enemys = {"Зомби": 1, "Скелет": 2, "Крипер": 5}
chance_things = {"Кожа": 6, "Железо": 4, "Алмаз": 20}
inventory = {"Кожа": 0, "Железо": 0, "Алмаз": 0}
all_crafts = {
"Железный меч (урон 4)": ("Железо", 2),
"Алмазный меч (урон 7)": ("Алмаз", 2),

"Кожаный шлем (+0.5 броня)": ("Кожа", 5, 0.5),
"Кожаный нагрудник (+1 броня)": ("Кожа", 8, 1),
"Кожаные поножи (+1 броня)": ("Кожа", 7, 1),
"Кожаные сапоги (+0.5 броня)": ("Кожа", 4, 0.5),

"Железный шлем (+1 броня)": ("Железо", 5, 1),
"Железный нагрудник (+2 броня)": ("Железо", 8, 2),
"Железные поножи (+2 броня)": ("Железо", 7, 2),
"Железные сапоги (+1 броня)": ("Железо", 4, 1),

"Алмазный шлем (+2 броня)": ("Алмаз", 5, 2),
"Алмазный нагрудник (+4 броня)": ("Алмаз", 8, 4),
"Алмазные поножи (+4 броня)": ("Алмаз", 7, 4),
"Алмазные сапоги (+2 броня)": ("Алмаз", 4, 2)
}

Armor_parts = []
Player_damage = 1
Player_Hp = 20
Player_armor = 0
Level = 0

def Random_events(events: dict) -> list:
    result_event = ""
    for event in events:
        num = random.randint(0, events[event])
        if(num == events[event]): 
            result_event = event
            break
    return result_event

def Fight(enemys: list):
    global Player_Hp
    global Player_damage
    global Player_armor
    danger = 0
    for enemy in enemys:
        danger += strength_enemys[enemy]
    if Player_damage < danger:
        damage = (danger // 2
                  ) * (danger // Player_damage) // (Player_armor + 1)
        Player_Hp -= damage
        print(f"Получино {damage} урона")
        if(Player_Hp > 0): print(f"Текущее здоровье {Player_Hp}")
        else: print("Вы погибли")
    else: print("Вы удачно сражались и не потратили ни одного HP")

def Go_to_mine():
    Get_space()
    print("====================")
    print("Ты в шахте")
    global Level
    # Проверка на монстров
    enemys = []
    for i in range(Level // 10 + 1):
        enemy = Random_events(chance_enemys)
        if(enemy != ""): enemys.append(enemy)
    if(len(enemys) == 0):
        print("Вы никого не встретели")
    else: 
        print(f"Вы встретели {enemys}")
        Fight(enemys)

    global Player_Hp
    if(Player_Hp > 0):
        Level += 1
        # Проверка на лут
        new_thing = Random_events(chance_things)
        if(new_thing != ""): 
            print(f"Вы добыли: {new_thing}")
            inventory[new_thing] += 1
        else: print("Вы ничего не добыли")

    input('нажмите "Enter" чтобы продолжить')

def Get_space():
    for _ in range(space): print()

def Get_state():
    global Player_Hp
    global Player_damage
    global Player_armor
    Get_space()
    print("====================")
    print(f"""
Статус:
HP: {Player_Hp}
Damage: {Player_damage}
Armor: {Player_armor}
LEVEL: {Level}
Кожа: {inventory["Кожа"]}
Железо: {inventory["Железо"]}
Алмазы: {inventory["Алмаз"]}""")
    input('нажмите "Enter" чтобы продолжить')

def CraftMenu():
    """Функция крафта вещей"""
    Get_space()
    print("====================")
    print("Меню крафта")
    print("Доступные крафты:")
    available_crafts = dict()
    craft_names = []

    for item in all_crafts:
        matirial = all_crafts[item][0]
        count = all_crafts[item][1]
        if(inventory[matirial] >= count and item.split()[1] not in Armor_parts):
            available_crafts[item] = all_crafts[item]

    for index, item in enumerate(available_crafts):
        matirial = all_crafts[item][0]
        count = all_crafts[item][1]
        print(f"{index}) {item}: стоимость = {count}, материал: {matirial}")
        craft_names.append(item)

    if(len(available_crafts) == 0): print("Нет доступных крафтов (слишком мало ресурсов/ либо вы уже скрафтили все что можно)")
    else: 
        input_ = input('Введите код доступного крафта или "q" для выхода: ')
        if(input_ != "q"):
            try:
                cod = int(input_)
                Craft(craft_names[cod])
            except ValueError:
                "Неправельный ввод"
    print()
    input('нажмите "Enter" чтобы продолжить')

def Craft(craft_name: str):
    """функция обработки крафта"""
    global Player_armor
    global Player_damage
    if craft_name == "Железный меч (урон 4)": Player_damage = 4
    elif craft_name == "Алмазный меч (урон 7)": Player_damage = 7
    else:
        Player_armor += all_crafts[craft_name][2]
        Armor_parts.append(craft_name.split()[1])
    inventory[all_crafts[craft_name][0]] -= all_crafts[craft_name][1]
    print(f"Вы скрафтили {craft_name}")

def chose_menu():
    """функция для выбора действия"""
    Get_space()
    print("====================")
    print("Меню выбора")
    print("""
Пойти в шахту - 1
Крафтить - 2
Статус - 3
""")
    input_ = input("Введите код действия:")
    if(str.isdigit(input_)):
        action = int(input_)
        match action:
            case 1: Go_to_mine()
            case 2: CraftMenu()
            case 3: Get_state()
            case _: print("Неправельный ввод")

try:
    space = int(input("Введите допустимое для вас количество строк между менюшками информации (нажмите 'Enter' для выбора по умолчанию): "))
except ValueError:
    space = 100

while Player_Hp > 0:
    """основной цикл игры"""
    chose_menu()
print()
print("Конец игры")
print(f"Ваш уровень до смерти: {Level}")


