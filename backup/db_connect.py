import mysql.connector
import psycopg2
import pymongo

def db_connect(db_type, config):
    try:
        match db_type:
            case "mysql":
                conn = mysql.connector.connect(
                    host=config['host'], password=config['password'], database=config['database'])
            case "postgesql":
                conn = psycopg2.connect(
                    host=config['host'], password=config['password'], dbname=config['database'])
            case "mongodb":
                conn = pymongo.MongoClient(
                    f"mongodb://{config['host']}:{config['port']}")
        print("Connection successful")
        return conn
    except Exception as e:
        print(f"Connection failed: {e}")
        return None
    