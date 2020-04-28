CREATE OR REPLACE VIEW AllTables AS
    SELECT 
        speech_name
        , event
        , film_date
        , duration_sec
        , url
        
        , views
        
        , rating_name
        , rating_value
        
        , person_name
    
    FROM 
        TEDTalk
        JOIN SpeechPerson USING (speech_name)
        JOIN SpeechRating USING (speech_name)
        JOIN Video USING (url);
        
