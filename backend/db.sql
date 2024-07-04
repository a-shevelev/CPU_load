CREATE TABLE cpu_load (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    load FLOAT NOT NULL
);
CREATE TABLE server_status (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    status VARCHAR(100) NOT NULL
);
