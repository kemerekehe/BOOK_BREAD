from typing import List, Dict, Any
from abc import ABC, abstractmethod
from ..Entities.Book import Book

class BookRepositoryInterface:
    @abstractmethod
    def browse(self) -> List[Book]:
        pass

    def read(self,book_id:int) -> Book:
        pass

    def add(self, book_data: dict) -> int:
        pass

    def edit(self, book_id:int, book_data: Dict[str, Any]) -> bool:
        pass

    def delete(self, book_id) -> bool:
        pass