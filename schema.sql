
CREATE TABLE IF NOT EXISTS accounts(
    ID          INTEGER    PRIMARY KEY AUTOINCREMENT,
    username    TEXT        NOT NULL,
    password    TEXT        NOT NULL,
    email       TEXT        NOT NULL,
    city        TEXT        NOT NULL,
    STATE       TEXT        NOT NULL,
    RATING      DECIMAL
);  