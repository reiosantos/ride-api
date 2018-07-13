DROP SCHEMA IF EXISTS tests CASCADE ;

CREATE SCHEMA tests;

CREATE TABLE tests.users (
    id SERIAL NOT NULL PRIMARY KEY,
    user_id character varying(45) UNIQUE ,
    full_names character varying(255),
    username character varying(255),
    contact character varying(255),
    registration_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    user_type character varying(45),
    password character varying(255),
    last_login timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tests.rides (
    id SERIAL NOT NULL PRIMARY KEY,
    ride_id character varying(45) UNIQUE ,
    post_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    destination character varying(255),
    departure_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    trip_from character varying(255),
    trip_cost double precision,
    status character varying(255),
    driver_id character varying(45) REFERENCES tests.users(user_id)
);

CREATE TABLE tests.requests (
    id SERIAL NOT NULL PRIMARY KEY,
    request_id character varying(45) UNIQUE ,
    ride_id_fk character varying(255) REFERENCES tests.rides(ride_id),
    request_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    passenger_id character varying(45) REFERENCES tests.users(user_id),
    taken boolean,
    status character varying(45)
);
