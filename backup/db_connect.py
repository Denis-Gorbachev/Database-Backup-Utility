import mysql.connector
import psycopg2
import pymongo

def db_connect(db_type, config, logger):
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
        logger.info("Connection successful")
        return conn
    except Exception as e:
        print(f"Connection failed: {e}")
        logger.error(f"Connection failed: {e}")
        return None
    