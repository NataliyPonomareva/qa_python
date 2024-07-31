import pytest

from main import BooksCollector
import data


@pytest.fixture
def collector():
    """Фикстура для создания экземпляра BooksCollector."""
    collector = BooksCollector()
    return collector


@pytest.fixture
def book_data(collector):
    """Фикстура для установки начальных данных книги."""
    book_name = data.BOOK_1
    genre = data.GENRE_IS
    collector.books_genre[book_name] = ''  # Инициализируйте жанр как пустую строку
    return book_name, genre  # Возвращаем кортеж с данными