CREATE TABLE manual_recommend_stock (
    id int primary key auto_increment,
    code char(16),
    name varchar(64),
    cancel smallint default 0,
    index manual_recommend_stock_index(code)
);


CREATE TABLE manual_recommend_stock_price_history (
    id int primary key auto_increment,
    code char(16),
    name varchar(64),
    now float,
    open float,
    close float,
    high float,
    low float,
    marketValue float,
    tradingMarketValue float,
    pe float,
    turnoverRate float,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    openHigh int,
    openHighRate float,
    closeRate float,
    needAlert smallint,
    riseUpRate float,
    downRate float,
    nowRate float,
    afterHalfHourRiseUpRate float,
    afterHalfHourDownRate float,
    afterHalfHourNowRate float,
    bid1Money float,
    index manual_recommend_stock_price_history_code_index(code)
);