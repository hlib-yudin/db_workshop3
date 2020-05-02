import csv
import cx_Oracle

username = 'Yudin'
password = 'yudin'
databaseName = 'localhost/xe'

connection = cx_Oracle.connect(username, password, databaseName)
cursor = connection.cursor()
tables = ['TEDTalk', 'Person', 'SpeechPerson', 'Rating', 
    'SpeechRating', 'TEDEvent', 'Video']

try:
    for table in tables:

        # відкриваємо csv-файл для обраної таблиці
        with open(table + '.csv', 'w', newline='') as csv_file:
            query = 'SELECT * FROM ' + table
            cursor.execute(query)
            row = cursor.fetchone()

            # отримуємо заголовок таблиці, записуємо в csv-файл
            headers = tuple(map(lambda x: x[0], cursor.description))
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(headers)

            # зчитуємо рядки таблиці, записуємо в csv_file
            while row:
                csv_writer.writerow(row)
                row = cursor.fetchone()

finally:
    cursor.close()
    connection.close()
