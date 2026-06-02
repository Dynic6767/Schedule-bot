import sqlite3

conn = sqlite3.connect('schedule.db')
cursor = conn.cursor()

def get_schedule(class_num, quarter, day_of_week):
    cursor.execute('''
        SELECT lesson_number, subject 
        FROM lessons 
        WHERE class_number = ? AND quarter = ? AND day_of_week = ?
        ORDER BY lesson_number
    ''', (class_num, quarter, day_of_week))
    
    lessons = cursor.fetchall()
    return lessons

def print_schedule(class_num, quarter, day_of_week):
    day_names = {1: 'Понедельник', 2: 'Вторник', 3: 'Среда', 4: 'Четверг', 5: 'Пятница'}
    schedule = get_schedule(class_num, quarter, day_of_week)
    
    if not schedule:
        print(f"Записей для {class_num} класса, {quarter} четверти и {day_names[day_of_week]} не найдено.")
        return
    
    print(f"\nРасписание для {class_num} класса на {quarter} четверть ({day_names[day_of_week]}):")
    for lesson_num, subject in schedule:
        print(f"{lesson_num}. {subject}")

def get_valid_class():
    while True:
        try:
            class_num = int(input("Введите номер класса (1-11): "))
            if 1 <= class_num <= 11:
                return class_num
            else:
                print("Такого класса не существует. Введите от 1-11. ")
        except ValueError:
            print("Введите число.")

def get_valid_quarter():
    while True:
        try:
            quarter = int(input("Выберите четверть (1-4): "))
            if 1 <= quarter <= 4:
                return quarter
            else:
                print("Такой четверти не существует. Введите от 1-11.")
        except ValueError:
            print("Введите число.")

def get_valid_day():
    while True:
        try:
            day = int(input("Выберите день недели (1-5): "))
            if 1 <= day <= 5:
                return day
            else:
                print("Такой четверти не существует. Введите от 1-11.")
        except ValueError:
            print("Введите число.")

class_num = get_valid_class()
quarter = get_valid_quarter()
day = get_valid_day()

print_schedule(class_num, quarter, day)