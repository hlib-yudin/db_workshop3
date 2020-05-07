SET SERVEROUTPUT ON

BEGIN
    DBMS_OUTPUT.enable;
END;

/

DECLARE
    -- кількість рядків для вставки
    max_num_rows INT NOT NULL DEFAULT 5;
    -- змінні, що будуть містити атрибути таблиці
    v_speech_name TEDTalk.speech_name%TYPE;
    v_rating_name Rating.rating_name%TYPE;
    v_rating_value INT;

BEGIN 
    
    -- таблиця SpeechRating зв'язана з іншими таблицями зовнішніми ключами
    -- щоб не виникло помилки цілісності даних, слід спочатку заповнити батьківські таблиці також тестовими даними

    insert into tedevent (event) values ('TED0000');
    
    FOR i in 1..max_num_rows LOOP
        INSERT INTO rating (rating_name) values ('rating' || i);
    END LOOP;
    
    INSERT INTO tedtalk (speech_name, description, duration_sec, event, film_date, url)
        VALUES ('speech1', 'description', 100, 'TED0000', TO_DATE('04-20-2006', 'MM-DD-YYYY'), 'url');
        
        
    -- сам цикл і заповнення таблиці

    FOR i IN 1..max_num_rows LOOP
    
        INSERT INTO SpeechRating (speech_name, rating_name, rating_value)
            VALUES ('speech1', 'rating' || i, i*100);
            
        SELECT speech_name, rating_name, rating_value 
            INTO v_speech_name, v_rating_name, v_rating_value
            FROM SpeechRating
            WHERE rating_name = 'rating' || i;
            
        DBMS_OUTPUT.put_line('Speech name: ' || v_speech_name);
        DBMS_OUTPUT.put_line('Rating name: ' || v_rating_name);
        DBMS_OUTPUT.put_line('Rating value: ' || v_rating_value);
        DBMS_OUTPUT.put_line('-------------------------------------');
    
    END LOOP;
    
    -- видаляємо тестові дані
    DELETE FROM SpeechRating WHERE speech_name = 'speech1';
    DELETE FROM Rating WHERE rating_name LIKE 'rating%';
    DELETE FROM TEDTalk WHERE speech_name = 'speech1';
    DELETE FROM TEDEvent WHERE event = 'TED0000';
    DBMS_OUTPUT.put_line('Inserted data was deleted.');
    
END;

