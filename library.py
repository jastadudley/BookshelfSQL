import sqlite3

#=========================================================================================================================
# BookshelfSQL - Book databse Managment System
# Author: Jasta Dudley
# Description: Creates and  manages a realational book database using SQLite. Demonstrates full CRUD operations and JOIN
# queries across multiple tables.
#=========================================================================================================================

# Connect to the database (and creates the file if it does not alreayd exist.)
conn = sqlite3.connect('bookshelf.db')
cursor = conn.cursor()

#--------------------------------------------------CREATES THE TABLES------------------------------------------------------

#Authors table
cursor.execute('''
     CREATE TABLE IF NOT EXISTS authors (
          author_id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          nationality TEXT
     )
''')

# Genres table
cursor.execute('''
      CREATE TABLE IF NOT EXISTS genres (
          genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
          genre_name TEXT NOT NULL
     )
               
''')

# Books table
cursor.execute('''
     CREATE TABLE IF NOT EXISTS books (
          book_id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          author_id INTEGER,
          genre_id INTEGER,
          year_published INTEGER,
          rating REAL,
          FOREIGN KEY (author_id) REFERENCES authors(author_id),
          FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
     )          
''')

#------------------------------------------------------------INSERT FUNCTIONS--------------------------------------------------
def add_author(name, nationality):
    # Adds  anew author to the authors table
    conn = sqlite3.connect('bookshelf.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO authors (name, nationality) values (?, ?)', (name, nationality))
    conn.commit()
    print(f"Author '{name}' added successfully.")
    conn.close()

def add_genre(genre_name,):
    # Adds a new genre to the genres table
    conn = sqlite3.connect('bookshelf.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO genres (genre_name) values (?)', (genre_name,))
    conn.commit()
    print(f"Genre '{genre_name}' added successfully.")
    conn.close()

def add_book(title, author_id, genre_id, year_published, rating):
    # Adds a new book to the books table
    conn = sqlite3.connect('bookshelf.db')
    cursor = conn.cursor()
    cursor.execute('''
          INSERT INTO books (title, author_id, genre_id, year_published, rating)
          VALUES (?, ?, ?, ?, ?)
     ''', (title, author_id, genre_id, year_published, rating))
    conn.commit()
    print(f"Book '{title}' added successfully.")
    conn.close()

#------------------------------------------------------------READ FUNCTIONS--------------------------------------------------
def get_all_books():
    # Retrieves all books fromt he books table
    conn = sqlite3.connect( 'bookshelf.db')
    cursor = conn.cursor()
    cursor.execute( 'SELECT * FROM books')
    books = cursor.fetchall()
    print("\n --------------------------ALL Books----------------------------")
    for book in books:
        print(book)
    conn.close()

def get_all_authors():
    # Retreaves all authors fromt the authors table
    conn = sqlite3.connect('bookshelf.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()
    print("\n----------------------------ALL Authors---------------------------")
    for author in authors:
        print(author)
    conn.close()
    
def get_books_with_details():
    # My JOIN query- retraieves books with their author name and genre name
    conn = sqlite3.connect('bookshelf.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT books.title, authors.name, genres.genre_name, books.year_published, books.rating
        FROM books
        JOIN authors ON books.author_id = authors.author_id
        JOIN genres ON books.genre_id = genres.genre_id
    ''')
    results = cursor.fetchall()
    print("\n---------------------------Books With Detail-----------------------")
    for row in results:
        print(f"Title: {row[0]} | Author: {row[1]} | Genre: {row[2]} | Year: {row[3]} | Rating: {row[4]}")
    conn.close()

#------------------------------------------------------------UPDATE FUNCTIONS-------------------------------------------------
def update_book_rating(book_id, new_rating):
    # Updates the rating of a book by it's ID
    conn = sqlite3.connect('bookshelf.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE books SET rating = ? wHERE book_id = ?', (new_rating, book_id))
    conn.commit()
    print(f"Book ID {book_id} rating updated to {new_rating}.")
    conn.close()

#------------------------------------------------------------DELETE FUNCTIONS--------------------------------------------------
def delete_book (book_id):
    # Deletes a book from the books table by its ID
    conn = sqlite3.connect('bookshelf.db')
    cursor = conn.cursor()
    cursor.execute( 'DELETE FROM books WHERE book_id = ?', (book_id,))
    conn.commit()
    print(f"Book ID {book_id} deleted successfully.")
    conn.close()

#----------------------------------------------------------------MAIN BLOCK-----------------------------------------------------
# This section runs all the functions to demonstrate the database working

if __name__ == "__main__":
    print("=================================== Setting Up BookshelfSQL Database ======================================")

    # Adding Authors
    add_author('Stephen King', 'American')
    add_author('Nancy Farmer', 'American')
    add_author('Frank Herbert', 'American')

    # Adding Genres
    add_genre('Horror Fiction')
    add_genre('Young Adult')
    add_genre('Science Fiction')

    # Adding books (first title, then author_id, Genre_id, year_published, rating)
    add_book ('The Shining', 1, 1, 1977, 4.2)
    add_book('The House of the Scorpion', 2, 2, 2002, 4.0)
    add_book('Dune', 3, 3, 1965, 4.2)

        # Read all books and authors
    get_all_books()
    get_all_authors()

    # Run the JOIN query
    get_books_with_details()

    # Update a riting on a book
    update_book_rating(1, 4.8)

    # Delete a book
    delete_book(3)

    # Show the final state of collection
    print("\n===================================== Final State of Database ========================================")
    get_books_with_details()