--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3
-- Dumped by pg_dump version 10.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tests; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tests;


ALTER SCHEMA tests OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: requests; Type: TABLE; Schema: tests; Owner: postgres
--

CREATE TABLE tests.requests (
    id integer NOT NULL,
    request_id character varying(45),
    ride_id_fk character varying(255),
    request_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    passenger_id character varying(45),
    taken boolean,
    status character varying(45)
);


ALTER TABLE tests.requests OWNER TO postgres;

--
-- Name: requests_id_seq; Type: SEQUENCE; Schema: tests; Owner: postgres
--

CREATE SEQUENCE tests.requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tests.requests_id_seq OWNER TO postgres;

--
-- Name: requests_id_seq; Type: SEQUENCE OWNED BY; Schema: tests; Owner: postgres
--

ALTER SEQUENCE tests.requests_id_seq OWNED BY tests.requests.id;


--
-- Name: rides; Type: TABLE; Schema: tests; Owner: postgres
--

CREATE TABLE tests.rides (
    id integer NOT NULL,
    ride_id character varying(45),
    post_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    destination character varying(255),
    departure_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    trip_from character varying(255),
    trip_cost double precision,
    status character varying(255),
    driver_id character varying(45)
);


ALTER TABLE tests.rides OWNER TO postgres;

--
-- Name: table_name_id_seq; Type: SEQUENCE; Schema: tests; Owner: postgres
--

CREATE SEQUENCE tests.table_name_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tests.table_name_id_seq OWNER TO postgres;

--
-- Name: table_name_id_seq; Type: SEQUENCE OWNED BY; Schema: tests; Owner: postgres
--

ALTER SEQUENCE tests.table_name_id_seq OWNED BY tests.rides.id;


--
-- Name: users; Type: TABLE; Schema: tests; Owner: postgres
--

CREATE TABLE tests.users (
    id integer NOT NULL,
    user_id character varying(45),
    full_names character varying(255),
    username character varying(255),
    contact character varying(255),
    registration_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    user_type character varying(45),
    password character varying(255)
);


ALTER TABLE tests.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: tests; Owner: postgres
--

CREATE SEQUENCE tests.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tests.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: tests; Owner: postgres
--

ALTER SEQUENCE tests.users_id_seq OWNED BY tests.users.id;


--
-- Name: requests id; Type: DEFAULT; Schema: tests; Owner: postgres
--

ALTER TABLE ONLY tests.requests ALTER COLUMN id SET DEFAULT nextval('tests.requests_id_seq'::regclass);


--
-- Name: rides id; Type: DEFAULT; Schema: tests; Owner: postgres
--

ALTER TABLE ONLY tests.rides ALTER COLUMN id SET DEFAULT nextval('tests.table_name_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: tests; Owner: postgres
--

ALTER TABLE ONLY tests.users ALTER COLUMN id SET DEFAULT nextval('tests.users_id_seq'::regclass);


--
-- Name: requests requests_pkey; Type: CONSTRAINT; Schema: tests; Owner: postgres
--

ALTER TABLE ONLY tests.requests
    ADD CONSTRAINT requests_pkey PRIMARY KEY (id);


--
-- Name: rides table_name_pkey; Type: CONSTRAINT; Schema: tests; Owner: postgres
--

ALTER TABLE ONLY tests.rides
    ADD CONSTRAINT table_name_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: tests; Owner: postgres
--

ALTER TABLE ONLY tests.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: requests_id_uindex; Type: INDEX; Schema: tests; Owner: postgres
--

CREATE UNIQUE INDEX requests_id_uindex ON tests.requests USING btree (id);


--
-- Name: requests_request_id_uindex; Type: INDEX; Schema: tests; Owner: postgres
--

CREATE UNIQUE INDEX requests_request_id_uindex ON tests.requests USING btree (request_id);


--
-- Name: table_name_id_uindex; Type: INDEX; Schema: tests; Owner: postgres
--

CREATE UNIQUE INDEX table_name_id_uindex ON tests.rides USING btree (id);


--
-- Name: table_name_ride_id_uindex; Type: INDEX; Schema: tests; Owner: postgres
--

CREATE UNIQUE INDEX table_name_ride_id_uindex ON tests.rides USING btree (ride_id);


--
-- Name: users_id_uindex; Type: INDEX; Schema: tests; Owner: postgres
--

CREATE UNIQUE INDEX users_id_uindex ON tests.users USING btree (id);


--
-- Name: users_user_id_uindex; Type: INDEX; Schema: tests; Owner: postgres
--

CREATE UNIQUE INDEX users_user_id_uindex ON tests.users USING btree (user_id);


--
-- Name: requests requests_rides_ride_id_fk; Type: FK CONSTRAINT; Schema: tests; Owner: postgres
--

ALTER TABLE ONLY tests.requests
    ADD CONSTRAINT requests_rides_ride_id_fk FOREIGN KEY (ride_id_fk) REFERENCES production.rides(ride_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: requests requests_users_user_id_fk; Type: FK CONSTRAINT; Schema: tests; Owner: postgres
--

ALTER TABLE ONLY tests.requests
    ADD CONSTRAINT requests_users_user_id_fk FOREIGN KEY (passenger_id) REFERENCES production.users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: rides rides_users_user_id_fk; Type: FK CONSTRAINT; Schema: tests; Owner: postgres
--

ALTER TABLE ONLY tests.rides
    ADD CONSTRAINT rides_users_user_id_fk FOREIGN KEY (driver_id) REFERENCES production.users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

