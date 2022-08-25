-- Удаляет запись, если количество вхождений больше 1

DELETE FROM `words` WHERE `count` > %d;