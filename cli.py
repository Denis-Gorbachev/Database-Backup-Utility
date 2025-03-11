import argparse
import logging
import json
import backup.db_connect as db_connect
import backup.backup as backup
import backup.restore as restore

def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
def main():
    parser = argparse.ArgumentParser("Database backup utility")
    parser.add_argument('operation', choices=['backup', 'restore'], help="Operation to perform: backup or restore")
    parser.add_argument('--db-type', required=True, choices=['postgresql', 'mysql', 'mongodb'], help="Database type (mysql, postgresql, mongodb)")
    parser.add_argument('--config', required=True, help="Path to JSON configuration file for database connection")

    parser.add_argument('--output', help="Output backup file path")
    parser.add_argument('--compress', action='store_true', help="Compress backup")

    parser.add_argument('--log-file', help="Log file path", default='backup.log')

    args = parser.parse_args()

    setup_logging(args.log_file)
    logging.info(f"Starting {args.operation} operation")

    try:
        with open(args.config) as conf_file:
            config = json.load(conf_file)
            db_config = config['database']

    except: 
        logging.error(f"Error opening file {args.config}")
        print(f"Error opening file {args.config}")
        return

    required_keys = ['host', 'port', 'user', 'password', 'database']
    for key in required_keys:
        if key not in db_config:
            logging.error(f"Config is missing required database configuration key: {key}")
            print(f"Config is missing required database configuration keys: {key}")
            return

    try:
        if args.operation == 'backup':
            conn = db_connect.db_connect(args.db_type, db_config, logging)
            if conn:
                backup.db_backup(args.db_type, db_config['database'], db_config, args.output, logging)
        elif args.operation == 'restore':
            restore.db_restore(args.db_type, db_config['database'], db_config, args.output, logging)
    except Exception as e:
        logging.error(f"An error occured during {args.operation} operation")

if __name__ == "__main__":
    main()