CREATE TABLE daily_limit_level1_stock (
    id int primary key auto_increment,
    code char(16),
    name varchar(64),
    now float,
    open float,
    close float,
    growthRate float,
    buyPrice float,
    buyDate TIMESTAMP,
    safePrice float,
    lowestPrice float,
    highestPrice float,
    growthRate float,
    buyReason varchar(256),
    sellPrice float,
    sellDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sellReason varchar(256),
    visible smallint,
    type varchar(64),
    industry varchar(64),
    concepts varchar(1024),
    index my_stocks_code_index(code)
);

CREATE TABLE daily_limit_level2_stock (
    id int primary key auto_increment,
    code char(16),
    name varchar(64),
    now float,
    open float,
    close float,
    growthRate float,
    buyPrice float,
    buyDate TIMESTAMP,
    safePrice float,
    lowestPrice float,
    highestPrice float,
    growRate float,
    buyReason varchar(256),
    sellPrice float,
    sellDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sellReason varchar(256),
    visible smallint,
    type varchar(64),
    industry varchar(64),
    concepts varchar(1024),
    index my_stocks_code_index(code)
);
