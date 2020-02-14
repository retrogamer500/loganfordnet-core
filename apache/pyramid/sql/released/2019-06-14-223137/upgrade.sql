CREATE TABLE page (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    title VARCHAR(100) CHARACTER SET utf8mb4 NOT NULL, 
    url VARCHAR(256) CHARACTER SET utf8mb4 NOT NULL, 
    display_in_sidebar INTEGER NOT NULL, 
    created_by_id INTEGER NOT NULL, 
    created_date TIMESTAMP NULL, 
    CONSTRAINT pk_page PRIMARY KEY (id), 
    CONSTRAINT fk_page_created_by_id_user FOREIGN KEY(created_by_id) REFERENCES user (id), 
    CONSTRAINT uq_page_url UNIQUE (url)
);

CREATE INDEX ix_page_id ON page (id);

CREATE TABLE page_history (
    id INTEGER NOT NULL AUTO_INCREMENT, 
    content TEXT, 
    version INTEGER NOT NULL, 
    last_modified_by_id INTEGER NOT NULL, 
    last_modified_date TIMESTAMP NULL, 
    page_id INTEGER NOT NULL, 
    CONSTRAINT pk_page_history PRIMARY KEY (id), 
    CONSTRAINT fk_page_history_last_modified_by_id_user FOREIGN KEY(last_modified_by_id) REFERENCES user (id), 
    CONSTRAINT fk_page_history_page_id_page FOREIGN KEY(page_id) REFERENCES page (id)
);

CREATE INDEX ix_page_history_id ON page_history (id);

