import sys
import os
from dataclasses import dataclass
from typing import Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

@dataclass
class Book:
    title: str
    author: str
    published_year: int
    quantity: int
    id: Optional[int] = None

    def __post_init__(self):
        if not self.title or not self.author:
            raise ValueError("Title and author cannot be empty.")
        
        if not isinstance(self.published_year, int) or self.published_year <= 0:
            raise ValueError("Published year must be a positive integer.")

        if not isinstance(self.quantity, int) or self.quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")


