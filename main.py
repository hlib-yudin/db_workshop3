import cx_Oracle
import plotly.offline as py
import plotly.graph_objs as go

username = 'SYSTEM'
password = 'oracle'
databaseName = 'localhost/xe'

connection = cx_Oracle.connect(username, password, databaseName)
cursor = connection.cursor()

"""-------------------------------------------------------------------------------------
Запит 1 - вивести топ-10 спікерів, загальна тривалість виступів яких найбільша, та загальну 
тривалість усіх їхніх виступів."""

query = '''
-- крок 3 -- обрати топ-10    
SELECT 
    *
FROM (

        -- крок 2 -- сам запит
        SELECT 
            person_name
            , SUM(duration_sec) AS total_duration_sec
        FROM

                    -- крок 1 -- позбутися купи дублікатів, які виникли при 
                    -- JOIN-і всіх табличок
                    (SELECT DISTINCT
                        person_name
                        , speech_name
                        , duration_sec
                    FROM
                        AllTables)
                 
        GROUP BY person_name
        ORDER BY total_duration_sec DESC
) 
WHERE ROWNUM <= 10'''

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

url_1 = py.plot(fig, filename='desktop/db/lab3/Спікер-загальна тривалість.html')

"""----------------------------------------------------------------------
Запит 2 - для виступів з TED2014 вивести рейтинг (Funny, Inspiring, Beautiful...) 
та відсоток виступів, у яких переважає цей рейтинг."""

query = '''
--крок 4 -- LEFT JOIN з рейтингами
SELECT 
    Rating.rating_name
    , NVL(temp2.speech_count, 0) AS speech_count
    --якщо необхідно порахувати у відсотках
    --, NVL(ROUND(temp2.speech_count / temp3.total_speeches * 100, 2), 0) AS percentage
FROM 
    Rating 
    LEFT JOIN (
            
            --крок 3: обрати зі SpeechRating те, що отримали на кроці 2
            SELECT 
                SpeechRating.rating_name
                ,COUNT(*) as speech_count
            FROM (   
                        --крок 2: виступ -- максимальне rating_value
                        SELECT 
                            speech_name
                            ,MAX(rating_value) AS max_rating_value
                        FROM (
                        
                                -- крок 1 -- позбутися дублікатів
                                SELECT DISTINCT
                                    speech_name
                                    , rating_name
                                    , rating_value
                                    , event
                                FROM AllTables)
                                    
                            
                        WHERE
                            event = 'TED2014'
                        GROUP BY 
                            speech_name
                         
            -- крок 3            
            ) temp1 JOIN SpeechRating
                ON SpeechRating.speech_name = temp1.speech_name
                AND SpeechRating.rating_value = temp1.max_rating_value 
                    
            GROUP BY
                SpeechRating.rating_name
                
--крок 4                
) temp2 
    ON temp2.rating_name = Rating.rating_name
    
--якщо необхідно порахувати в відсотках
--, (SELECT COUNT(*) AS total_speeches FROM TEDTalk WHERE event = 'TED2014') temp3
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
url_2 = py.plot([pie], filename='desktop/db/lab3/Рейтинг-відсоток.html')

"""------------------------------------------------------------------------
Запит 3 - вивести динаміку переглядів виступів на ted.com по роках (за всі роки)."""

query = '''
--крок 2: згрупувати за роками
SELECT
    EXTRACT(YEAR FROM film_date) AS year,
    SUM(views) AS total_views
FROM (

        -- крок 1 -- позбутись дублікатів
        SELECT DISTINCT
            speech_name
            , film_date
            , views
        FROM AllTables)

        
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
url_3 = py.plot([scatter], filename='desktop/db/lab3/Дата-перегляди.html')

connection.close()

