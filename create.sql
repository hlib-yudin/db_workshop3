--сутність Person
--ключем є ім'я людини, бо за даними датасету неможливо розрізнити, чи це дві людини з однаковим іменем,
--чи це одна й та сама людина повторюється двічі. Вважатимемо, що імена унікальні.
CREATE TABLE Person (
    person_name VARCHAR(50) NOT NULL PRIMARY KEY
);


--сутність TEDEvent
CREATE TABLE TEDEvent (
    event VARCHAR(70) NOT NULL PRIMARY KEY
    );
    

--сутність Rating
CREATE TABLE Rating (
    rating_name VARCHAR(20) NOT NULL PRIMARY KEY
    );
       

--сутність TEDTalk -- сам виступ
--назва виступу складається з імені людини та назви доповіді; одна й та сама людина не буде двічі розповідати одну й 
--ту саму доповідь. Отже, назву виступу можна вважати ключем.
CREATE TABLE TEDTalk(
    speech_name VARCHAR(120) NOT NULL PRIMARY KEY,
    description VARCHAR(1000) NOT NULL,
    duration_sec INT NOT NULL CHECK (duration_sec > 0),
    event VARCHAR(70) NOT NULL REFERENCES TEDEvent(event),
    film_date TIMESTAMP NOT NULL,
    url VARCHAR(255) NOT NULL UNIQUE
    );
   
    
--сутність SpeechPerson -- людина та TEDTalk, який вона розповідає
CREATE TABLE SpeechPerson (
    person_name VARCHAR(50) NOT NULL REFERENCES Person(person_name),
    speech_name VARCHAR(120) NOT NULL REFERENCES TEDTalk(speech_name),
    CONSTRAINT PK_speechperson PRIMARY KEY (person_name, speech_name)
    );
    

--сутність SpeechRating -- виступ та його різні рейтинги
CREATE TABLE SpeechRating (
    speech_name VARCHAR(120) NOT NULL REFERENCES TEDTalk(speech_name),
    rating_name VARCHAR(20) NOT NULL REFERENCES Rating(rating_name),
    rating_value INT DEFAULT 0 CHECK(rating_value >= 0),
    CONSTRAINT PK_speechrating PRIMARY KEY (speech_name, rating_name)
    );


--сутність Video -- відео лекції, опубліковане на офційному сайті ted.com
CREATE TABLE Video (
    url VARCHAR(255) NOT NULL REFERENCES TEDTalk(url),
    curr_date DATE DEFAULT TO_DATE('09-21-2017', 'MM-DD-YYYY') NOT NULL,
    views INT DEFAULT 0 CHECK (views >= 0),
    CONSTRAINT PK_video PRIMARY KEY (url, curr_date)
    );