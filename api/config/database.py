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
    schema = None

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
    def connect(cls, schema=DatabaseConfig.SCHEMA_PRODUCTION):
        """
        provides a database connection object
        creates the object
        :param schema:
        :return:
        """
        if not cls.__conn:
            cls.__conn = cls.DbConnection(schema).conn
        cls.schema = schema
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
