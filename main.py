import cx_Oracle
import plotly.offline as py
import plotly.graph_objs as go

username = 'Yudin'
password = 'yudin'
databaseName = 'localhost/xe'

connection = cx_Oracle.connect(username, password, databaseName)
cursor = connection.cursor()

"""-------------------------------------------------------------------------------------
Запит 1 - вивести топ-10 спікерів, загальна тривалість виступів яких найбільша, та загальну 
тривалість усіх їхніх виступів."""

query = '''
SELECT *
FROM (
        SELECT
            person_name
            , SUM(duration_sec) as total_duration_sec
        FROM
            PersonSpeechDuration
        GROUP BY person_name
        ORDER BY SUM(duration_sec) DESC
        
) WHERE ROWNUM <= 10'''

cursor.execute(query)
person_names = []
total_duration_sec = []

row = cursor.fetchone()
while row:
    person_names.append(row[0])
    duration = divmod(row[1], 60)
    duration_formatted = '{}:{:0<2}'.format(duration[0], str(duration[1]))
    total_duration_sec.append(row[1])
    row = cursor.fetchone()


bar = [go.Bar(
    x=person_names,
    y=total_duration_sec
)]
layout = go.Layout(
    # title='Спікери та загальна тривалість їхніх виступів -- топ-10',
    xaxis={
        'title':'Спікери'
    },
    yaxis={
        'title':'Тривалість'
    },
    annotations=[
        go.layout.Annotation(
            x=x,
            y=y,
            text=str(y//3600) + ':' + str(y//60%60) + ':' + '{:02}'.format(y%60)
        )
    for x,y in zip(person_names, total_duration_sec)]
)

fig = go.Figure(data=bar, layout=layout)

url_1 = py.plot(fig, filename='Спікер-загальна тривалість.html')

"""----------------------------------------------------------------------
Запит 2 - для виступів з TED2014 вивести рейтинг (Funny, Inspiring, Beautiful...) 
та відсоток виступів, у яких переважає цей рейтинг."""

query = '''
SELECT 
    Rating.rating_name
    , NVL(speech_count, 0) AS speech_count
FROM 
    -- об'єднуємо з Rating, бо в temp1 будуть присутні не всі рейтинги
    Rating
    LEFT JOIN (
    
            -- рейтинг -- к-сть виступів, в яких переважає цей рейтинг
            SELECT
                e.primary_rating_name
                , COUNT(e.speech_name) as speech_count
            FROM
                EventSpeechPrimaryRating e
            WHERE 
                event = 'TED2014'
            GROUP BY
                e.primary_rating_name
            
    ) temp1 ON Rating.rating_name = temp1.primary_rating_name
'''

cursor.execute(query)
rating_names = []
speech_count = []

row = cursor.fetchone()
while row:

    rating_names.append(row[0])
    speech_count.append(row[1])
    row = cursor.fetchone()

pie = go.Pie(labels=rating_names, values=speech_count)
url_2 = py.plot([pie], filename='Рейтинг-відсоток.html')

"""------------------------------------------------------------------------
Запит 3 - вивести динаміку переглядів виступів на ted.com по роках (за всі роки)."""

query = '''
--крок 2: згрупувати за роками
SELECT
    EXTRACT(YEAR FROM film_date) AS year,
    SUM(views) AS total_views
FROM 
    TEDTalk JOIN Video
        ON TEDTalk.url = Video.url

        
GROUP BY EXTRACT(YEAR FROM film_date)
ORDER BY year'''

cursor.execute(query)
years = []
views = []

row = cursor.fetchone()
while row:

    years.append(row[0])
    views.append(row[1])
    row = cursor.fetchone()

scatter = go.Scatter(
    x=years,
    y=views,
    mode='lines+markers'
)
url_3 = py.plot([scatter], filename='Дата-перегляди.html')

connection.close()

