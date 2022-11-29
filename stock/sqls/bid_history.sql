CREATE TABLE bid_history (
    id int primary key auto_increment,
    code char(16),
    name varchar(64),
    now float,
    open float,
    close float,
    openHigh int,
    type varchar(64),
    industry varchar(64),
    concepts varchar(1024),
    bid1Money float,
    bid2Money float,
    bid3Money float,
    bid4Money float,
    bid5Money float,
    bidTime TIMESTAMP,
    index bid_history_code_index(code)
);

CREATE TABLE bid_sentiment_history (
     id int primary key auto_increment,
     industry varchar(64),
     count smallint,
     bidTime TIMESTAMP
);

