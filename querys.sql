CREATE DATABASE parking;

CREATE TABLE parking.space (
    floor INT NOT NULL,
    spot CHAR NOT NULL,
    used BOOL DEFAULT TRUE,
    PRIMARY KEY (floor, space)
);