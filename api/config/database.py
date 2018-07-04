"""
database connection module
"""
import psycopg2 as pg
from psycopg2.extras import RealDictCursor

from api.config.config import DatabaseConfig


class DatabaseConnection:
    """
    Database connection class
    Handles all database related issues/processes
    """
    __conn = None
    schema = DatabaseConfig.SCHEMA_PRODUCTION

    class DbConnection(object):
        """
        class creates the connection object abd sets
        auto commit to False
        """

        def __init__(self, schema):
            self.schema = schema
            self.conn = pg.connect(database=DatabaseConfig.DATABASE,
                                   user=DatabaseConfig.USER,
                                   password=DatabaseConfig.PASSWORD,
                                   host=DatabaseConfig.HOST,
                                   port=DatabaseConfig.PORT,
                                   cursor_factory=RealDictCursor,
                                   options=f'-c search_path={self.schema}', )

            self.conn.autocommit = False

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.conn.close()

    @classmethod
    def init_db(cls, app):
        """
        provides a database connection object
        creates the object
        :return:
        """
        if app.config['TESTING']:
            cls.schema = DatabaseConfig.SCHEMA_TESTING

        if not cls.__conn:
            cls.__conn = cls.DbConnection(cls.schema).conn

    @classmethod
    def connect(cls):
        return cls

    @classmethod
    def insert(cls, table, data):
        """
        handle all insertions into the database
        :param table:
        :param data:
        :return:
        """
        if not table or not data or not isinstance(data, dict):
            return False
        columns = tuple(data.keys())
        values = tuple(data.values())

        _top = f"""INSERT INTO {cls.schema}.{table} ("""

        cols = ", ".join([f""" "{n}" """ for n in columns])

        middle = """) VALUES ("""

        val = ", ".join([f""" '{v}' """ for v in values])

        bottom = """)"""

        sql = _top + cols + middle + val + bottom

        cur = cls.__conn.cursor()
        cur.execute(sql)
        cls.__conn.commit()
        if cur:
            return cur
        return None

    @classmethod
    def find(cls, name_of_table, criteria=None, join=None):
        """
        handles all queries to retrieve data
        :param name_of_table:
        :param criteria:
        :param join:
        :return:
        """
        sql = ""
        if not criteria and not join:
            sql = f"""SELECT * FROM {cls.schema}.{name_of_table}"""
        else:
            if criteria and not join:
                columns = tuple(criteria.keys())
                values = tuple(criteria.values())
                top1 = f"""SELECT * FROM {cls.schema}.{name_of_table} WHERE ("""

                if len(columns) == 1:
                    crit = f""" "{columns[0]}"='{values[0]}' )"""
                else:
                    crit = " AND ".join([f""" "{k}" = '{v}' """ for k, v in
                                         criteria.items()]) + """)"""

                sql = top1 + crit
            else:
                pass
        cur = cls.__conn.cursor()
        cur.execute(sql)
        cls.__conn.commit()
        if cur:
            val = cur.fetchall()
            if len(val) == 1:
                return val[0]
            elif len(val) > 1:
                return val
        return None

    @classmethod
    def update(cls, table_name, selection, update):
        """
        Handles update queries
        :param table_name:
        :param selection:
        :param update:
        :return:
        """

        _top = f"""UPDATE {cls.schema}.{table_name} SET """

        vals = ", ".join([f""" "{col1}"='{val1}' """ for col1, val1 in update.items()])

        middle = """ WHERE """

        cols = " AND ".join([f""" "{col}"='{val}' """ for col, val in selection.items()])

        sql = _top + vals + middle + cols

        cur = cls.__conn.cursor()
        cur.execute(sql)
        cls.__conn.commit()
        if cur:
            return cur
        return None

    @classmethod
    def delete(cls, table_name, selection):
        """
        handles delete queries
        :param table_name:
        :param selection:
        :return:
        """
        _top = f"""DELETE FROM {cls.schema}.{table_name} WHERE """

        cols = " AND ".join([f""" "{col}"='{val}' """ for col, val in selection.items()])

        sql = _top + cols

        cur = cls.__conn.cursor()
        cur.execute(sql)
        cls.__conn.commit()
        if cur:
            return cur
        return None

    @classmethod
    def find_detailed_requests(cls, name_of_table, criteria=None):
        """
        specific query handler for requests
        :param name_of_table:
        :param criteria:
        :return:
        """
        if not criteria:
            query = f"""SELECT * FROM {cls.schema}.{name_of_table}"""
        else:
            query = f"""
            SELECT a.request_date, a.request_id, a.status, a.taken, 
            b.status as ride_status, b.driver_id, b.ride_id, b.departure_time, 
            b.destination, b.post_date, b.trip_cost, b.trip_from, c.user_id, c.contact, 
            c.full_names FROM production.requests a LEFT JOIN production.rides b ON 
            a.ride_id_fk = b.ride_id LEFT JOIN production.users c ON 
            a.passenger_id = c.user_id WHERE (b.driver_id='{criteria['driver_id']}' AND 
            a.ride_id_fk='{criteria['ride_id']}')
            """

        cur = cls.__conn.cursor()
        cur.execute(query)
        cls.__conn.commit()
        if cur:
            val = cur.fetchall()
            if len(val) == 1:
                return val[0]
            elif len(val) > 1:
                return val
        return None

    @classmethod
    def create_test_schema(cls):
        """
        create test schema
        :return:
        """
        cur = cls.__conn.cursor()
        # cur.execute(open("../../database_tests.sql", "r").read())
        cur.execute(
            """
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
            """
        )
        cls.__conn.commit()

    @classmethod
    def drop_test_schema(cls):
        """
        delete test schema after using it
        :return:
        """
        cur = cls.__conn.cursor()
        cur.execute("""DROP SCHEMA IF EXISTS tests CASCADE""")
        cls.__conn.commit()
