DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS ad;

CREATE TABLE accounts (
    ID          INTEGER          PRIMARY KEY AUTOINCREMENT,
    username    TEXT     NOT NULL,
    RATING      DECIMAL
);