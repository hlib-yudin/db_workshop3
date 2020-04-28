CREATE VIEW AllTables AS
    SELECT * 
    FROM 
        TEDTalk
        JOIN SpeechPerson USING (speech_name)
        JOIN SpeechRating USING (speech_name)
        JOIN Video USING (url);
        