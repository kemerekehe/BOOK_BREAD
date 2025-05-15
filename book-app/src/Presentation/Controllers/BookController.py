from typing import Dict, Any, List
from src.Application.Services.BookServices import BookServices
from src.Domain.Entities.Book import Book

class BookController:
    def __init__(self, service: BookServices):
        self.service = service

    def get_all_books(self) -> List[Book]:
        return self.service.browse()

    def get_book_by_id(self, book_id: int) -> Book:
        return self.service.read(book_id)

    def create_book(self, book_data: Dict[str, Any]) -> int:
        return self.service.add(book_data)

    def update_book(self, book_id: int, book_data: Dict[str, Any]) -> bool:
        return self.service.edit(book_id, book_data)

    def delete_book(self, book_id: int) -> bool:
        return self.service.delete(book_id)
