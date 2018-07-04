--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3
-- Dumped by pg_dump version 10.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = ON;
SELECT pg_catalog.set_config('search_path', '', FALSE);
SET check_function_bodies = FALSE;
SET client_min_messages = WARNING;
SET row_security = OFF;

--
-- Name: production; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA production;


ALTER SCHEMA production
OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = FALSE;

--
-- Name: requests; Type: TABLE; Schema: production; Owner: postgres
--

CREATE TABLE production.requests (
  id           INTEGER NOT NULL,
  request_id   CHARACTER VARYING(45),
  request_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  ride_id_fk   CHARACTER VARYING(45),
  passenger_id CHARACTER VARYING(45),
  taken        BOOLEAN,
  status       CHARACTER VARYING(45)
);


ALTER TABLE production.requests
  OWNER TO postgres;

--
-- Name: requests_id_seq; Type: SEQUENCE; Schema: production; Owner: postgres
--

CREATE SEQUENCE production.requests_id_seq
  AS INTEGER
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;


ALTER TABLE production.requests_id_seq
  OWNER TO postgres;

--
-- Name: requests_id_seq; Type: SEQUENCE OWNED BY; Schema: production; Owner: postgres
--

ALTER SEQUENCE production.requests_id_seq
OWNED BY production.requests.id;

--
-- Name: rides; Type: TABLE; Schema: production; Owner: postgres
--

CREATE TABLE production.rides (
  id             INTEGER NOT NULL,
  ride_id        CHARACTER VARYING(45),
  post_date      TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  destination    CHARACTER VARYING(255),
  departure_time TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  trip_from      CHARACTER VARYING(255),
  trip_cost      DOUBLE PRECISION,
  status         CHARACTER VARYING(255),
  driver_id      CHARACTER VARYING(45)
);


ALTER TABLE production.rides
  OWNER TO postgres;

--
-- Name: rides_id_seq; Type: SEQUENCE; Schema: production; Owner: postgres
--

CREATE SEQUENCE production.rides_id_seq
  AS INTEGER
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;


ALTER TABLE production.rides_id_seq
  OWNER TO postgres;

--
-- Name: rides_id_seq; Type: SEQUENCE OWNED BY; Schema: production; Owner: postgres
--

ALTER SEQUENCE production.rides_id_seq
OWNED BY production.rides.id;

--
-- Name: users; Type: TABLE; Schema: production; Owner: postgres
--

CREATE TABLE production.users (
  id                INTEGER NOT NULL,
  username          CHARACTER VARYING(255),
  full_names        CHARACTER VARYING(255),
  contact           CHARACTER VARYING(45),
  registration_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  user_type         CHARACTER VARYING(45),
  password          CHARACTER VARYING(255),
  user_id           CHARACTER VARYING(45)
);


ALTER TABLE production.users
  OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: production; Owner: postgres
--

CREATE SEQUENCE production.users_user_id_seq
  AS INTEGER
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;


ALTER TABLE production.users_user_id_seq
  OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: production; Owner: postgres
--

ALTER SEQUENCE production.users_user_id_seq
OWNED BY production.users.id;

--
-- Name: requests id; Type: DEFAULT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production.requests
  ALTER COLUMN id SET DEFAULT nextval('production.requests_id_seq' :: REGCLASS);

--
-- Name: rides id; Type: DEFAULT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production.rides
  ALTER COLUMN id SET DEFAULT nextval('production.rides_id_seq' :: REGCLASS);

--
-- Name: users id; Type: DEFAULT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production.users
  ALTER COLUMN id SET DEFAULT nextval('production.users_user_id_seq' :: REGCLASS);

--
-- Name: requests_request_id_uindex; Type: INDEX; Schema: production; Owner: postgres
--

CREATE UNIQUE INDEX requests_request_id_uindex
  ON production.requests USING BTREE (request_id);

--
-- Name: rides_ride_id_uindex; Type: INDEX; Schema: production; Owner: postgres
--

CREATE UNIQUE INDEX rides_ride_id_uindex
  ON production.rides USING BTREE (ride_id);

--
-- Name: users_user_id_uindex; Type: INDEX; Schema: production; Owner: postgres
--

CREATE UNIQUE INDEX users_user_id_uindex
  ON production.users USING BTREE (user_id);

--
-- Name: requests requests_passenger_id_fkey; Type: FK CONSTRAINT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production.requests
  ADD CONSTRAINT requests_passenger_id_fkey FOREIGN KEY (passenger_id) REFERENCES production.users (user_id) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: requests requests_ride_id_fk_fkey; Type: FK CONSTRAINT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production.requests
  ADD CONSTRAINT requests_ride_id_fk_fkey FOREIGN KEY (ride_id_fk) REFERENCES production.rides (ride_id) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- Name: rides rides_driver_id_fkey; Type: FK CONSTRAINT; Schema: production; Owner: postgres
--

ALTER TABLE ONLY production.rides
  ADD CONSTRAINT rides_driver_id_fkey FOREIGN KEY (driver_id) REFERENCES production.users (user_id) ON UPDATE CASCADE ON DELETE CASCADE;

--
-- PostgreSQL database dump complete
--

