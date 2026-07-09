import random
import time

# -----------------------------ФУНКЦИИ-----------------------------

# Интерфейс стартового меню
def start_menu():
    print(f"1. Начать игру") # Начать игру
    print(f"0. Выход") # Выйти из игры
    print(f"------------------") # Пунктирная линия для UI

# Визуализация поля игры
def display_field(game_field):
    
    row_num = 0 # Счётчик строк
    
    for row in game_field: # Вывод полей
        row_num += 1
        print(f"{row_num}.", *row)
    print('----------------------------------------')

# Обработка выбранного поля игроком/ботом
def hero_choice(game_field, move, hero, is_bot_move=False):
    found_field = 0 # Номер найденного поля (по умолчанию 0)

    # if is_win_check(game_field):
    for i in range(0, len(game_field)):
        for j in range(0, len(game_field)):
            found_field += 1
            
            if found_field == move and game_field[i][j] == '-':
                game_field[i][j] = hero
                return True
            elif found_field == move and game_field[i][j] != '-' and is_bot_move:
                # print("Бот сделал ход на занятое поле!")
                return False
            elif found_field == move and game_field[i][j] != '-':
                print("Игрок, ты выбрал занятое поле!")
                return False
        
        if found_field == move:
                break
    # else:
    #     return True

# Визуализация ПОБЕДЫ Игрока <hero>
def display_winner(game_field, hero):
    print('-------------------WIN------------------')

    time.sleep(0.5)

    print(f'🏆 Победил {hero}')

    time.sleep(0.5)
    
    display_field(game_field)

# Функция сканирования поля
def is_win_check(game_field):
    
    n = len(game_field)

    total_line = [1 for i in range(0, n) if '-' in game_field[i]] # Счётчик пустых полей

    if 3 in [game_field[i].count('X') for i in range(0, n)]:
        display_winner(game_field, 'Крестик')
        return False
    elif 3 in [game_field[i].count('O') for i in range(0, n)]:
        display_winner(game_field, 'Нолик')
        return False
    else:
        total_x = []
        total_o = []

        # Парсинг элементов столбцов (Вертикальные победные комбинации)
        for i in range(0, n):
            for j in range(0, n):
                if game_field[j][i] == 'X':
                    total_x.append(1)
                elif game_field[j][i] == 'O':
                    total_o.append(1)

            if sum(total_x) == 3:
                display_winner(game_field, 'Крестик')

                return False
            elif sum(total_o) == 3:
                display_winner(game_field, 'Нолик')

                return False
            
            else:
                total_x = []
                total_o = []

        # Парсинг элементов по диагонали (Главной и Побочной)
        for i in range(0, n):
            if game_field[i][i] == 'X' or game_field[i][n-i-1] == 'X': # Главная/Побочная диагональ
                total_x.append(1)
            if game_field[i][i] == 'O' or game_field[i][n-i-1] == 'O': # Главная/Побочная диагональ
                total_o.append(1)

        if sum(total_x) == 3:
            display_winner(game_field, 'Крестик')
            return False
        
        elif sum(total_o) == 3:
            display_winner(game_field, 'Нолик')
            return False
        
        else:
            total_x = []
            total_o = []
        
    # Если пустых полей нет, то конец игры
    if sum(total_line) == 0:
        display_field(game_field)
        print('Игра кончилась.')
        return False
    # Иначе игра продолжается
    else:
        return True
    
# ---------------------------------------------------------------------------------------
         
# --------------------------------------НАЧАЛО ИГРЫ--------------------------------------

start_menu() # Стартовое меню
main_menu = int(input(": ")) # Номер Пункта меню
while main_menu != 0:

    field = [
                ['-', '-', '-',],
                ['-', '-', '-',],
                ['-', '-', '-',],
        ]

    if main_menu == 1:
        print("1. За крестик")
        print("2. За нолик")

        hero_num = int(input("За кого хочешь играть?: "))

        if hero_num == 1:
            print("Ты выбрал Крестик (Х)")
            print("Игра началась.")
            print("----------------------")

            while is_win_check(field):
        
                display_field(field)
                
                player_move = int(input("Выбери позицию куда сделать ход (от 1 до 9): "))
                bot_move = random.randint(1, 9)

                if player_move > 9 or player_move < 1:
                    print("Введите число в диапазоне от 1 до 9!")
                else:
                    while hero_choice(field, player_move, 'X') == False:
                        player_move = int(input("Выбери позицию куда сделать ход (от 1 до 9): "))

                    while hero_choice(field, bot_move, 'O', True) == False:
                        bot_move = random.randint(1, 9)

        elif hero_num == 2:
            print("Ты выбрал Нолик (O)")
            print("Игра началась.")
            print("----------------------")

            while is_win_check(field):

                display_field(field)

                player_move = int(input("Выбери позицию куда сделать ход (от 1 до 9): "))
                bot_move = random.randint(1, 9)

                if player_move > 9 or player_move < 1:
                    print("Введите число в диапазоне от 1 до 9!")
                else:
                    while hero_choice(field, player_move, 'O') == False:
                        player_move = int(input("Выбери позицию куда сделать ход (от 1 до 9): "))

                    while hero_choice(field, bot_move, 'X', True) == False:
                        bot_move = random.randint(1, 9)
        else:
            print("Введи цифру 1 или 2")

    start_menu()
    main_menu = int(input(": "))

# =========Задачи==========
# ✅ Удалить баг двойного вывода
# =========Доработки==========
# . . .
