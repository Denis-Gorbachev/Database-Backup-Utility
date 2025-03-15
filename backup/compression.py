import tarfile
import os

def compress_backup(backup_file, output_file, logger):
    try:
        if not os.path.isfile(backup_file):
            logger.error("Backup file doesn't exists") 
            raise FileNotFoundError("Backup file doesnt exists")
        
        with tarfile.open(output_file, "w:gz") as tar:
            tar.add(backup_file, arcname=os.path.basename(backup_file))
            logger.info(f"Backup file compressed at {output_file}")
            
    except tarfile.TarError as e:
        logger.error(f"Error while compressing file {backup_file}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while compressing: {e}")
        raise
