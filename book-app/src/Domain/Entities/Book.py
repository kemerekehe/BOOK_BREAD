import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
class Book:
    def __init__(self, title: str, author: str, published_year: int, quantity: int):
        if not title or not author or not published_year or not quantity:
            raise ValueError("Data cannot be empty.")
        
        try:
            self.published_year = int(published_year)
        except ValueError:
            raise ValueError("Published year must be a valid integer.")

        try:
            self.quantity = int(quantity)
        except ValueError:
            raise ValueError("Quantity must be an integer and greater than zero.")
        
        self.title = title
        self.author = author
        self.published_year = published_year
        self.quantity = quantity


