

import streamlit as st
import sqlite3
import pandas as pd

def initialize_databases():
    # Students database
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            major TEXT
        )
    """)

    # Add dummy data only if the table is empty
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO students (name, age, major) VALUES (?, ?, ?)",
            [
                ("Alice", 22, "Computer Science"),
                ("Bob", 24, "Business"),
                ("Charlie", 21, "Engineering")
            ]
        )

    conn.commit()
    conn.close()

    # Products database
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            quantity INTEGER
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)",
            [
                ("Keyboard", 49.99, 10),
                ("Mouse", 19.99, 25),
                ("Monitor", 179.99, 5)
            ]
        )

    conn.commit()
    conn.close()

    # Employees database
    conn = sqlite3.connect("employees.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            salary REAL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)",
            [
                ("Emma", "IT", 3500),
                ("Daniel", "Sales", 3000),
                ("Sophia", "HR", 3200)
            ]
        )

    conn.commit()
    conn.close()

    
def read_database(database, table):
    conn = sqlite3.connect(database)

    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)

    conn.close()
    return df


def add_record(database, table, values):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    # Create placeholders for SQL values
    placeholders = ", ".join(["?"] * len(values))

    # Insert the new record
    cursor.execute(
        f"INSERT INTO {table} VALUES (NULL, {placeholders})",
        values
    )

    conn.commit()
    conn.close()


def update_record(database, table, record_id, values):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    if table == "students":
        columns = ["name", "age", "major"]
    elif table == "products":
        columns = ["name", "price", "quantity"]
    elif table == "employees":
        columns = ["name", "department", "salary"]
    else:
        conn.close()
        raise ValueError("Unknown table")

    # Create SQL SET clause
    set_clause = ", ".join(f"{col} = ?" for col in columns)

    cursor.execute(
        f"UPDATE {table} SET {set_clause} WHERE id = ?",
        (*values, record_id)
    )

    conn.commit()
    conn.close()

    
def delete_record(database, table, record_id):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute(
        f"DELETE FROM {table} WHERE id = ?",
        (record_id,)
    )

    conn.commit()
    conn.close()


# Initialize databases when application starts
initialize_databases()



# Database configuration
database_options = {
    "Students": ("students.db", "students"),
    "Products": ("products.db", "products"),
    "Employees": ("employees.db", "employees")
}

initialize_databases()


# Clear selected checkboxes
def clear_selection(database_name):
    prefix = f"select_{database_name}_"

    for key in list(st.session_state.keys()):
        if key.startswith(prefix):
            del st.session_state[key]


# Shared input fields
def record_fields(database_name, record=None):

    if database_name == "Students":
        name = st.text_input(
            "Name",
            value=record["name"] if record is not None else ""
        )
        age = st.number_input(
            "Age",
            min_value=1,
            value=int(record["age"]) if record is not None else 18
        )
        major = st.text_input(
            "Major",
            value=record["major"] if record is not None else ""
        )
        return (name, age, major)

    elif database_name == "Products":
        name = st.text_input(
            "Product Name",
            value=record["name"] if record is not None else ""
        )
        price = st.number_input(
            "Price",
            min_value=0.0,
            value=float(record["price"]) if record is not None else 0.0
        )
        quantity = st.number_input(
            "Quantity",
            min_value=0,
            value=int(record["quantity"]) if record is not None else 0
        )
        return (name, price, quantity)

    elif database_name == "Employees":
        name = st.text_input(
            "Employee Name",
            value=record["name"] if record is not None else ""
        )
        department = st.text_input(
            "Department",
            value=record["department"] if record is not None else ""
        )
        salary = st.number_input(
            "Salary",
            min_value=0.0,
            value=float(record["salary"]) if record is not None else 0.0
        )
        return (name, department, salary)


# Add record popup
@st.dialog("Add New Record")
def add_dialog(database_name, database_file, table_name):

    with st.form("add_form"):
        values = record_fields(database_name)

        if st.form_submit_button("Add Record", type="primary"):
            if any(
                isinstance(v, str) and not v.strip()
                for v in values
            ):
                st.error("Please fill in all text fields.")
            else:
                add_record(database_file, table_name, values)
                st.rerun()


# Edit record popup
@st.dialog("Edit Record")
def edit_dialog(database_name, database_file, table_name, record):

    record_id = int(record["id"])
    st.caption(f"Record ID: {record_id}")

    with st.form("edit_form"):
        values = record_fields(database_name, record)

        if st.form_submit_button("Save Changes", type="primary"):
            if any(
                isinstance(v, str) and not v.strip()
                for v in values
            ):
                st.error("Please fill in all text fields.")
            else:
                update_record(
                    database_file, table_name, record_id, values
                )
                st.rerun()


# Delete confirmation popup
@st.dialog("Confirm Deletion")
def delete_dialog(database_name, database_file, table_name, ids):

    st.warning(
        f"Are you sure you want to permanently delete "
        f"{len(ids)} selected record(s)?"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cancel", use_container_width=True):
            st.rerun()

    with col2:
        if st.button(
            "Confirm Delete",
            type="primary",
            use_container_width=True
        ):
            for record_id in ids:
                delete_record(database_file, table_name, record_id)

            clear_selection(database_name)
            st.rerun()


# Main application
st.title("Database Management Application")

selected_database = st.selectbox(
    "Select a database:",
    list(database_options.keys())
)

database_file, table_name = database_options[selected_database]

st.subheader(f"{selected_database} Database")

if st.button("Add New Record", icon=":material/add:"):
    add_dialog(selected_database, database_file, table_name)

df = read_database(database_file, table_name)

# Table layout: checkbox, data columns, edit button
column_widths = [0.6] + [1.5] * len(df.columns) + [0.7]

# Header
header_cols = st.columns(column_widths, vertical_alignment="center")

header_cols[0].write("**Select**")

for i, column in enumerate(df.columns):
    header_cols[i + 1].write(f"**{column.capitalize()}**")

header_cols[-1].write("**Edit**")

st.divider()

selected_ids = []
edit_record = None

# Display each database row
for _, record in df.iterrows():

    record_id = int(record["id"])

    cols = st.columns(
        column_widths,
        vertical_alignment="center"
    )

    # Selection checkbox
    checked = cols[0].checkbox(
        "Select",
        key=f"select_{selected_database}_{record_id}",
        label_visibility="collapsed"
    )

    if checked:
        selected_ids.append(record_id)

    # Display database values
    for i, column in enumerate(df.columns):
        cols[i + 1].write(str(record[column]))

    # Pencil button
    if cols[-1].button(
        "",
        icon=":material/edit:",
        key=f"edit_{selected_database}_{record_id}",
        help="Edit this record"
    ):
        edit_record = record

# Delete button appears only when records are selected
if selected_ids:
    st.divider()

    st.write(f"{len(selected_ids)} record(s) selected")

    if st.button(
        f"Delete Selected ({len(selected_ids)})",
        icon=":material/delete:",
        type="primary"
    ):
        delete_dialog(
            selected_database,
            database_file,
            table_name,
            selected_ids
        )

# Open edit popup if a pencil button was clicked
if edit_record is not None:
    edit_dialog(
        selected_database,
        database_file,
        table_name,
        edit_record
    )
