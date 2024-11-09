import csv
from .base import IP2CountryDatabase
from app.constants import DATA_FILE_PATH

class CSVDatabase(IP2CountryDatabase):
    def __init__(self, file_path=DATA_FILE_PATH):
        self.ip_data = []
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.ip_data.append({
                    'ip': row['ip'],
                    'city': row['city'],
                    'country': row['country']
                })

    def lookup(self, ip_address: str) -> dict:
        # Override lookup the base class method
        for entry in self.ip_data:
            if entry['ip'] == ip_address:
                return {
                    'country': entry['country'],
                    'city': entry['city']
                }
        return None
