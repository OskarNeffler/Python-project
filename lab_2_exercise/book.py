from typing import Any
import requests


class BookRecommendationSystem:
    def __init__(self, file_name: str = "books.json"):
        """
        Initialize the BookRecommendationSystem.

        Args:
            file_name: The file where book data is stored locally.
        """
        self.file_name = file_name
        self.books = self._fetch_all_books()

    def list_books(self, limit: int = None) -> list[dict[str, Any]]:
        """
        Return a list of books. If the limit is provided, return that many books.

        Args:
            limit: The maximum number of books to return.

        Returns:
            A list of dictionaries representing the books.
        """
        if limit:
            return self.books[:limit]
        return self.books

    def _fetch_all_books(self, limit: int = None) -> list[dict[str, Any]]:
        """
        Fetch all books from the API, with an optional limit.

        Args:
            limit: Optional limit on the number of books to fetch.

        Returns:
            A list of dictionaries containing book information.

        Raises:
            requests.RequestException: If there's an error with the API request.
        """
        #https://freetestapi.com/api/v1/books
        #https://freetestapi.com/api/v1/books?limit={limit}
        try:
            response = requests.get(f"https://freetestapi.com/api/v1/books?limit={limit}")
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException:
            raise requests.RequestException("Book API does not work")

    def get_book_details(self, book_id: int) -> dict[str, Any]:
        """
        Fetch detailed information about a specific book using its ID.

        Args:
            book_id: The unique identifier for the book.

        Returns:
            A dictionary containing detailed book information.

        Raises:
            ValueError: If the book_id is not found.
        """
        for book in self.books:
            if book["id"] == book_id:
                return book
        raise ValueError(f"Book with ID {book_id} not found")

    def search_books(self, query: str) -> list[dict[str, Any]]:
        """
        Search for books using a query string.

        Args:
            query: The search query string.

        Returns:
            A list of dictionaries containing book information matching the search query.

        Raises:
            requests.RequestException: If there's an error with the API request.
        """
        try:
            response = requests.get(f"https://freetestapi.com/api/v1/books?search={query}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            raise requests.RequestException("Error searching for books")

    def create_reading_list(self, name: str) -> None:
        """
        Create a new reading list with the given name.

        Args:
            name: The name of the reading list.

        Raises:
            ValueError: If a reading list with the same name already exists.
        """
        if name in self.reading_lists:
            raise ValueError(f"Reading list '{name}' already exists.")
        self.reading_lists[name] = []

    def add_to_reading_list(self, list_name: str, book_id: int) -> None:
        """
        Add a book to a specified reading list.

        Args:
            list_name: The name of the reading list.
            book_id: The unique identifier of the book to add.

        Raises:
            ValueError: If the list_name doesn't exist or the book is already in the list.
        """
        if list_name not in self.reading_lists:
            raise ValueError(f"Reading list '{list_name}' does not exist.")
        book = self.get_book_details(book_id)
        if book in self.reading_lists[list_name]:
            raise ValueError(f"Book with ID {book_id} is already in the reading list.")
        self.reading_lists[list_name].append(book)

    def get_reading_list(self, list_name: str) -> list[dict[str, Any]]:
        """
        Retrieve all books in a specified reading list.

        Args:
            list_name: The name of the reading list.

        Returns:
            A list of dictionaries containing book information for all books in the list.

        Raises:
            ValueError: If the list_name doesn't exist.
        """
        if list_name not in self.reading_lists:
            raise ValueError(f"Reading list '{list_name}' does not exist.")
        return self.reading_lists[list_name]

    def recommend_books_by_genre(self, genre: str, max_recommendations: int = 5) -> list[dict[str, Any]]:
        """
        Recommend books based on a specified genre.

        Args:
            genre: The genre to base recommendations on.
            max_recommendations: Maximum number of recommendations to return (default 5).

        Returns:
            A list of dictionaries containing information about recommended books.
        """
        recommendations = [book for book in self.books if genre in book.get("genre", [])]
        return recommendations[:max_recommendations]

    def export_reading_list_to_json(self, list_name: str) -> None:
        """
        Export a reading list to a JSON file.

        Args:
            list_name: The name of the reading list to export.

        Raises:
            ValueError: If the list_name doesn't exist.
            IOError: If there's an error writing to the file.
        """
        if list_name not in self.reading_lists:
            raise ValueError(f"Reading list '{list_name}' does not exist.")
        try:
            with open(f"{list_name}.json", "w") as file:
                json.dump(self.reading_lists[list_name], file)
        except IOError as e:
            raise IOError(f"Error writing to file: {e}")
