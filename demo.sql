DROP TABLE user_roles;
DROP TABLE users;
DROP TABLE roles;

CREATE TABLE roles (
    role_id TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    name TEXT
);

CREATE TABLE user_roles (
    user_role_id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    role_id TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(user_id)
    FOREIGN KEY(role_id) REFERENCES role(role_id)
);

INSERT INTO roles (role_id, description) VALUES ('admin', 'Administrator Role');
INSERT INTO roles (role_id, description) VALUES ('user', 'Users');

INSERT INTO users (user_id, name) VALUES ('alice', 'Alice');
INSERT INTO users (user_id, name) VALUES ('bob', 'Bob');
INSERT INTO users (user_id, name) VALUES ('eve', 'Eve');
INSERT INTO users (user_id, name) VALUES ('frank', 'Frank');
INSERT INTO users (user_id, name) VALUES ('george', 'George');
INSERT INTO users (user_id, name) VALUES ('admin', 'The Administrator');

INSERT INTO user_roles(user_id, role_id) VALUES ('admin', 'admin');
INSERT INTO user_roles(user_id, role_id) VALUES ('admin', 'users');
INSERT INTO user_roles(user_id, role_id) VALUES ('alice', 'users');
INSERT INTO user_roles(user_id, role_id) VALUES ('bob', 'users');
INSERT INTO user_roles(user_id, role_id) VALUES ('eve', 'users');
INSERT INTO user_roles(user_id, role_id) VALUES ('george', 'users');