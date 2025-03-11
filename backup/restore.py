import subprocess

def db_restore(db_type, db_name, config, backup_file, logger):
    try:
        match db_type:
            case "mysql":
                command = [
                    "mysql", "-u", config['user'], "-p" + config['password'], "-h", config.get('host', 'localhost'), "-P", str(config.get('port', 3306)), config['database']]
                with open(backup_file, 'r') as f:
                    subprocess.run(command, stdin=f, check=True)
                    logger.info(f"MySQL database {db_name} restored successfully from {backup_file}")
            case "postgresql":
                command = [
                    "pg_restore", "-U", config['user'], "-h", config.get('host', 'localhost'), "-p", str(config.get('port', 5432)), "-d", config['database'], "-v", backup_file]
                subprocess.run(command, check=True)
                logger.info(f"PostgreSQL database {db_name} restored successfully from {backup_file}")
            case "mongodb":
                command = [
                    "mongorestore", "--host", config.get('host', 'localhost'), "--port", str(config.get('port', 27017)), "--db", config['database'], backup_file]
                subprocess.run(command, check=True)
                logger.info(f"MongoDB database {db_name} restored successfully from {backup_file}")
                
    except Exception as e:
        logger.error(f"Error occured in restoration database {db_name}: {e}")
        print(f"Error occured in restoration database {db_name}: {e}")