from tkinter import *
from tkinter import ttk
import sqlite3

# Создаем главное окно приложения
root = Tk()
root.title("Список сотрудников компании")

# Создаем и настраиваем treeview для отображения списка сотрудников
tree = ttk.Treeview(root, columns=("fio", "phone", "email", "salary"), show="headings")
tree.column("fio", width=150)
tree.column("phone", width=100)
tree.column("email", width=150)
tree.column("salary", width=80)
tree.heading("fio", text="ФИО")
tree.heading("phone", text="Телефон")
tree.heading("email", text="Email")
tree.heading("salary", text="Зарплата")
tree.pack(side=TOP, fill=BOTH, expand=True)

# Создаем базу данных и таблицу для хранения данных
connection = sqlite3.connect("db.db")
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fio TEXT,
                    phone TEXT,
                    email TEXT,
                    salary INTEGER
                )""")
connection.commit()

# Функция добавления сотрудника в базу данных и treeview
def add_employee():
    fio = fio_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()
    # Добавляем данные в базу данных
    cursor.execute("INSERT INTO employees (fio, phone, email, salary) VALUES (?, ?, ?, ?)",
                   (fio, phone, email, salary))
    connection.commit()
    # Получаем id новой записи
    new_id = cursor.lastrowid
    # Добавляем данные в treeview
    tree.insert("", END, values=(new_id, fio, phone, email, salary))

# Функция обновления сотрудника в базе данных и treeview
def update_employee():
    # Получаем выделенную строку
    selection = tree.selection()
    if len(selection) != 1:
        return
    # Получаем новые значения из полей ввода
    fio = fio_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()
    # Получаем id выделенной строки
    selected_id = tree.item(selection, "values")[0]
    # Обновляем данные в базе данных
    cursor.execute("UPDATE employees SET fio=?, phone=?, email=?, salary=? WHERE id=?",
                   (fio, phone, email, salary, selected_id))
    connection.commit()
    # Обновляем данные в treeview
    tree.item(selection, values=(selected_id, fio, phone, email, salary))

# Функция удаления сотрудника из базы данных и treeview
def delete_employee():
    # Получаем выделенную строку
    selection = tree.selection()
    if len(selection) != 1:
        return
    # Получаем id выделенной строки
    selected_id = tree.item(selection, "values")[0]
    # Удаляем данные из базы данных
    cursor.execute("DELETE FROM employees WHERE id=?", (selected_id,))
    connection.commit()
    # Удаляем данные из treeview
    tree.delete(selection)

# Функция поиска сотрудника по ФИО
def search_employee():
    keyword = search_entry.get()
    # Очищаем treeview
    tree.delete(*tree.get_children())
    # Ищем сотрудников в базе данных по ключевому слову
    cursor.execute("SELECT * FROM employees WHERE fio LIKE ?", (f"%{keyword}%",))
    for row in cursor.fetchall():
        # Вставляем данные в treeview
        tree.insert("", END, values=row)

# Создаем и настраиваем кнопки и поля ввода
frame = Frame(root)
frame.pack(side=TOP, padx=10, pady=10)

fio_label = Label(frame, text="ФИО")
fio_label.grid(row=0, column=0, sticky=E)
fio_entry = Entry(frame)
fio_entry.grid(row=0, column=1)

phone_label = Label(frame, text="Телефон")
phone_label.grid(row=1, column=0, sticky=E)

phone_entry = Entry(frame)
phone_entry.grid(row=1, column=1)

email_label = Label(frame, text="Email")
email_label.grid(row=2, column=0, sticky=E)
email_entry = Entry(frame)
email_entry.grid(row=2, column=1)

salary_label = Label(frame, text="Зарплата")
salary_label.grid(row=3, column=0, sticky=E)
salary_entry = Entry(frame)
salary_entry.grid(row=3, column=1)

add_button = Button(frame, text="Добавить", command=add_employee)
add_button.grid(row=4, column=0, sticky=W)

update_button = Button(frame, text="Обновить", command=update_employee)
update_button.grid(row=4, column=1)

delete_button = Button(frame, text="Удалить", command=delete_employee)
delete_button.grid(row=5, column=0, sticky=W)

search_label = Label(frame, text="Поиск")
search_label.grid(row=6, column=0, sticky=E)
search_entry = Entry(frame)
search_entry.grid(row=6, column=1)
search_button = Button(frame, text="Искать", command=search_employee)
search_button.grid(row=7, column=0, sticky=W)

# Заполняем treeview данными из базы данных
cursor.execute("SELECT * FROM employees")
for row in cursor.fetchall():
    tree.insert("", END, values=row)

# Запускаем главный цикл приложения
root.mainloop()
