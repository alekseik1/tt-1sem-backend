import flask
import psycopg2
from instance.config import DevelopmentConfig as config
import psycopg2.extras
from app import app


def get_connection():
    if not hasattr(flask.g, 'dbconn'):
        flask.g.dbconn = psycopg2.connect(
            database=config.DB_NAME, host=config.DB_HOST,
            user=config.DB_USER, password=config.DB_PASS)
    return flask.g.dbconn


def get_cursor():
    return get_connection().cursor(
        cursor_factory=psycopg2.extras.DictCursor)


def query_one(sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)
        return dict(cur.fetchone())


def insert_one(sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchone()[0]


def query_all(sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)
        return [dict(i) for i in cur.fetchall()]


def _rollback_db(sender, exception, **extra):
    if hasattr(flask.g, 'dbconn'):
        conn = flask.g.dbconn
        conn.rollback()
        conn.close()
        delattr(flask.g, 'dbconn')


def _commit_db(sender, *args, **extra):
    if hasattr(flask.g, 'dbconn'):
        conn = flask.g.dbconn
        conn.commit()
        conn.close()
        delattr(flask.g, 'dbconn')
        return True
    return False


flask.got_request_exception.connect(_rollback_db, app)
flask.request_finished.connect(_commit_db, app)
