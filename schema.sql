

CREATE TABLE IF NOT EXISTS accounts(
    email       TEXT        PRIMARY KEY,
    username    TEXT        NOT NULL,
    password    TEXT        NOT NULL,
    city        TEXT        NOT NULL,
    state       TEXT        NOT NULL,
    rating      DECIMAL,
    adsPosted   INTEGER,
    bidsPosted  INTEGER,
);  

/* Add in extra criteria that we want to incude in the ad element 
* State for ad will be either:
* - ACTIVE if thr ad is open and receiving bids
* - PROGRESS when a bid has been selected but the event has not happened
* - COMPLETED when date of ad is passed and ad had a winning bid
* - CLOSED when date of ad is passed and ad did not have a winning bid
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
    alcohol     INTEGER     NOT NULL,
    noPeople    INTEGER     NOT NULL,
    setting     TEXT        NOT NULL,
    bidID       INTEGER     FOREIGN KEY,  
    CONSTRAINT fk
        FOREIGN KEY (userEmail)
        REFERENCES accounts(email)
);

/* Add in the ad email into the bid field*/
/* 
* Status for bids will be either:
* - PENDING when ad does not have a winning bid
* - ACCEPTED when ad becomes the winning bid of ad
* - DECLINED when ad has different winning bid
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