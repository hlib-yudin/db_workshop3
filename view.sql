-- в умові завдання сказано вказати таблиці, що містяться в усіх запитах,
-- але в даному випадку це лише одна таблиця -- TEDTalk
-- представлення з однієї таблиці не допоможе реалізувати всі три запити
-- тому вирішено створити два представлення: перше -- для першого запиту, друге -- для другого


-- структура представлення:
-- ім'я людини -- назва його виступу -- тривалість цього виступу
CREATE OR REPLACE VIEW PersonSpeechDuration AS
    SELECT
        person_name
        , speech_name
        , duration_sec
    FROM
        TEDTalk
        JOIN SpeechPerson USING (speech_name);
        
        
        
-- структура представлення:
-- TEDEvent -- назва виступу -- рейтинг, який переважає в цьому виступі
CREATE OR REPLACE VIEW EventSpeechPrimaryRating AS

    --крок 2: event -- виступ -- primary_rating_name
    SELECT 
        TEDTalk.event as event
        , temp1.speech_name as speech_name
        , SpeechRating.rating_name as primary_rating_name
    FROM (   
                --крок 1: виступ -- максимальне rating_value серед усіх rating_name
                SELECT 
                    SpeechRating.speech_name as speech_name
                    , MAX(SpeechRating.rating_value) AS max_rating_value
                FROM 
                    SpeechRating 
                GROUP BY 
                    SpeechRating.speech_name
                 
        -- крок 2            
        ) temp1 JOIN SpeechRating
            ON SpeechRating.speech_name = temp1.speech_name
            AND SpeechRating.rating_value = temp1.max_rating_value
        JOIN TEDTalk
            ON TEDTalk.speech_name = temp1.speech_name
            
    ORDER BY TEDTalk.event;
    
