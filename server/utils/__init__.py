import os
from contextlib import contextmanager
from typing import Any

import psycopg2
import sqlalchemy.orm
from flask import g, current_app
from flask_sqlalchemy import SQLAlchemy, SignallingSession
from psycopg2.errors import UndefinedTable
from config import TENANT_DB_BASE_URL


def create_binds():
    main = os.environ.get("MAIN_DB")

    conn = psycopg2.connect(
        database=main,
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
        cursor.execute(sql)
        results = cursor.fetchall()

        if results:
            binds = {result[1]: TENANT_DB_BASE_URL + result[1] for result in results}
    except UndefinedTable:
        current_app.logger.error("Tenant not defined")
    conn.close()

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


class MTSignallingSession(SignallingSession):

    def __init__(self, db, *args, **kwargs):
        super().__init__(db, *args, **kwargs)
        self.db = db

    def get_bind(self, mapper=None, clause=None):
        if mapper is not None:
            info = getattr(mapper.persist_selectable, "info", {})
            if info.get("bind_key") == "__tenant__":
                info["bind_key"] = self.db.context_bind_key
                try:
                    return super().get_bind(mapper=mapper, clause=clause)
                finally:
                    info["bind_key"] = "__tenant__"
        return super().get_bind(mapper=mapper, clause=clause)


class MultiTenantSQLA(SQLAlchemy):
    context_bind_key = None

    @contextmanager
    def context(self, bind=None):
        _context_bind_key = self.context_bind_key
        try:
            self.context_bind_key = bind
            yield
        finally:
            self.context_bind_key = _context_bind_key

    def create_session(self, options):
        return sqlalchemy.orm.sessionmaker(class_=MTSignallingSession, db=self, **options)

    def get_binds(self, app=None):
        binds = super().get_binds(app=app)
        app = self.get_app(app)
        engine = self.get_engine(app, None)
        tables = self.get_tables_for_bind("__tenant__")
        binds.update(dict((table, engine) for table in tables))
        return binds

    @staticmethod
    def choose_tenant(user):
        g.tenant = user.tenant.name

    def get_engine(self, app=None, bind=None):
        if bind is None:
            if not hasattr(g, "tenant"):
                bind = current_app.config["MAIN_DB"]
            else:
                bind = g.tenant
        return super().get_engine(app=app, bind=bind)

    def get_tables_for_bind(self, bind: Any | None = ...):
        result = []
        for table in self.Model.metadata.tables.values():
            if table.info.get("bind_key") == bind or (bind is not None and table.info.get("bind_key") == "__tenant__"):
                result.append(table)
        return result
