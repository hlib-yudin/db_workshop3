from csv import DictReader as csv_DictReader
from re import split as re_split
from ast import literal_eval 
from datetime import datetime
import cx_Oracle

# під'єднуємось до бази даних
username = 'Yudin'
password = 'yudin'
databaseName = 'localhost/xe'

connection = cx_Oracle.connect(username, password, databaseName)
cursor = connection.cursor()

# відкриваємо csv-файл
csv_file = open('ted_main.csv', errors='ignore')
csv_reader = csv_DictReader(csv_file)
line_num = 1


# деякі атрибути, що визначені як PK, можуть повторюватися
# вставлення рядків з такими атрибутами у таблицю викличе помилку
# створимо списки, які міститимуть унікальні значення цих атрибутів
event_unique = []
person_name_unique = []

# якщо в таблицях вже є дані -- видалимо їх
tables = ['Speechperson', 'SpeechRating', 'Person', 
    'Rating', 'Video', 'TEDTalk', 'TEDEvent']
for table in tables:
    cursor.execute("DELETE FROM " + table)


# оброблюємо csv-файл
try:
    for line in csv_reader:

        # зчитуємо атрибути, "підправляємо" дані
        description = line['description'].strip()
        duration_sec = int(line['duration'])
        event = line['event'].strip()
        film_date = datetime.fromtimestamp(int(line['film_date']))
        speech_name = line['name'].strip()
        url = line['url'].strip()
        views = int(line['views'])
        rating_dict_list = literal_eval(line['ratings'])

        # оскільки в атрибуті main_speaker датасету дані містять інформацію про
        # всіх спікерів одразу, її треба розбити
        person_name_list = re_split(',|\+| and ', line['main_speaker'])
        person_name_list = [name.strip() for name in person_name_list]

#------------------------------------------------------------------------------
        # вставляємо event в TEDEvent, слідкуємо за можливими повторами
        if event not in event_unique:
            event_unique.append(event)
            query = '''INSERT INTO TEDEvent (event) VALUES (:event)'''
            cursor.execute(query, event=event)

        # вставляємо інформацію в TEDTalk
        query = '''
        INSERT INTO TEDTalk (speech_name, description, duration_sec, event, film_date, url)
            VALUES (:speech_name, :description, :duration_sec, :event, :film_date, :url)'''
        cursor.execute(query, speech_name=speech_name, description=description, 
            duration_sec=duration_sec, event=event, film_date=film_date, url=url)

        # вставляємо інформацію в Video
        query = '''INSERT INTO Video (url, views) VALUES (:url, :views)'''
        cursor.execute(query, url=url, views=views)

        # вставляємо інформацію в Person i SpeechPerson
        # одному рядку з csv-файла можуть відповідати кілька людей
        # слідкуємо за повторами
        for person_name in person_name_list:
            if person_name not in person_name_unique:
                person_name_unique.append(person_name)
                query = '''INSERT INTO Person (person_name) VALUES (:person_name)'''
                cursor.execute(query, person_name=person_name)

            query = '''
                INSERT INTO SpeechPerson (person_name, speech_name)
                    VALUES (:person_name, :speech_name)'''
            cursor.execute(query, person_name=person_name, speech_name=speech_name)

        # вставляємо інформацію в SpeechRating (та в Rating)
        # одному рядку з csv-файлу відповідають 14 значень різних рейтингів
        for rating_dict in rating_dict_list:
            rating_name = rating_dict['name'].strip()
            rating_value = int(rating_dict['count'])

            # оскільки назви рейтингів в усіх csv-рядках однакові,
            # ми можемо вставити інофрмацію в Rating лише на основі першого рядка
            if line_num == 1:
                query = '''INSERT INTO Rating (rating_name) VALUES (:rating_name)'''
                cursor.execute(query, rating_name=rating_name)

            query = '''
                INSERT INTO SpeechRating (speech_name, rating_name, rating_value)
                    VALUES (:speech_name, :rating_name, :rating_value)'''
            cursor.execute(query, speech_name=speech_name, rating_name=rating_name,
                rating_value=rating_value)

#---------------------------------------------------------------------
        # відображаємо в консоль кількість вже оброблених рядків
        print(f'Inserted line {line_num}/2550')
        line_num += 1
        

# відстеження помилок та номера рядка, на якому сталася помилка
except:
    print(f'Error on the line {line_num}')
    raise

finally:
    # зберігаємо зміни, закриваємо файл і connection
    csv_file.close() 
    connection.commit()
    cursor.close()
    connection.close()


