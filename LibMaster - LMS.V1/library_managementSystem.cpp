#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace std;

class Book {
public:
    int id;
    string title;
    string author;

    Book() {} // Default constructor

    Book(int i, string t, string a) : id(i), title(t), author(a) {} // Parameterized constructor
};

void addBook() {
    ofstream file("books.txt", ios::app); // Open file in append mode

    int id;
    string title, author;

    cout << "Enter Book ID: ";
    cin >> id;
    cin.ignore(); // To ignore newline character
    cout << "Enter Book Title: ";
    getline(cin, title);
    cout << "Enter Author Name: ";
    getline(cin, author);

    file << id << "," << title << "," << author << endl; // Save to file
    file.close();

    cout << "Book added successfully!" << endl;
}


void viewBooks() {
    ifstream file("books.txt");
    if (!file) {
        cout << "No books found!" << endl;
        return;
    }

    int id;
    string title, author;

    cout << "ID\tTitle\tAuthor" << endl;
    while (file >> id) {
        getline(file, title, ','); // Read title until comma
        getline(file, author);     // Read author
        cout << id << "\t" << title << "\t" << author << endl;
    }
    file.close();
}


void searchBook() {
    ifstream file("books.txt"); // Open the file for reading
    if (!file) {
        cout << "No books found!" << endl;
        return;
    }

    string searchTitle, title, author;
    int id;
    bool found = false;

    cout << "Enter Book Title to Search: ";
    cin.ignore(); // Clear input buffer
    getline(cin, searchTitle);

    cout << "\nSearching for Book...\n";

    while (file >> id) {
        file.ignore(); // Ignore the comma
        getline(file, title, ',');
        getline(file, author);

        if (title == searchTitle) {
            cout << "\nBook Found!" << endl;
            cout << "ID: " << id << endl;
            cout << "Title: " << title << endl;
            cout << "Author: " << author << endl;
            found = true;
            break;
        }
    }

    if (!found) {
        cout << "Book not found!" << endl;
    }

    file.close();
}


void deleteBook() {
    ifstream file("books.txt");
    ofstream temp("temp.txt");

    int id, deleteId;
    string title, author;

    cout << "Enter Book ID to Delete: ";
    cin >> deleteId;

    bool found = false;

    while (file >> id) {
        getline(file, title, ',');
        getline(file, author);
        if (id == deleteId) {
            found = true;
            continue; // Skip the book to delete
        }
        temp << id << "," << title << "," << author << endl;
    }
    file.close();
    temp.close();

    remove("books.txt"); // Delete old file
    rename("temp.txt", "books.txt"); // Rename temp file to books.txt

    if (found)
        cout << "Book deleted successfully!" << endl;
    else
        cout << "Book not found!" << endl;
}


int main() {
    int choice;

    while (true) {
        cout << "\nLibrary Management System" << endl;
        cout << "1. Add Book" << endl;
        cout << "2. View Books" << endl;
        cout << "3. Search Book" << endl;
        cout << "4. Delete Book" << endl;
        cout << "5. Exit" << endl;

        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
        case 1: addBook(); break;
        case 2: viewBooks(); break;
        case 3: searchBook(); break;
        case 4: deleteBook(); break;
        case 5: cout << "Exiting program. Goodbye!" << endl; return 0;
        default: cout << "Invalid choice! Try again." << endl;
        }
    }
    return 0;
}

