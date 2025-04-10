import json
import os
from typing import Dict, List, Optional, TypeVar, Generic
from pathlib import Path

T = TypeVar('T')

class JsonDatabase(Generic[T]):
    """! @brief A simple JSON-based database implementation.
    
    This class provides basic database operations using JSON files for storage.
    Each model type will be stored in its own JSON file.
    """
    
    def __init__(self, filename: str):
        """Initialize the database with a specific JSON file."""
        self.filename = filename
        self.db_path = Path('./data')
        self.db_path.mkdir(exist_ok=True)
        self.file_path = self.db_path / filename
        
        # Initialize empty database file if it doesn't exist
        if not self.file_path.exists():
            self.save_data([])
    
    def load_data(self) -> List[Dict]:
        """Load data from the JSON file."""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_data(self, data: List[Dict]) -> None:
        """Save data to the JSON file."""
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def insert(self, item: T) -> None:
        """Insert a new item into the database."""
        data = self.load_data()
        # Convert Pydantic model to dict if necessary
        item_dict = item.model_dump() if hasattr(item, 'model_dump') else dict(item)
        data.append(item_dict)
        self.save_data(data)
    
    def get_all(self) -> List[Dict]:
        """Retrieve all items from the database."""
        return self.load_data()
    
    def find_by_field(self, field: str, value: any) -> Optional[Dict]:
        """Find an item by a specific field value."""
        data = self.load_data()
        for item in data:
            if item.get(field) == value:
                return item
        return None
    
    def update_by_field(self, field: str, value: any, new_data: Dict) -> bool:
        """Update an item identified by a field with new data."""
        data = self.load_data()
        for i, item in enumerate(data):
            if item.get(field) == value:
                data[i].update(new_data)
                self.save_data(data)
                return True
        return False
    
    def delete_by_field(self, field: str, value: any) -> bool:
        """Delete an item by a specific field value."""
        data = self.load_data()
        initial_length = len(data)
        data = [item for item in data if item.get(field) != value]
        if len(data) != initial_length:
            self.save_data(data)
            return True
        return False
