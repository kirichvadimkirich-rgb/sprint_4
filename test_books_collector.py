from main import BooksCollector
import pytest


class TestBooksCollector:

    # проверяем, что после инициализации словарь books_genre пустой.
    def test_initial_books_genre_empty(self, collector):
        assert collector.books_genre == {}

    # проверяем, что после инициализации список избранного пустой.
    def test_initial_favorites_empty(self, collector):
        assert collector.favorites == []

    # проверяем, что после инициализации список допустимых жанров задан.
    def test_initial_genre_list_true(self, collector):
        expected_genre = ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']
        assert collector.genre == expected_genre

    # проверяем, что после инициализации список жанров с возрастным рейтингом задан.
    def test_initial_genre_age_rating_true(self, collector):
        expected_age_rating = ['Ужасы', 'Детективы']
        assert collector.genre_age_rating == expected_age_rating
    
    # проверяем добавления книги с разной длиной имени.
    @pytest.mark.parametrize('name, expected_in_collection', [
    ('Гордость', True),
    ('Название из сорока символов 40 символов!', True),
    ('', False),
    ('f' * 41, False),
    ('Игры престолов', True)
    ])
    def test_add_new_book_handles_different_name_lengths(self, collector, name, expected_in_collection):
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == expected_in_collection
   
    # проверка установки жанра 
    @pytest.mark.parametrize('name, genre, expected_genre', [
    ('Книга_1', 'Фантастика', 'Фантастика'),
    ('Книга_2', 'Ужасы', 'Ужасы'),
    ('Книга_3', 'Детективы', 'Детективы'),
    ('Книга_4', 'Мультфильмы', 'Мультфильмы'),
    ('Книга_5', 'Комедии', 'Комедии'),
    ('Книга_недопустимый_жанр', 'Роман', '')               
    ])
    def test_set_book_genre_sets_genre_for_valid_and_returns_empty_for_invalid(self, collector, name, genre, expected_genre):
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == expected_genre
   
    # проверка получения списка книг определённого жанра.
    @pytest.mark.parametrize('genre, expected_books', [
    ('Фантастика', ['Книга_1']),
    ('Ужасы', ['Книга_2']),
    ('Детективы', []),
    ('Мультфильмы', ['Книга_3']),
    ('Комедии', ['Книга_4', 'Книга_5']),
    ('Неизвестный жанр', [])
    ])
    def test_get_list_books_with_specific_genre_for_valid_and_returns_empty_for_invalid(self, collector_with_books, genre, expected_books):
        assert collector_with_books.get_books_with_specific_genre(genre) == expected_books

    # проверяем, что после добавления двух книг, метод get_books_genre возвращает корректное кол-во в словаре
    @pytest.mark.parametrize('name_1, name_2', [
    ['Гордость и предубеждение и зомби', 'Что делать, если ваш кот хочет вас убить'] 
    ])
    def test_add_new_book_added_two_books(self, collector, name_1, name_2):
        collector.add_new_book(name_1)
        collector.add_new_book(name_2)
        assert len(collector.get_books_genre()) == 2

    # проверка получения списка книг, подходящих детям 
    @pytest.mark.parametrize('books_dict, expected_children', [
    (
        {'Книга_1': 'Фантастика', 'Книга_2': 'Ужасы', 'Книга_3': 'Детективы',
         'Книга_4': 'Мультфильмы', 'Книга_5': 'Комедии'},
        ['Книга_1', 'Книга_4', 'Книга_5']
    ),
    (
        {'Книга_6': 'Ужасы', 'Книга_7': 'Детективы'},
        []
    ),
    (
        {},
        []
    ),
    ])
    def test_get_books_for_children_with_mixed_genres(self, collector, books_dict, expected_children):
        for name, genre in books_dict.items():
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        assert sorted(collector.get_books_for_children()) == sorted(expected_children)


    # проверка добавления книги в избранное 
    @pytest.mark.parametrize('name_add_new_book, name_add_book_in_favorites, repeat_count, expected_list_book_in_favorites', [
    ('Жизнь', 'Жизнь', 1, ['Жизнь']),   
    ('', 'Жизнь', 1, []),             
    ('Жизнь', 'Жизнь', 2, ['Жизнь']),  
    ])
    def test_add_book_in_favorites_multiple_scenarios(self, collector, name_add_new_book, name_add_book_in_favorites, repeat_count, expected_list_book_in_favorites):
        collector.add_new_book(name_add_new_book)
        for _ in range(repeat_count):
            collector.add_book_in_favorites(name_add_book_in_favorites)
        assert collector.get_list_of_favorites_books() == expected_list_book_in_favorites 
    
    # удаляем книгу из Избранного
    @pytest.mark.parametrize('name_add_book_1, name_add_book_2, name_delete_book, repeat_count, expected_list_book_in_favorites', [
    ('Жизнь', 'Лидер КМ', 'Лидер КМ', 1, ['Жизнь']),               
    ('Жизнь', 'Лидер КМ', 'Петр 1', 1, ['Жизнь', 'Лидер КМ']),  
    ('Жизнь', 'Лидер КМ', 'Жизнь', 2, ['Лидер КМ'])
    ])
    def test_delete_book_from_favorites_multiple_scenarios(self, collector, name_add_book_1, name_add_book_2, name_delete_book, repeat_count, expected_list_book_in_favorites):
        collector.add_new_book(name_add_book_1)
        collector.add_new_book(name_add_book_2)
        collector.add_book_in_favorites(name_add_book_1)
        collector.add_book_in_favorites(name_add_book_2)
        for _ in range(repeat_count):
            collector.delete_book_from_favorites(name_delete_book)  
        assert collector.get_list_of_favorites_books() == expected_list_book_in_favorites
        