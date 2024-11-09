import pytest
from app.database.csv_database import CSVDatabase
import os

@pytest.fixture
def test_csv_file(tmp_path):
    # Create a temporary CSV file for testing
    csv_content = """ip,city,country
1.1.1.1,Sydney,Australia
2.2.2.2,London,United Kingdom
8.8.8.8,Mountain View,United States"""
    
    csv_file = tmp_path / "test_ip_data.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)

def test_csv_database_initialization(test_csv_file):
    db = CSVDatabase(test_csv_file)
    assert len(db.ip_data) == 3

def test_csv_database_lookup(test_csv_file):
    db = CSVDatabase(test_csv_file)
    
    # Test successful lookup
    result = db.lookup("1.1.1.1")
    assert result == {"country": "Australia", "city": "Sydney"}
    
    # Test non-existent IP
    result = db.lookup("3.3.3.3")
    assert result is None 