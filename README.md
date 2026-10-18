# Database Management Application

A simple database management application developed for **CT80A0000 – Data-Intensive Systems**, Assignment T2.

The application provides a web-based interface for accessing and modifying data stored in three separate SQLite databases. It is built using **Python, SQLite, and Streamlit**.

## Features

- **Three independent databases:** Students, Products, and Employees.
- **Database selection:** Switch between databases using a dropdown menu.
- **View records:** Display the contents of the selected database.
- **Add records:** Insert new entries using a popup form.
- **Edit records:** Modify existing entries using the edit button on each row.
- **Delete records:** Select and delete multiple entries with a confirmation dialog.
- **Persistent storage:** Changes are saved to SQLite database files.
- **Dummy data:** Each database is automatically initialized with sample records.

## Technologies

- **Python** – Application logic and database operations
- **SQLite** – Database management and persistent storage
- **Streamlit** – Web-based user interface
- **Pandas** – Reading and displaying database records

## Installation and Usage

### 1. Requirements

Make sure you have Python 3 installed.

### 2. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Alternatively, download the repository as a ZIP file and extract it.

### 3. Install dependencies

```bash
pip install streamlit pandas
```

SQLite is included in Python's standard library and does not require separate installation.

### 4. Run the application

```bash
python -m streamlit run app.py
```

The application should automatically open in your default web browser.

If it does not, navigate to:

**http://localhost:8501**

## Database Structure

The application uses three separate SQLite database files, each containing one table.

| Database | Table | Fields |
|---|---|---|
| `students.db` | students | id, name, age, major |
| `products.db` | products | id, name, price, quantity |
| `employees.db` | employees | id, name, department, salary |

The databases and their initial dummy data are created automatically when the application is first launched.

## Demonstration

A video demonstrating the application's features and functionality is available on YouTube.

**[Watch the Demo Video](https://youtu.be/CYKuVDZ-7FA)**

## Course Information

**Course:** CT80A0000 – Data-Intensive Systems  
**Assignment:** T2 – Database Application  
**Purpose:** Demonstrate database access, selection, and data modification through a graphical user interface.
