CREATE TABLE stock (
    id int primary key,
    code char(16),
    name varchar(64),
    buy_price bigint,
    now_price bigint
);