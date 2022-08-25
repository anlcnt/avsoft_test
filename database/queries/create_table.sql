-- Запрос создания таблицы в базе

CREATE TABLE `words` (`word` VARCHAR(256) NOT NULL , `count` INT NOT NULL , UNIQUE (`word`)) COMMENT = 'Соотношение слов и количества вхождений';