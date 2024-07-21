import pytest

import data


class TestBooksCollector:

    # Тест для метода add_new_book - добавление книги
    def test_add_first_book(self, collector):
        collector.add_new_book(data.BOOK_1)
        assert data.BOOK_1 in collector.books_genre
        assert collector.books_genre[data.BOOK_1] == ''

    # Тест для метода add_new_book - добавление двух книг
    def test_add_second_book(self, collector):
        collector.add_new_book(data.BOOK_1)
        collector.add_new_book(data.BOOK_2)
        assert len(collector.books_genre) == 2

    # Тест для метода add_new_book - добавление дубликата книги
    def test_add_duplicate_book(self, collector):
        collector.add_new_book(data.BOOK_1)
        initial_count = len(collector.books_genre)
        # Пытаемся добавить дубликат
        collector.add_new_book(data.BOOK_1)
        # Проверяем, что количество книг не изменилось
        assert len(collector.books_genre) == initial_count

    # Тест для метода add_new_book - передача невалидного по длине названия
    @pytest.mark.parametrize('book_name', [data.EMPTY_NAME, data.LONG_NAME])
    def test_add_new_book_invalid_length(self, collector, book_name):
        collector.add_new_book(book_name)
        assert len(collector.books_genre) == 0

    # Тест для метода set_book_genre - передача книги и жанра, которые есть в словаре и списке
    def test_set_book_genre_is_book_and_genre(self, book_data, collector):
        book_name, genre = book_data
        collector.set_book_genre(book_name, genre)
        assert collector.books_genre[book_name] == genre

    # Тест для метода set_book_genre - передача книги из словаря, с отсутствующим жанром
    # Проверяем, что метод не устанавливает жанр для книги не из списка доступных жанров
    def test_set_book_genre_not_genre(self, book_data, collector):
        book_name, genre = book_data
        invalid_genre = data.INVALID_GENRE
        collector.set_book_genre(book_name, invalid_genre)
        assert collector.books_genre[book_name] != invalid_genre

    # Тест для метода set_book_genre - проверяем, что метод не устанавливает жанр для несуществующей книги
    def test_set_book_genre_not_existent_book(self, collector):
        collector.set_book_genre(data.NON_EXISTENT_BOOK, data.GENRE_IS)
        assert data.NON_EXISTENT_BOOK not in collector.books_genre
        assert data.GENRE_IS not in collector.books_genre.values()

    # Тест для метода set_book_genre - проверяем, что метод корректно обновляет жанр у существующей книги
    def test_set_book_genre_updated_genre(self, book_data, collector):
        book_name, genre = book_data
        updated_genre = data.UPDATED_GENRE
        collector.set_book_genre(book_name, updated_genre)
        assert collector.books_genre[book_name] == updated_genre

    # Тест для метода get_book_genre - проверяем, что метод правильно возвращает жанр книги
    def test_get_book_genre_positive_t(self, collector, book_data):
        book_name, genre = book_data
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == genre

    # Тест для метода get_book_genre -проверяем, что метод возвращает None для несуществующей книги
    def test_get_book_genre_not_existe_book(self, collector):
        assert collector.get_book_genre(data.NON_EXISTENT_BOOK) is None

    # Тест для метода get_book_genre -проверяем, что метод возвращает '' для книги без жанра
    def test_get_book_genre_book_name_no_genre(self, collector):
        collector.add_new_book(data.BOOK_1)
        assert collector.get_book_genre(data.BOOK_1) == ''

    # Тест для метода get_books_with_specific_genre -проверяем, что метод возвращает книги с заданным жанром
    def test_get_books_with_specific_genre_existe_genre(self, collector):
        collector.add_new_book(data.BOOK_1)
        collector.set_book_genre(data.BOOK_1, data.GENRE_IS)
        collector.add_new_book(data.BOOK_2)
        collector.set_book_genre(data.BOOK_2, data.GENRE_IS)
        assert collector.get_books_with_specific_genre(data.GENRE_IS) == [data.BOOK_1, data.BOOK_2]

    # Тест для метода get_books_with_specific_genre -проверяем, что метод возвращает None для несуществующего жанра
    def test_get_books_with_specific_genre_invalid_genre(self, collector):
        collector.add_new_book(data.BOOK_1)
        collector.set_book_genre(data.BOOK_1, data.GENRE_IS)
        assert collector.get_books_with_specific_genre(data.INVALID_GENRE) == []

    # Тест для метода get_books_with_specific_genre - жанр из списка, но книги с указанным жанром не добавлялась
    def test_get_books_with_specific_genre_book_not_add(self, collector):
        assert collector.get_books_with_specific_genre(data.GENRE_IS) == []

    # Тест для метода get_books_genre - добавлена книга, установлен ей жанр
    def test_get_books_genre_one_book_with_genre(self, book_data, collector):
        book_name, genre = book_data
        collector.set_book_genre(book_name, genre)
        assert collector.get_books_genre() == {data.BOOK_1: data.GENRE_IS}

    # Тест для метода get_books_genre - добавлена одна книга, жанр не устанавливался
    def test_get_books_genre_one_book_add_without_genre(self, collector):
        collector.add_new_book(data.BOOK_1)
        assert collector.get_books_genre() == {data.BOOK_1: ''}

    # Тест для метода get_books_genre - проверяем, что если книга не добавлялась, то словарь пустой
    def test_get_books_genre_not_book(self, collector):
        assert collector.get_books_genre() == {}

    # Тест для метода get_books_for_children - книга подходит детям
    def test_get_books_for_children_book_suitable(self, collector):
        collector.add_new_book(data.BOOK_SUITABLE_FOR_CHILDREN)
        collector.set_book_genre(data.BOOK_SUITABLE_FOR_CHILDREN, data.GENRE_BOOK_SUITABLE_FOR_CHILDREN)
        assert collector.get_books_for_children() == [data.BOOK_SUITABLE_FOR_CHILDREN]

    # Тест для метода get_books_for_children - книга подходит детям, но жанр не передали
    def test_get_books_for_children_not_genre(self, collector):
        collector.add_new_book(data.BOOK_SUITABLE_FOR_CHILDREN)
        assert collector.get_books_for_children() == []

    # Тест для метода get_books_for_children - книга для взрослых
    def test_get_books_for_children_age_rating(self, collector):
        collector.add_new_book(data.BOOK_1)
        collector.set_book_genre(data.BOOK_1, data.GENRE_AGE_RATING)
        assert collector.get_books_for_children() == []

    # Тест для метода add_book_in_favorites - проверяем, что метод добавляет книгу в список избранных,
    # если она присутствует в списке всех книг и не была ранее добавлена
    def test_add_book_in_favorites_book_in_books_genre(self, collector):
        collector.add_new_book(data.BOOK_1)
        collector.add_book_in_favorites(data.BOOK_1)
        assert data.BOOK_1 in collector.favorites

    # Тест для метода add_book_in_favorites - проверяем, что метод не добавляет книгу повторно в список избранных
    def test_add_book_in_favorites_repeat_add_book(self, collector):
        collector.add_new_book(data.BOOK_1)
        collector.add_book_in_favorites(data.BOOK_1)
        collector.add_book_in_favorites(data.BOOK_1)
        assert collector.favorites.count(data.BOOK_1) == 1

    # Тест для метода add_book_in_favorites - добавление в избранное минуя словарь
    def test_add_book_in_favorites_not_existe_book(self, collector):
        collector.add_book_in_favorites(data.BOOK_1)
        assert  data.BOOK_1 not in collector.favorites

    # Тест для метода delete_book_from_favorites - удаление из избранного
    def test_delete_book_from_favorites_book_is_favorites(self, collector):
        collector.add_new_book(data.BOOK_1)
        collector.add_book_in_favorites(data.BOOK_1)
        collector.delete_book_from_favorites(data.BOOK_1)
        assert data.BOOK_1 not in collector.favorites

    # Тест для метода delete_book_from_favorites - пытаемся удалить книгу, которая уже отсутствует в списке избранных
    def test_delete_book_from_favorites_repeat_delete(self, collector):
        collector.add_new_book(data.BOOK_1)
        collector.add_book_in_favorites(data.BOOK_1)
        collector.delete_book_from_favorites(data.BOOK_1)
        collector.delete_book_from_favorites(data.BOOK_1)
        assert data.BOOK_1 not in collector.favorites

    # Тест для метода delete_book_from_favorites - удаление книги, которую не добавляли в избранное
    def test_delete_book_from_favorites_book_isnt_favorites(self, collector):
        collector.add_new_book(data.BOOK_1)
        collector.delete_book_from_favorites(data.BOOK_1)
        assert data.BOOK_1 not in collector.favorites

    # Тест для метода get_list_of_favorites_books - добавлена одна книга
    def test_get_list_of_favorites_books_one_book(self, collector):
        collector.add_new_book(data.BOOK_1)
        collector.add_book_in_favorites(data.BOOK_1)
        assert collector.get_list_of_favorites_books() == [data.BOOK_1]

    # Тест для метода get_list_of_favorites_books - добавлено две книги
    def test_get_list_of_favorites_books_two_books(self, collector):
        collector.add_new_book(data.BOOK_1)
        collector.add_book_in_favorites(data.BOOK_1)
        collector.add_new_book(data.BOOK_2)
        collector.add_book_in_favorites(data.BOOK_2)
        assert len(collector.get_list_of_favorites_books()) == 2

    # Тест для метода get_list_of_favorites_books - книги не добавлялись
    def test_get_list_of_favorites_not_books(self, collector):
        assert collector.get_list_of_favorites_books() == []