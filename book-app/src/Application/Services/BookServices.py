from typing import List, Optional, Dict, Any
from src.Domain.Interfaces.BookInterface import BookRepositoryInterface
from src.Domain.Entities.Book import Book

class BookServices:

    def __init__(self, book_repository: BookRepositoryInterface):
        self._repository = book_repository

    def browse(self) -> List[Book]:
        return self._repository.browse()

    def read(self, book_id: int) -> Book:
        book = self._repository.read(book_id)
        if not book:
            raise ValueError(f"Book with ID {book_id} not found")
        return book

    def add(self, book_data: Dict[str, Any]) -> int:
        self._validate_book_data(book_data)
        return self._repository.add(book_data)

    def edit(self, book_id: int, book_data: Dict[str, Any]) -> bool:
        if book_data:
            self._validate_book_data(book_data, is_update=True)
        
        success = self._repository.edit(book_id, book_data)
        if not success:
            raise ValueError(f"Book with ID {book_id} not found")
        return True

    def delete(self, book_id: int) -> bool:
        success = self._repository.delete(book_id)
        if not success:
            raise ValueError(f"Book with ID {book_id} not found")
        return True
    def _validate_book_data(self, book_data: Dict[str, Any], is_update: bool = False) -> None:
        required_fields = {'title', 'author', 'published_year', 'quantity'}

        if not is_update:
            missing_fields = required_fields - book_data.keys()
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        validators = {
            'title': self._validate_non_empty_string,
            'author': self._validate_non_empty_string,
            'published_year': self._validate_positive_integer,
            'quantity': self._validate_non_negative_integer
        }

        for field, validator in validators.items():
            if field in book_data:
                validator(field, book_data[field])

    def _validate_non_empty_string(self, field: str, value: Any) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field.capitalize()} must be a non-empty string")

    def _validate_positive_integer(self, field: str, value: Any) -> None:
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{field.capitalize()} must be a positive integer")

    def _validate_non_negative_integer(self, field: str, value: Any) -> None:
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"{field.capitalize()} must be a non-negative integer")
