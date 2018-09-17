
CREATE TABLE IF NOT EXISTS accounts(
    ID          INTEGER     PRIMARY KEY AUTOINCREMENT,
    username    TEXT        NOT NULL,
    password    TEXT        NOT NULL,
    email       TEXT        NOT NULL,
    city        TEXT        NOT NULL,
    STATE       TEXT        NOT NULL,
    RATING      DECIMAL
);  

/* Add in extra criteria that we want to incude in the ad element */
CREATE TABLE IF NOT EXISTS ads(
    ID          INTEGER     PRIMARY KEY AUTOINCREMENT,
    userID      INTEGER     FOREIGN KEY,
    title       TEXT        NOT NULL,
    price       DECIMAL     NOT NULL,
    area        TEXT        NOT NULL,
    descr       TEXT        NOT NULL,
    active      BOOLEAN     NOT NULL
);

/* Add in extra criteria we want to include*/
CREATE TABLE IF NOT EXISTS bids(
    ID          INTEGER     PRIMARY KEY AUTOINCREMENT,
    adID        INTEGER     FOREIGN KEY,
    userID      INTEGER     FOREIGN KEY,
    price       DECIMAL     NOT NULL,
    comment     TEXT
);