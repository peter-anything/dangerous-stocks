CREATE TABLE stock_review (
    id int primary key auto_increment,
    code char(16),
    name varchar(64),
    now float,
    open float,
    close float,
    high float,
    low float,
    growthRate float,
    createdAt timestamp,
    upLimit float,
    downLimit float,
    marketValue float,
    tradingMarketValue float,
    pe float,
    turnoverRate float,
    type varchar(64),
    industry varchar(64),
    concepts varchar(1024),
    bid1Money float,
    upLimitType int,
    everUpLimited int,
    breakUpLimitCount int,
    continuousUpLimitCount int,
    upDownStatistics varchar(64),
    firstUpLimitTime varchar(64),
    finalUpLimitTime varchar(64),
    index stock_review_code_index(code)
);

ALTER TABLE stock_review ADD volumne float;

ALTER TABLE stock_review ADD smallUp float default 0;
ALTER TABLE stock_review ADD smallVolumeUp float default 0;
ALTER TABLE stock_review ADD volumeBreakUpMa5 float default 0;
ALTER TABLE stock_review ADD last2Up float default 0;
ALTER TABLE stock_review ADD last3Up float default 0;
ALTER TABLE stock_review ADD last5Up float default 0;