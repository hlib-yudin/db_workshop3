DECLARE
    -- кількість рядків для вставки
    max_num_rows INT NOT NULL DEFAULT 5;

BEGIN 
    
    -- таблиця SpeechRating зв'язана з іншими таблицями зовнішніми ключами
    -- щоб не виникло помилки цілісності даних, слід спочатку заповнити батьківські таблиці також тестовими даними
    
    DELETE FROM SpeechRating;
    DELETE FROM Rating;
    DELETE FROM TEDTalk;
    DELETE FROM TEDEvent;

    insert into tedevent (event) values ('TED2006');
    
    FOR i in 1..max_num_rows LOOP
        INSERT INTO rating (rating_name) values ('rating' || i);
    END LOOP;
    
    INSERT INTO tedtalk (speech_name, description, duration_sec, event, film_date, url)
        VALUES ('speech1', 'description', 100, 'TED2006', TO_DATE('04-20-2006', 'MM-DD-YYYY'), 'url');
        
        
    -- сам цикл і заповнення таблиці

    FOR i IN 1..max_num_rows LOOP
    
        INSERT INTO SpeechRating (speech_name, rating_name, rating_value)
            VALUES ('speech1', 'rating' || i, i*100);
    
    END LOOP;
    
END;

-- розкоментуйте, щоб перевірити, що таблиця дійсно заповнилася
--select * from speechrating;
