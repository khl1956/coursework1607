ALTER TABLE Commands ADD CONSTRAINT FK_Command_List_ID FOREIGN KEY (Command_List_ID)
      REFERENCES Command_List (ID)