CREATE USER postgres;


CREATE TABLE
IF NOT EXISTS public.statistics (
    customerId INTEGER NOT NULL,
    type VARCHAR NOT NULL,
    amount NUMERIC(10, 3) NOT NULL,
    uuid UUID PRIMARY KEY,
    date DATE NOT NULL
);
