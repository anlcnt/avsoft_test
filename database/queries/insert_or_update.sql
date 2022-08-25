-- Запрос для заполнения базы данных

INSERT INTO words(word, count) 
VALUES %s
ON DUPLICATE KEY UPDATE 
    word = VALUES(word),
    count = count + VALUES(count);