import pytest
from main import BooksCollector


@pytest.fixture
def collector():
    return BooksCollector()

@pytest.fixture
def collector_with_books(collector):
    books_with_genre = {'Книга_1': 'Фантастика', 'Книга_2': 'Ужасы', 'Книга_3': 'Мультфильмы', 
                         'Книга_4': 'Комедии', 'Книга_5': 'Комедии'}
    for name, genre in books_with_genre.items():
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
    return collector

