from main import BooksCollector
import pytest


class TestBooksCollector:

    # проверяем, что после инициализации словарь books_genre пустой.
    def test_initial_books_genre_empty(self, collector):
        assert collector.get_books_genre() == {}

    # проверяем, что после инициализации список избранного пустой.
    def test_initial_favorites_empty(self, collector):
        assert collector.get_list_of_favorites_books() == []
    
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
   
    # проверка установки существующего жанра книге 
    @pytest.mark.parametrize('name, genre, expected_genre', [
    ('Книга_1', 'Фантастика', 'Фантастика'),
    ('Книга_2', 'Ужасы', 'Ужасы'),
    ('Книга_3', 'Детективы', 'Детективы'),
    ('Книга_4', 'Мультфильмы', 'Мультфильмы'),
    ('Книга_5', 'Комедии', 'Комедии')             
    ])
    def test_set_book_genre_all_valid_genres(self, collector, name, genre, expected_genre):
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == expected_genre

    # проверка установки несуществующего жанра книге 
    @pytest.mark.parametrize('name, genre, expected_genre', [
    ('Книга_отсутствует_жанр', '', ''),
    ('Книга_недопустимый_жанр', 'Роман', '')               
    ])
    def test_set_book_genre_with_invalid_genre_returns_empty(self, collector, name, genre, expected_genre):
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == expected_genre

    # проверка получения списка книг с допустимыми жанрами (включая жанры, по которым нет книг)
    @pytest.mark.parametrize('genre, expected_books', [
    ('Фантастика', ['Книга_1']),
    ('Ужасы', ['Книга_2']),
    ('Детективы', []),
    ('Мультфильмы', ['Книга_3']),
    ('Комедии', ['Книга_4', 'Книга_5'])
    ])
    def test_get_books_with_specific_genre_valid_genres(self, collector_with_books, genre, expected_books):
        assert collector_with_books.get_books_with_specific_genre(genre) == expected_books

    # проверка получения пустого списка книг с недопустимыми жанрами
    @pytest.mark.parametrize('invalid_genre', [
    'Неизвестный жанр',
    ''   
    ])
    def test_get_books_with_specific_genre_invalid_genre_returns_empty(self, collector_with_books, invalid_genre):
        assert collector_with_books.get_books_with_specific_genre(invalid_genre) == []

    # проверяем, что после добавления двух книг, метод get_books_genre возвращает корректное кол-во в словаре
    def test_add_new_book_added_two_books(self, collector):
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    # проверка получения списка книг, подходящих детям 
    def test_get_books_for_children_mixed_genres_returns_only_allowed(self, collector):
        books_dict = {'Книга_1': 'Фантастика', 'Книга_2': 'Ужасы', 'Книга_3': 'Детективы',
         'Книга_4': 'Мультфильмы', 'Книга_5': 'Комедии'}
        expected_for_children = ['Книга_1', 'Книга_4', 'Книга_5']
        for name, genre in books_dict.items():
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        assert sorted(collector.get_books_for_children()) == sorted(expected_for_children)

    # проверка, что если все книги имеют возрастные жанры, результат пуст
    def test_get_books_for_children_only_adult_genres_returns_empty(self, collector):
        books = {
        'Книга_1': 'Ужасы',
        'Книга_2': 'Детективы'
        }
        for name, genre in books.items():
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)
        assert collector.get_books_for_children() == []

    # проверка, что для пустой коллекции метод возвращает пустой список
    def test_get_books_for_children_empty_collection_returns_empty(self, collector):
        assert collector.get_books_for_children() == []

    # проверка успешного добавления книги в избранное 
    def test_add_book_in_favorites_success(self, collector):
        collector.add_new_book('Жизнь')
        collector.add_book_in_favorites('Жизнь')
        assert collector.get_list_of_favorites_books() == ['Жизнь']

    # проверка, что нельзя добавить в избранное книгу, отсутствующую в коллекции
    def test_add_book_in_favorites_does_not_add_missing_book(self, collector):
        collector.add_book_in_favorites('Жизнь')
        assert collector.get_list_of_favorites_books() == []

    # проверка, что повторное добавление той же книги не создаёт дубликат
    def test_add_book_in_favorites_no_duplicate_on_multiple_adds(self, collector):
        collector.add_new_book('Жизнь')
        collector.add_book_in_favorites('Жизнь')
        collector.add_book_in_favorites('Жизнь')
        assert collector.get_list_of_favorites_books() == ['Жизнь']

    # проверка успешного удаления книги из избранного
    def test_delete_book_from_favorites_success(self, collector):
        collector.add_new_book('Жизнь')
        collector.add_book_in_favorites('Жизнь')
        collector.delete_book_from_favorites('Жизнь')  
        assert collector.get_list_of_favorites_books() == []

    # проверка, что повторное удаление удалённой книги не вызывает ошибок и не меняет список
    def test_delete_book_from_favorites_multiple_calls_safe(self, collector):
        collector.add_new_book('Жизнь')
        collector.add_book_in_favorites('Жизнь')
        collector.delete_book_from_favorites('Жизнь')
        collector.delete_book_from_favorites('Жизнь')
        assert collector.get_list_of_favorites_books() == []
    
    # проверка, что попытка удалить книгу, отсутствующую в избранном, не меняет список
    def test_delete_book_from_favorites_does_nothing_if_book_not_in_favorites(self, collector):
        collector.add_new_book('Жизнь')
        collector.add_book_in_favorites('Жизнь')
        collector.delete_book_from_favorites('Петр 1')
        assert collector.get_list_of_favorites_books() == ['Жизнь']

        