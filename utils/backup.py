import shutil
from pathlib import Path
import datetime

class BackupManager:
    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self):
        """Create a backup of the database"""
        try:
            db_path = Path("data/agency.db")
            if not db_path.exists():
                return
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"agency_backup_{timestamp}.db"
            
            shutil.copy2(db_path, backup_path)
            return str(backup_path)
        except Exception as e:
            print(f"Backup failed: {str(e)}")
            return None

backup_manager = BackupManager() 