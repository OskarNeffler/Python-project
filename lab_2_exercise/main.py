from typing import Any
import requests
from book import BookRecommendationSystem

def main() -> None:
    """
    The main function that runs the book recommendation application.
    """
    try:
        book_system = BookRecommendationSystem()
    except Exception as e:
        print(f"Error initializing the book system: {e}")
        return

    while True:
        print("\nBook Recommendation System Menu:")
        print("[1] - Fetch and list books")
        print("[2] - Get book details")
        print("[3] - Search for books")
        print("[4] - Create a new reading list")
        print("[5] - Add a book to a reading list")
        print("[6] - View a reading list")
        print("[7] - Get book recommendations by genre")
        print("[8] - Export a reading list to JSON")
        print("[9] - Exit the application")

        choice = input("Make a choice: ")

        if choice == "1":
            try:
                list_of_books = book_system.fetch_all_books()
                for book in list_of_books:
                    print(book.get("title", "No title available"))
            except requests.RequestException:
                print("API is not working, try again later.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == "2":
            try:
                book_system.list_books()
                book_id = input("Enter a book id: ")
                book = book_system.get_book_details(book_id=book_id)
                print(f"Title: {book.get('title', 'N/A')}")
                print(f"Author: {book.get('author', 'N/A')}")
                print(f"Description: {book.get('description', 'N/A')}")
                print(f"Genres: {', '.join(book.get('genre', []))}")
            except KeyError:
                print("Some book details are missing.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == "3":
            pass  # Implement search functionality here

        elif choice == "4":
            pass  # Implement create reading list functionality here

        elif choice == "5":
            pass  # Implement add book to reading list functionality here

        elif choice == "6":
            pass  # Implement view reading list functionality here

        elif choice == "7":
            pass  # Implement genre recommendation functionality here

        elif choice == "8":
            pass  # Implement export reading list to JSON functionality here

        elif choice == "9":
            print("Goodbye!")
            exit()

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
