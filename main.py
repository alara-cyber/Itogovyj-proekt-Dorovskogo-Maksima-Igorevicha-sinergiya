from tkinter import *
from tkinter import ttk

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


# Функция добавления сотрудника в treeview
def add_employee():
    fio = fio_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()
    tree.insert("", END, values=(fio, phone, email, salary))


# Функция изменения сотрудника в treeview
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
    # Изменяем значения выделенной строки
    tree.item(selection, values=(fio, phone, email, salary))


# Функция удаления сотрудника из treeview
def delete_employee():
    # Получаем выделенную строку
    selection = tree.selection()
    if len(selection) != 1:
        return
    # Удаляем выделенную строку
    tree.delete(selection)


# Функция поиска сотрудника по ФИО
def search_employee():
    keyword = search_entry.get()
    # Очищаем treeview
    tree.delete(*tree.get_children())


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
add_button.grid(row=4, column=0)

update_button = Button(frame, text="Изменить", command=update_employee)
update_button.grid(row=4, column=1)

delete_button = Button(frame, text="Удалить", command=delete_employee)
delete_button.grid(row=5, column=0)

search_label = Label(frame, text="Поиск по ФИО")
search_label.grid(row=6, column=0, sticky=E)
search_entry = Entry(frame)
search_entry.grid(row=6, column=1)

root.mainloop()