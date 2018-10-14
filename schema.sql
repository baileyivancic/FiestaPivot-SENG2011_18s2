


CREATE TABLE IF NOT EXISTS accounts(
    email       TEXT        PRIMARY KEY,
    username    TEXT        NOT NULL,
    password    TEXT        NOT NULL,
    city        TEXT        NOT NULL,
    state       TEXT        NOT NULL,
    rating      DECIMAL,
    adsPosted   INTEGER,
    bidsPosted  INTEGER,
    about       TEXT
);  

/* Add in extra criteria that we want to incude in the ad element 
* Status for ads will be one of the following:
* - ACTIVE when date has not been reached and a winning bid has not been chosen (DEFAULT WHEN CREATEDz)
* - PROGRESS when date has not been reached and a winnign bid has been chosen
* - COMPLETED when date has been reached and a winning bid has been chosen
* - CLOSED when date has been reached and no winning bid OR user closes before date
*/
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
    alcohol     TEXT        NOT NULL,
    noPeople    INTEGER     NOT NULL,
    CONSTRAINT fk
        FOREIGN KEY (userEmail)
        REFERENCES accounts(email)
);

/* Add in the ad email into the bid field
* - Status for bids will be one of the following:
* - PENDING when the ad does not yet have a winning bid and is still ACTIVE
* - ACCEPTED if the ad is the winning bid for the ad
* - DECLINED if the ad is CLOSED or PROGRESS or COMPLETED and the bid is not the winning bid of the ad
*/
CREATE TABLE IF NOT EXISTS bids(
    ID          INTEGER     PRIMARY KEY AUTOINCREMENT,
    adID        INTEGER     NOT NULL,
    adName      TEXT        NOT NULL,
    userEmail   INTEGER     NOT NULL,
    price       DECIMAL     NOT NULL,
    comment     TEXT,
    status      TEXT,
    CONSTRAINT fk
        FOREIGN KEY (adID, userEmail)
        REFERENCES ads(ID, userEmail)
);