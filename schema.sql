


CREATE TABLE IF NOT EXISTS accounts(
    email       TEXT        PRIMARY KEY,
    username    TEXT        NOT NULL,
    password    TEXT        NOT NULL,
    city        TEXT        NOT NULL,
    state       TEXT        NOT NULL,
    rating      DECIMAL     NOT NULL,
    adsPosted   INTEGER     NOT NULL,
    bidsPosted  INTEGER     NOT NULL,
    about       TEXT        NOT NULL,
    phoneNo     TEXT        NOT NULL
);  

/* Add in extra criteria that we want to incude in the ad element 
* Status for ads will be one of the following:
* - ACTIVE when date has not been reached and a winning bid has not been chosen (DEFAULT WHEN CREATED)
* - PROGRESS when date has not been reached and a winnign bid has been chosen
* - COMPLETED when date has been reached and a winning bid has been chosen
* - EXPIRED when date has been reached and no winning bid chosen
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
    winningID   INTEGER     NOT NULL,
    CONSTRAINT fk
        FOREIGN KEY (userEmail)
        REFERENCES accounts(email)
);

/* Add in the ad email into the bid field
* - Status for bids will be one of the following:
* - PENDING when the ad does not yet have a winning bid and is still ACTIVE
* - ACCEPTED if the ad is the winning bid for the ad
* - DECLINED if the ad is CLOSED or PROGRESS or COMPLETED and the bid is not the winning bid of the ad
* - COMPLETED when date has arrived and bid is the winning bid
# - AD DELETED if original ad has been deleted
*/
CREATE TABLE IF NOT EXISTS bids(
    ID          INTEGER     PRIMARY KEY AUTOINCREMENT,
    adID        INTEGER     NOT NULL,
    adName      TEXT        NOT NULL,
    userEmail   INTEGER     NOT NULL,
    price       DECIMAL     NOT NULL,
    comment     TEXT        NOT NULL,
    status      TEXT        NOT NULL,
    date        TEXT        NOT NULL,
    oPrice      INTEGER     NOT NULL,
    CONSTRAINT fk
        FOREIGN KEY (adID, userEmail)
        REFERENCES ads(ID, userEmail)
);