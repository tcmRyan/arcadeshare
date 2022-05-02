import os
import psycopg2
from psycopg2.errors import UndefinedTable
from config import TENANT_DB_BASE_URL


def create_binds():
    conn = psycopg2.connect(
        database="arcade",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        host=os.environ["DB_HOST"],
        port="5432"
    )

    conn.autocommit = True
    cursor = conn.cursor()
    sql = '''SELECT * FROM tenant'''
    binds = {}
    try:
        results = cursor.execute(sql)
        if results:
            binds = {result.name: TENANT_DB_BASE_URL + result.name for result in results}
    except UndefinedTable:
        pass
    conn.close()
    main = os.environ.get("MAIN_DB")
    binds.update({main: TENANT_DB_BASE_URL + main})
    return binds


def main_db_sql(sql):
    conn = psycopg2.connect(
        database="postgres",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        host=os.environ["DB_HOST"],
        port="5432"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.close()
