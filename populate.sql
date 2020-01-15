INSERT INTO Voice_Pattern (id, login, password, email, lastname, firstname, created)
VALUES(1, 'Jon1','1234qwer','Jonbla1@gmail.com', 'Jon', 'Kon', NOW());
INSERT INTO Voice_Pattern (id, login, password, email, lastname, firstname, created)
VALUES(2, 'Bob345','123qwert','bobwilsom@gmail.com', 'Bob', 'Wilsom', NOW());
INSERT INTO Voice_Pattern (id, login, password, email, lastname, firstname, created)
VALUES(3, 'Nick324','1234qwer','nicktramp@gmail.com', 'Nick', 'Tramp', NOW());

INSERT INTO Text_Data (id, name, description, created, countofprojects, user_id)
VALUES (1, 'Population of reptile','Research population reptile', NOW(), 1, 3);
INSERT INTO Text_Data (id, name, description, created, countofprojects, user_id)
VALUES (2, 'Parsing fecebook','Methods for parsing page of fecebook', NOW(), 3, 1);
INSERT INTO Text_Data (id, name, description, created, countofprojects, user_id)
VALUES (3, 'Data maining','Algoritms for maining', NOW(), 2, 1);

INSERT INTO Command_List (id, name, description, created, CountOfFiles, reposytoty_ID)
VALUES (1, 'Population','Research population reptile in Africa', NOW(), 4, 1);
INSERT INTO Command_List (id, name, description, created, CountOfFiles, reposytoty_ID)
VALUES (2, 'Parsing news line','Method parsing news line of fecebook', NOW(), 3, 2);
INSERT INTO Command_List (id, name, description, created, CountOfFiles, reposytoty_ID)
VALUES (3, 'Parsing single page','Method parsing single page of fecebook', NOW(), 5, 2);

INSERT INTO Command (id, name, File_text, Expansion, versions, created, rating, project_ID)
VALUES (1, 'main','import ...', '.py', '1.0.0.1', NOW(), 0.32, 1);
INSERT INTO Command (id, name, file_text, Expansion, versions, created, rating, project_ID)
VALUES (2, 'poplate','import pandas ...', '.py', '1.0.0.2', NOW(), 0.39, 1);
INSERT INTO Command (id, name, file_text, Expansion, versions, created, rating, project_ID)
VALUES (3, 'main','import xml...', '.py', '1.0.1', NOW(), 0.02, 2);

select * from voice_pattern;
select * from text_data;
select * from command_list;
select * from command;
