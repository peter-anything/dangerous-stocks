CREATE TABLE stock (
    id int primary key auto_increment,
    code char(16),
    name varchar(64),
    market varchar(64),
    category varchar(64),
    type varchar(64),
    index stock_code_index(code),
    index stock_name_index(name)
);

CREATE TABLE stock_industry (
    id int primary key auto_increment,
    code char(16),
    name varchar(64),
    index stock_industry_index(code)
);


CREATE TABLE stock_fundamental (
    id int primary key auto_increment,
    code char(16),
    name varchar(64),
    marketValue float,
    tradingMarketValue float,
    open float,
    high float,
    low float,
    close float,
    pe float,
    turnoverRate float,
    turnoverVolume float,
    tradingMoney float,
    createdAt TIMESTAMP,
    growthRate float,
    index stock_fundamental_code_index(code)
);


CREATE TABLE my_stock (
    id int primary key,
    code char(16),
    name varchar(64),
    buyPrice float,
    buyDate TIMESTAMP,
    safePrice float,
    buyReason varchar(256),
    sellPrice float,
    sellDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sellReason varchar(256),
    visible smallint,
    index my_stocks_code_index(code)
);
