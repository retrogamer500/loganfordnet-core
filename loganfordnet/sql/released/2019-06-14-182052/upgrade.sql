-- Running upgrade  -> 8fb7424ef690

CREATE TABLE page (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    title VARCHAR(100) CHARACTER SET utf8mb4 NOT NULL, 
    display_in_sidebar INTEGER NOT NULL, 
    user_id INTEGER NOT NULL, 
    CONSTRAINT pk_page PRIMARY KEY (id), 
    CONSTRAINT fk_page_user_id_user FOREIGN KEY(user_id) REFERENCES user (id)
);

CREATE INDEX ix_page_id ON page (id);

CREATE TABLE page_history (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    content TEXT, 
    version INTEGER NOT NULL, 
    user_id INTEGER NOT NULL, 
    page_id INTEGER NOT NULL, 
    CONSTRAINT pk_page_history PRIMARY KEY (id), 
    CONSTRAINT fk_page_history_page_id_page FOREIGN KEY(page_id) REFERENCES page (id), 
    CONSTRAINT fk_page_history_user_id_user FOREIGN KEY(user_id) REFERENCES user (id)
);

CREATE INDEX ix_page_history_id ON page_history (id);
