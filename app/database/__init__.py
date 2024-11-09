from .csv_database import CSVDatabase
from app.constants import DATA_FILE_PATH

def get_ip2country_db(db_type: str):
    # DB type should inherit from BaseDatabase and implement the lookup method
    if db_type == "csv":
        return CSVDatabase()
    else:
        raise ValueError(f"Unsupported database type: {db_type}") 