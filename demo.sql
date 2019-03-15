DROP TABLE users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO users (name) VALUES ('Alice');
INSERT INTO users (name) VALUES ('Bob');
INSERT INTO users (name) VALUES ('Eve');
INSERT INTO users (name) VALUES ('Frank');
INSERT INTO users (name) VALUES ('George');