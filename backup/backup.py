import subprocess

def db_backup(db_type, db_name, config, output_file, logger):
    try:
        match db_type:
            case "mysql":
                command = ["mysqldump", '-u', config['user'], f"-p{config['password']}", db_name]
                with open(output_file, 'w') as f:
                    subprocess.run(command, stdout=f, check=True)
                logger.info(f"MySQL backup of {db_name} completed successfully, saved to {output_file}")

            case "posgresql":
                command = ["psql", '-U', config['user'],"-F", "c", "-b","-f", output_file, db_name]
                subprocess.run(command, check=True)
                logger.info(f"PostgreSQL backup of {db_name} completed successfully, saved to {output_file}")
            case "mongodb":
                command = ["mongodump", "--db", db_name, "--out", output_file]
                subprocess.run(command, check=True)
                logger.info(f"MongoDB backup of {db_name} completed successfully, saved to {output_file}")
            case _:
                logger.error(f"Unsupported database type: {db_type}")
                raise ValueError(f"Unsupported database type: {db_type}")
                
    except subprocess.SubprocessError() as e:
        logger.error(f"Error occurred during backup of {db_name} with {db_type}: {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error during backup: {e}")
        raise

    return output_file