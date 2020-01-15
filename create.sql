CREATE TABLE "Voice_Pattern"(

	user_id INTEGER PRIMARY KEY,

	voice_body TEXT UNIQUE NOT NULL,

	voice_pronunciation_date TIMESTAMP,
	voice_emotion_logic_accent TEXT
);

CREATE TABLE "Command_List"(

	command_group_id INTEGER PRIMARY KEY,
	command_body_text TEXT NOT NULL,
	сommand_group_data TEXT,
);

CREATE TABLE "Text_Data"(

	belongs_to_id INTEGER PRIMARY KEY,
	text_body TEXT,
	text_pronunciation_time TIMESTAMP,
	text_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS "Command"(

	belongs_to_id INTEGER,
	command_body TEXT,
	CONSTRAINT belongs_to_id_fkey FOREIGN KEY (belongs_to_id)
		REFERENCES Voice_Pattern (user_id) MATCH SIMPLE
		ON UPDATE NO ACTION ON DELETE NO ACTION,
);

--ALTER TABLE Users ADD CONSTRAINT Chack_correct_email CHECK (Email like '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$');