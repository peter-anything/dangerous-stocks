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


CREATE TABLE recommend_stock_in_real_time (
      id int primary key auto_increment,
      code char(16),
      name varchar(64),
      industry varchar(64),
      marketValue float,
      turnover float,
      turnoverRate float,
      createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      openHighRate float,
      bottomUpRate float,
      nowRate float,
      canBuy smallint default 0,
      recent5ProfitLossRatio text,
      recent10ProfitLossRatio text,
      recent20ProfitLossRatio text,
      index recommend_stock_in_real_time_code_index(code)
);