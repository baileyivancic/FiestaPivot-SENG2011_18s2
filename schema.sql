


CREATE TABLE IF NOT EXISTS accounts(
    email       TEXT        PRIMARY KEY,
    username    TEXT        NOT NULL,
    password    TEXT        NOT NULL,
    city        TEXT        NOT NULL,
    state       TEXT        NOT NULL,
    rating      DECIMAL
);  

/* Add in extra criteria that we want to incude in the ad element */
CREATE TABLE IF NOT EXISTS ads(
    ID          INTEGER     PRIMARY KEY AUTOINCREMENT,
    userEmail   INTEGER     NOT NULL,
    title       TEXT        NOT NULL,
    price       DECIMAL     NOT NULL,
    city        TEXT        NOT NULL,
    state       TEXT        NOT NULL,
    descr       TEXT        NOT NULL,
    status      TEXT        NOT NULL,
    date        TEXT        NOT NULL,
    start_time  TEXT        NOT NULL,
    end_time    TEXT        NOT NULL,
    CONSTRAINT fk
        FOREIGN KEY (userEmail)
        REFERENCES accounts(email)
);

/* Add in the ad email into the bid field*/
/* Add in extra criteria we want to include*/
CREATE TABLE IF NOT EXISTS bids(
    ID          INTEGER     PRIMARY KEY AUTOINCREMENT,
    adID        INTEGER     NOT NULL,
    adName      TEXT        NOT NULL,
    userEmail   INTEGER     NOT NULL,
    price       DECIMAL     NOT NULL,
    comment     TEXT,
    CONSTRAINT fk
        FOREIGN KEY (adID, userEmail)
        REFERENCES ads(ID, userEmail)
);