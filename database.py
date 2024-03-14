from logger import logger
import sqlite3


filename = "database.db"

def get_database():
    return sqlite3.connect(filename)

def create_database():
    try:
        cur = get_database().cursor()
        command = "CREATE TABLE IF NOT EXISTS config(key TEXT PRIMARY KEY, value TEXT)"
        cur.execute(command)
        logger.info("Opened database %s"%filename)
        insert_value("amazon_link","https://www.amazon.com/2021-Apple-10-2-inch-iPad-Wi-Fi/dp/B09G9CJM1Z")
    except Exception as e:
        logger.error("Failed to open database %s"%filename)

def insert_value(key, value):
    try:
        con = get_database()
        cur = con.cursor()
        command = 'INSERT OR REPLACE INTO config(key,value) VALUES ("{key}","{value}")'.format(key = key, value = value)
        cur.execute(command)
        con.commit()
        log = "Added key: {key} and value: {value} to database {filename}".format(key = key, value = value, filename = filename)
        logger.info(log)
    except Exception as e:
        print(e)
        log = "Failed to add key: {key} and value: {value} to database {filename}".format(key = key, value = value, filename = filename)
        logger.error(log)

def get_key(key):
    try:
        value = None
        cur = get_database().cursor()
        command = 'SELECT value FROM config WHERE key="{key}"'.format(key = key)
        value = cur.execute(command).fetchone()[0]
        log = "Successfully retrieved key: {key} and value: {value} from database {filename}".format(key = key, value = value, filename = filename)
        logger.info(log)
        return value
    except Exception as e:
        log = "Failed to retrieve key: {key} from database {filename}".format(key = key, value = value, filename = filename)
        logger.error(log)
        return None
