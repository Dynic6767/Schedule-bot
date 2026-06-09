import sqlite3
import random

conn = sqlite3.connect('schedule.db')
cursor = conn.cursor()
"""ЗАПИСИ ДЛЯ РАЗРОБОТЧИКОВ!
   Подключения и библеотеки, очевидно.
"""

cursor.execute('''
CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_number INTEGER,
    quarter INTEGER,
    day_of_week INTEGER,
    lesson_number INTEGER,
    subject TEXT,
    room TEXT
)
''')
conn.commit()
"""Создание таблицы"""

def get_lessons_count(class_number):
    """
    Определяет количество уроков в день для заданного класса.
    Чем больше класс, тем больше уроков.
    """
    if 1 <= class_number <= 2:
        return 4
    elif 3 <= class_number <= 4:
        return 5
    elif 5 <= class_number <= 7:
        return 6
    else:  
        return 7

def get_subjects_for_class(class_number):
    """
    Создаёт список предметов, изучаемых в заданном классе.
    Каждый класс добавляется урок (до 9),
    в 7 классе заменяет «Математику» на «Алгебру» и «Геометрию».
    """
    base = ['Русский язык', 'Математика', 'Физкультура', 'Литература']
    subjects = base.copy()

    if class_number >= 3:
        subjects.append('Музыка')
    if class_number >= 4:
        subjects.append('ИЗО')
    if class_number >= 5:
        subjects.extend(['География', 'Биология'])
    if class_number >= 6:
        subjects.append('Информатика')
    if class_number >= 7:
        if 'Математика' in subjects:
            subjects.remove('Математика')
        subjects.extend(['Алгебра', 'Геометрия'])
    if class_number >= 8:
        subjects.append('Химия')

    return subjects

class_room_pools = {}

def generate_room_pool(class_number, pool_size=4):
    """Генерирует набор кабинетов для класса (по умолчанию 4 кабинета)."""
    pool = []
    for _ in range(pool_size):
        if class_number <= 4:
            block = random.choice(['1', '2'])
        else:
            block = random.choice(['3', '4'])

        floor = random.randint(1, 3)
        room_num = random.randint(10, 30)

        pool.append(f"{block}-{floor}-{room_num:02d}")
    return pool

def get_room(class_number):
    """
    Возвращает случайный кабинет из закреплённого набора для класса.
    Для 1–4 классов кабинеты в блоках 1 или 2, для 5–11 — в блоках 3 или 4.
    Кабинеты меняются каждый класс, у каждого урока свой кабинет.
    """
    if class_number not in class_room_pools:
        class_room_pools[class_number] = generate_room_pool(class_number)

    return random.choice(class_room_pools[class_number])
 

def fill_database():
    """
    Заполняет базу данных расписанием для всех классов (1–11), четвертей (1–4) и дней недели (1–5).
    Учитывает сокращение количества уроков в 4-й четверти.
    Подбирает предметы из списка для класса и присваивает кабинет.
    Выполняет массовую вставку записей в таблицу lessons.
    """
    quarters = [1, 2, 3, 4] 
    days_of_week = [1, 2, 3, 4, 5]  

    for class_num in range(1, 12):
        subjects = get_subjects_for_class(class_num)
        max_lessons = get_lessons_count(class_num)

        for quarter in quarters:
            lessons_in_day = max_lessons - 1 if quarter == 4 else max_lessons

            for day in days_of_week:
                for lesson_num in range(1, lessons_in_day + 1):
                    subject = subjects[(lesson_num - 1) % len(subjects)]
                    room = get_room(class_num)  

                    cursor.execute('''
                        INSERT INTO lessons (class_number, quarter, day_of_week, lesson_number, subject, room)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (class_num, quarter, day, lesson_num, subject, room))

    conn.commit()

fill_database()
conn.close()
"""Заполняет таблицу"""