import sqlite3

conn = sqlite3.connect('schedule.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_number INTEGER,
    quarter INTEGER,
    day_of_week INTEGER,
    lesson_number INTEGER,
    subject TEXT
)
''')
conn.commit()

def get_lessons_count(class_number):
    if 1 <= class_number <= 2:
        return 4
    elif 3 <= class_number <= 4:
        return 5
    elif 5 <= class_number <= 7:
        return 6
    else:  
        return 7

def get_subjects_for_class(class_number):
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

def fill_database():
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
                    
                    cursor.execute('''
                        INSERT INTO lessons (class_number, quarter, day_of_week, lesson_number, subject)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (class_num, quarter, day, lesson_num, subject))

    conn.commit()


