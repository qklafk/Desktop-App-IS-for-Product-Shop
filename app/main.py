from datetime import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, Button, Toplevel, scrolledtext

products = {}

# Создание базы данных и таблицы
def create_database():
    conn = sqlite3.connect('products_and_users.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        имя TEXT UNIQUE,
                        пароль TEXT,
                        роль TEXT)''')

    cursor.execute("SELECT * FROM users WHERE имя = 'admin'")
    admin = cursor.fetchone()

    if not admin:
        cursor.execute("INSERT INTO users (имя, пароль, роль) VALUES (?, ?, ?)", ('admin', 'admin', 'Администратор'))

    cursor.execute("SELECT * FROM users WHERE имя = 'moderator'")
    moderator = cursor.fetchone()

    if not moderator:
        cursor.execute("INSERT INTO users (имя, пароль, роль) VALUES (?, ?, ?)", ('moderator', 'moderator', 'Модератор'))

    cursor.execute("SELECT * FROM users WHERE имя = 'user'")
    user = cursor.fetchone()

    if not user:
        cursor.execute("INSERT INTO users (имя, пароль, роль) VALUES (?, ?, ?)", ('user', 'user', 'Пользователь'))

    conn.commit()
    conn.close()
create_database()

# Регистрация пользователя
def register_user():
    register_window = tk.Toplevel()
    register_window.title("Регистрация пользователя")
    register_window.geometry("400x400")
    register_window.resizable(False, False)

    label_style = {"font": ("Helvetica", 12)}
    entry_style = {"font": ("Helvetica", 12)}
    button_style = {
        "bg": "#ffffff",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 20,
        "height": 2
    }

    tk.Label(register_window, text="Введите имя пользователя:", **label_style).pack(pady=10)
    username_entry = tk.Entry(register_window, **entry_style)
    username_entry.pack(pady=5)

    tk.Label(register_window, text="Введите пароль:", **label_style).pack(pady=10)
    password_entry = tk.Entry(register_window, show='*', **entry_style)
    password_entry.pack(pady=5)

    def toggle_password_visibility():
        if password_entry.cget("show") == "*":
            password_entry.config(show="")
        else:
            password_entry.config(show="*")

    tk.Checkbutton(register_window, text="Показать пароль", command=toggle_password_visibility).pack(pady=5)

    def confirm_registration():
        имя = username_entry.get()
        пароль = password_entry.get()
        роль = "Пользователь"

        if not имя or not пароль:
            messagebox.showerror("Ошибка", "Имя и пароль не могут быть пустыми.")
            return

        try:
            conn = sqlite3.connect('products_and_users.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (имя, пароль, роль) VALUES (?, ?, ?)', (имя, пароль, роль))
            conn.commit()
            messagebox.showinfo("Успех", f"Пользователь '{имя}' успешно зарегистрирован.")
            register_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует. Пожалуйста, выберите другое имя.")
        finally:
            conn.close()

    btn_register = tk.Button(register_window, text="Зарегистрироваться", command=confirm_registration, **button_style)
    btn_register.pack(pady=20)

    btn_cancel = tk.Button(register_window, text="Отмена", command=register_window.destroy, **button_style)
    btn_cancel.pack(pady=5)

# Вход пользователя
def login_user():
    login_window = tk.Toplevel()
    login_window.title("Вход в систему")
    login_window.geometry("300x300")
    login_window.resizable(False, False)

    label_style = {"font": ("Helvetica", 12)}
    entry_style = {"font": ("Helvetica", 12)}
    button_style = {
        "bg": "#ffffff",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 15,
        "height": 2
    }

    user_info = [None, None]

    def attempt_login():
        имя = entry_name.get()
        пароль = entry_password.get()

        if not имя or not пароль:
            messagebox.showerror("Ошибка", "Имя пользователя и пароль не могут быть пустыми.")
            return

        conn = sqlite3.connect('products_and_users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE имя = ? AND пароль = ?', (имя, пароль))
        user = cursor.fetchone()
        conn.close()

        if user:
            user_info[0] = имя
            user_info[1] = user[3]
            login_window.destroy()
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль.")

    def cancel_login():
        user_info[0] = None
        user_info[1] = None
        login_window.destroy()

    def toggle_password_visibility():
        if entry_password.cget("show") == "*":
            entry_password.config(show="")
        else:
            entry_password.config(show="*")

    tk.Label(login_window, text="Введите имя пользователя:", **label_style).pack(pady=5)
    entry_name = tk.Entry(login_window, **entry_style)
    entry_name.pack(pady=5)

    tk.Label(login_window, text="Введите пароль:", **label_style).pack(pady=5)
    entry_password = tk.Entry(login_window, show='*', **entry_style)
    entry_password.pack(pady=5)

    tk.Checkbutton(login_window, text="Показать пароль", command=toggle_password_visibility).pack(pady=5)

    btn_login = tk.Button(login_window, text="Войти", command=attempt_login, **button_style)
    btn_login.pack(pady=10)

    btn_cancel = tk.Button(login_window, text="Отмена", command=cancel_login, **button_style)
    btn_cancel.pack(pady=5)

    login_window.wait_window()
    return user_info[0], user_info[1]

#Управление пользователями
# Функция добавления пользователя
def add_user():
    add_user_window = Toplevel()
    add_user_window.title("Добавить пользователя")
    add_user_window.geometry("300x400")
    add_user_window.resizable(False, False)

    label_style = {"font": ("Helvetica", 12)}
    entry_style = {"font": ("Helvetica", 12)}
    button_style = {
        "bg": "#ffffff",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 15,
        "height": 2
    }

    def attempt_add_user():
        имя = entry_name.get()
        пароль = entry_password.get()

        if not имя or not пароль:
            messagebox.showerror("Ошибка", "Имя и пароль не могут быть пустыми.")
            return

        роль_choice = role_var.get()

        роль_map = {'1': 'Администратор', '2': 'Модератор', '3': 'Пользователь'}
        роль = роль_map.get(роль_choice)

        if роль is None:
            messagebox.showerror("Ошибка", "Неверный выбор роли.")
            return

        try:
            conn = sqlite3.connect('products_and_users.db')
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM users WHERE имя = ?', (имя,))
            existing_user = cursor.fetchone()

            if existing_user:
                messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует. Пожалуйста, выберите другое имя.")
                return

            cursor.execute('INSERT INTO users (имя, пароль, роль) VALUES (?, ?, ?)', (имя, пароль, роль))
            conn.commit()
            messagebox.showinfo("Успех", f"Пользователь '{имя}' успешно добавлен с ролью '{роль}'.")

        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Произошла ошибка: {e}")

        finally:
            conn.close()
            add_user_window.destroy()

    def toggle_password_visibility():
        if entry_password.cget("show") == "*":
            entry_password.config(show="")
        else:
            entry_password.config(show="*")

    tk.Label(add_user_window, text="Введите имя пользователя:", **label_style).pack(pady=5)
    entry_name = tk.Entry(add_user_window, **entry_style)
    entry_name.pack(pady=5)

    tk.Label(add_user_window, text="Введите пароль:", **label_style).pack(pady=5)
    entry_password = tk.Entry(add_user_window, show='*', **entry_style)
    entry_password.pack(pady=5)

    show_password_var = tk.BooleanVar()
    tk.Checkbutton(add_user_window, text="Показать пароль", variable=show_password_var, command=toggle_password_visibility).pack(pady=5)

    tk.Label(add_user_window, text="Выберите роль:", **label_style).pack(pady=5)

    role_var = tk.StringVar(value='1')

    frame_roles = tk.Frame(add_user_window)
    frame_roles.pack(pady=5)

    tk.Radiobutton(frame_roles, text="Администратор", variable=role_var, value='1').pack(anchor=tk.CENTER)
    tk.Radiobutton(frame_roles, text="Модератор", variable=role_var, value='2').pack(anchor=tk.CENTER)
    tk.Radiobutton(frame_roles, text="Пользователь", variable=role_var, value='3').pack(anchor=tk.CENTER)

    btn_add = tk.Button(add_user_window, text="Добавить", command=attempt_add_user, **button_style)
    btn_add.pack(pady=10)

    btn_cancel = tk.Button(add_user_window, text="Отмена", command=add_user_window.destroy, **button_style)
    btn_cancel.pack(pady=5)

# Функция удаления пользователя
def delete_user():
    delete_window = tk.Toplevel()
    delete_window.title("Удаление пользователя")
    delete_window.geometry("300x150")
    delete_window.resizable(False, False)

    label_style = {"font": ("Helvetica", 12)}
    entry_style = {"font": ("Helvetica", 12)}
    button_style = {
        "bg": "#ffffff",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 15,
        "height": 2
    }

    def confirm_delete():
        имя = entry_name.get()
        if not имя:
            messagebox.showerror("Ошибка", "Имя не может быть пустым.")
            return

        try:
            conn = sqlite3.connect('products_and_users.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE имя = ?', (имя,))
            if cursor.rowcount == 0:
                messagebox.showerror("Ошибка", f"Пользователь '{имя}' не найден.")
            else:
                messagebox.showinfo("Успех", f"Пользователь '{имя}' успешно удален.")
            conn.commit()
        finally:
            conn.close()
            delete_window.destroy()

    def cancel_delete():
        delete_window.destroy()

    tk.Label(delete_window, text="Введите имя пользователя:", **label_style).pack(pady=10)
    entry_name = tk.Entry(delete_window, **entry_style)
    entry_name.pack(pady=5)

    btn_confirm = tk.Button(delete_window, text="Удалить", command=confirm_delete, **button_style)
    btn_confirm.pack(pady=10)

    btn_cancel = tk.Button(delete_window, text="Отмена", command=cancel_delete, **button_style)
    btn_cancel.pack(pady=5)

    delete_window.mainloop()

# Функция обновления пользователя
def update_user():
    update_user_window = tk.Toplevel()
    update_user_window.title("Обновить пользователя")
    update_user_window.geometry("400x450")
    update_user_window.resizable(False, False)

    label_style = {"font": ("Helvetica", 12)}
    entry_style = {"font": ("Helvetica", 12)}
    button_style = {
        "bg": "#ffffff",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 20,
        "height": 2
    }

    tk.Label(update_user_window, text="Введите имя пользователя:", **label_style).pack(pady=10)
    entry_name = tk.Entry(update_user_window, **entry_style)
    entry_name.pack(pady=5)

    def confirm_update():
        имя = entry_name.get()
        
        if not имя:
            messagebox.showerror("Ошибка", "Имя не может быть пустым.")
            return

        try:
            conn = sqlite3.connect('products_and_users.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE имя = ?', (имя,))
            user = cursor.fetchone()
            
            if user is None:
                messagebox.showerror("Ошибка", f"Пользователь '{имя}' не найден.")
                return

            новый_пароль = entry_password.get()
            новый_роль_choice = role_var.get()

            новый_роль_map = {'1': 'Администратор', '2': 'Модератор', '3': 'Пользователь'}
            новый_роль = новый_роль_map.get(новый_роль_choice)

            if новый_пароль:
                cursor.execute('UPDATE users SET пароль = ? WHERE имя = ?', (новый_пароль, имя))
            if новый_роль:
                cursor.execute('UPDATE users SET роль = ? WHERE имя = ?', (новый_роль, имя))

            conn.commit()
            messagebox.showinfo("Успех", f"Пользователь '{имя}' успешно обновлен.")
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Произошла ошибка: {e}")
        finally:
            conn.close()
            update_user_window.destroy()

    tk.Label(update_user_window, text="Введите новый пароль\n(или оставьте пустым для пропуска):", **label_style).pack(pady=10)
    entry_password = tk.Entry(update_user_window, show='*', **entry_style)
    entry_password.pack(pady=5)

    tk.Label(update_user_window, text="Выберите новую роль\n(или оставьте пустым для пропуска):", **label_style).pack(pady=10)

    role_var = tk.StringVar(value='1')
    frame_roles = tk.Frame(update_user_window)
    frame_roles.pack(pady=5)
    tk.Radiobutton(update_user_window, text="Администратор", variable=role_var, value='1').pack(anchor=tk.CENTER)
    tk.Radiobutton(update_user_window, text="Модератор", variable=role_var, value='2').pack(anchor=tk.CENTER)
    tk.Radiobutton(update_user_window, text="Пользователь", variable=role_var, value='3').pack(anchor=tk.CENTER)

    btn_update = tk.Button(update_user_window, text="Обновить", command=confirm_update, **button_style)
    btn_update.pack(pady=10)

    btn_cancel = tk.Button(update_user_window, text="Отмена", command=update_user_window.destroy, **button_style)
    btn_cancel.pack(pady=5)

# Список всех пользователей
def list_all_users():
    user_list_window = tk.Toplevel()
    user_list_window.title("Список всех пользователей")
    user_list_window.geometry("500x400")
    user_list_window.resizable(False, False)

    label_style = {"font": ("Helvetica", 14)}
    button_style = {
        "bg": "#ffffff",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 15,
        "height": 2
    }

    tk.Label(user_list_window, text="Список всех пользователей:", **label_style).pack(pady=10)

    text_area = scrolledtext.ScrolledText(user_list_window, width=50, height=15, font=("Helvetica", 12))
    text_area.pack(pady=10)
    text_area.config(state=tk.NORMAL)

    try:
        conn = sqlite3.connect('products_and_users.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()

        if users:
            user_list = "\n".join([f"Имя: {u[1]}, Роль: {u[3]}" for u in users])
            text_area.insert(tk.END, user_list)
        else:
            text_area.insert(tk.END, "Нет доступных пользователей.")
    except sqlite3.Error as e:
        messagebox.showerror("Ошибка базы данных", f"Произошла ошибка при получении пользователей: {e}")
    finally:
        if conn:
            conn.close()
    
    btn_close = tk.Button(user_list_window, text="Закрыть", command=user_list_window.destroy, **button_style)
    btn_close.pack(pady=10)

    text_area.config(state=tk.DISABLED)

# Показать данные пользователя
def show_user_details():
    show_details_window = tk.Toplevel()
    show_details_window.title("Подробная информация о пользователе")
    show_details_window.geometry("350x250")
    show_details_window.resizable(False, False)

    label_style = {"font": ("Helvetica", 12)}
    button_style = {
        "bg": "#ffffff",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 20,
        "height": 2
    }

    tk.Label(show_details_window, text="Введите имя пользователя:", **label_style).pack(pady=10)
    entry_name = tk.Entry(show_details_window, **label_style)
    entry_name.pack(pady=5)

    def confirm_show_details():
        имя = entry_name.get()
        
        if not имя:
            messagebox.showerror("Ошибка", "Имя не может быть пустым.")
            return

        try:
            conn = sqlite3.connect('products_and_users.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE имя = ?', (имя,))
            user_details = cursor.fetchone()

            if user_details:
                details_window = Toplevel()
                details_window.title("Подробная информация о пользователе")
                details_window.geometry("300x200")
                details_window.resizable(False, False)

                tk.Label(details_window, text=f"Имя: {user_details[1]}", **label_style).pack(pady=10)
                tk.Label(details_window, text=f"Роль: {user_details[3]}", **label_style).pack(pady=10)

                close_button = tk.Button(details_window, text="Закрыть", command=details_window.destroy, **button_style)
                close_button.pack(pady=20)

            else:
                messagebox.showerror("Ошибка", f"Пользователь '{имя}' не найден.")
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Произошла ошибка: {e}")
        finally:
            conn.close()
            show_details_window.destroy()

    btn_show = tk.Button(show_details_window, text="Показать детали", command=confirm_show_details, **button_style)
    btn_show.pack(pady=10)

    btn_cancel = tk.Button(show_details_window, text="Отмена", command=show_details_window.destroy, **button_style)
    btn_cancel.pack(pady=5)

# Изменить роль пользователя
def assign_role():
    assign_role_window = tk.Toplevel()
    assign_role_window.title("Назначить роль")
    assign_role_window.geometry("350x350")
    assign_role_window.resizable(False, False)

    label_style = {"font": ("Helvetica", 12)}
    button_style = {
        "bg": "#ffffff",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 20,
        "height": 2
    }

    tk.Label(assign_role_window, text="Введите имя пользователя:", **label_style).pack(pady=10)
    entry_name = tk.Entry(assign_role_window, **label_style)
    entry_name.pack(pady=5)

    tk.Label(assign_role_window, text="Выберите новую роль:", **label_style).pack(pady=10)

    role_var = tk.StringVar(value='1')
    frame_roles = tk.Frame(assign_role_window)
    frame_roles.pack(pady=5)
    tk.Radiobutton(assign_role_window, text="Администратор", variable=role_var, value='1').pack(anchor=tk.CENTER)
    tk.Radiobutton(assign_role_window, text="Модератор", variable=role_var, value='2').pack(anchor=tk.CENTER)
    tk.Radiobutton(assign_role_window, text="Пользователь", variable=role_var, value='3').pack(anchor=tk.CENTER)

    def confirm_assign_role():
        имя = entry_name.get()
        новый_роль_choice = role_var.get()

        роль_map = {'1': 'Администратор', '2': 'Модератор', '3': 'Пользователь'}
        новый_роль = роль_map.get(новый_роль_choice)

        if not имя:
            messagebox.showerror("Ошибка", "Имя не может быть пустым.")
            return

        try:
            conn = sqlite3.connect('products_and_users.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET роль = ? WHERE имя = ?', (новый_роль, имя))
            if cursor.rowcount == 0:
                messagebox.showerror("Ошибка", f"Пользователь '{имя}' не найден.")
            else:
                messagebox.showinfo("Успех", f"Роль пользователя '{имя}' изменена на '{новый_роль}'.")
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка базы данных", f"Произошла ошибка: {e}")
        finally:
            conn.close()
            assign_role_window.destroy()

    btn_assign = tk.Button(assign_role_window, text="Назначить", command=confirm_assign_role, **button_style)
    btn_assign.pack(pady=10)

    btn_cancel = tk.Button(assign_role_window, text="Отмена", command=assign_role_window.destroy, **button_style)
    btn_cancel.pack(pady=5)

# Управление продуктами
# Добавление продукта
def add_product():
    add_product_window = tk.Toplevel()
    add_product_window.title("Добавить продукт")
    add_product_window.geometry("400x550")
    add_product_window.resizable(False, False)

    label_style = {"font": ("Helvetica", 12)}
    entry_style = {"font": ("Helvetica", 12)}
    button_style = {
        "bg": "#ffffff",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 20,
        "height": 2
    }

    tk.Label(add_product_window, text="Введите наименование товара:", **label_style).pack(pady=10)
    entry_name = tk.Entry(add_product_window, **entry_style)
    entry_name.pack(pady=5)

    tk.Label(add_product_window, text="Введите категорию товара:", **label_style).pack(pady=10)
    entry_category = tk.Entry(add_product_window, **entry_style)
    entry_category.pack(pady=5)

    tk.Label(add_product_window, text="Введите описание товара:", **label_style).pack(pady=10)
    entry_description = tk.Entry(add_product_window, **entry_style)
    entry_description.pack(pady=5)

    tk.Label(add_product_window, text="Введите цену товара:", **label_style).pack(pady=10)
    entry_price = tk.Entry(add_product_window, **entry_style)
    entry_price.pack(pady=5)

    tk.Label(add_product_window, text="Введите срок годности товара\n(дд-мм-гггг):", **label_style).pack(pady=10)
    entry_expiration = tk.Entry(add_product_window, **entry_style)
    entry_expiration.pack(pady=5)

    def confirm_add_product():
        наименование = entry_name.get()
        категория = entry_category.get()
        описание = entry_description.get()
        цена_str = entry_price.get()
        срок_годности = entry_expiration.get()

        if not наименование:
            messagebox.showerror("Ошибка", "Наименование не может быть пустым.")
            return
        if наименование in products:
            messagebox.showerror("Ошибка", f"Товар с наименованием '{наименование}' уже существует.")
            return

        if not категория:
            messagebox.showerror("Ошибка", "Категория не может быть пустой.")
            return

        try:
            цена = float(цена_str)
            if цена <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Цена должна быть положительным числом.")
            return

        try:
            срок_годности = datetime.strptime(срок_годности, '%d-%m-%Y').strftime('%d-%m-%Y')
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте формат 'дд-мм-гггг'.")
            return

        products[наименование] = {
            'категория': категория,
            'описание': описание,
            'цена': цена,
            'срок_годности': срок_годности
        }

        messagebox.showinfo("Успех", f"Товар '{наименование}' успешно добавлен.")
        add_product_window.destroy()

    btn_add = tk.Button(add_product_window, text="Добавить", command=confirm_add_product, **button_style)
    btn_add.pack(pady=10)

    btn_cancel = tk.Button(add_product_window, text="Отмена", command=add_product_window.destroy, **button_style)
    btn_cancel.pack(pady=5)

#Удаление продукта
def delete_product():
    delete_product_window = tk.Toplevel()
    delete_product_window.title("Удалить продукт")
    delete_product_window.geometry("400x250")
    delete_product_window.resizable(False, False)

    label_style = {"font": ("Helvetica", 12)}
    entry_style = {"font": ("Helvetica", 12)}
    button_style = {
        "bg": "#ffffff",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 20,
        "height": 2
    }

    tk.Label(delete_product_window, text="Введите наименование товара для удаления:", **label_style).pack(pady=10)
    entry_name = tk.Entry(delete_product_window, **entry_style)
    entry_name.pack(pady=5)

    def confirm_delete():
        наименование = entry_name.get()
        if not наименование:
            messagebox.showerror("Ошибка", "Наименование не может быть пустым.")
            return

        if наименование in products:
            del products[наименование]
            messagebox.showinfo("Успех", f"Товар '{наименование}' удален.")
            delete_product_window.destroy()
        else:
            messagebox.showerror("Ошибка", f"Товар '{наименование}' не найден.")

    btn_delete = tk.Button(delete_product_window, text="Удалить", command=confirm_delete, **button_style)
    btn_delete.pack(pady=10)

    btn_cancel = tk.Button(delete_product_window, text="Отмена", command=delete_product_window.destroy, **button_style)
    btn_cancel.pack(pady=5)

#Обновление продукта
def update_product():
    update_product_window = tk.Toplevel()
    update_product_window.title("Обновить продукт")
    update_product_window.geometry("400x600")
    update_product_window.resizable(False, False)

    label_style = {"font": ("Helvetica", 12)}
    entry_style = {"font": ("Helvetica", 12)}
    button_style = {
        "bg": "#ffffff",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 20,
        "height": 2
    }

    tk.Label(update_product_window, text="Введите наименование товара для обновления:", **label_style).pack(pady=10)
    entry_name = tk.Entry(update_product_window, **entry_style)
    entry_name.pack(pady=5)

    tk.Label(update_product_window, text="Новая категория\n(или оставьте пустым):", **label_style).pack(pady=10)
    entry_category = tk.Entry(update_product_window, **entry_style)
    entry_category.pack(pady=5)

    tk.Label(update_product_window, text="Новое описание\n(или оставьте пустым):", **label_style).pack(pady=10)
    entry_description = tk.Entry(update_product_window, **entry_style)
    entry_description.pack(pady=5)

    tk.Label(update_product_window, text="Новая цена\n(или оставьте пустым):", **label_style).pack(pady=10)
    entry_price = tk.Entry(update_product_window, **entry_style)
    entry_price.pack(pady=5)

    tk.Label(update_product_window, text="Новый срок годности (дд-мм-гггг)\n(или оставьте пустым):", **label_style).pack(pady=10)
    entry_expiry = tk.Entry(update_product_window, **entry_style)
    entry_expiry.pack(pady=5)

    def confirm_update():
        наименование = entry_name.get()

        if not наименование:
            messagebox.showerror("Ошибка", "Наименование не может быть пустым.")
            return

        if наименование in products:
            категория = entry_category.get()
            if категория:
                products[наименование]['категория'] = категория

            описание = entry_description.get()
            if описание:
                products[наименование]['описание'] = описание

            цена_str = entry_price.get()
            if цена_str:
                try:
                    цена = float(цена_str)
                    if цена <= 0:
                        raise ValueError
                    products[наименование]['цена'] = цена
                except ValueError:
                    messagebox.showerror("Ошибка", "Цена должна быть положительным числом.")
                    return

            срок_годности = entry_expiry.get()
            if срок_годности:
                try:
                    срок_годности = datetime.strptime(срок_годности, '%d-%m-%Y').strftime('%d-%m-%Y')
                    products[наименование]['срок_годности'] = срок_годности
                except ValueError:
                    messagebox.showerror("Ошибка", "Неверный формат даты. Используйте формат 'дд-мм-гггг'.")

            messagebox.showinfo("Успех", f"Товар '{наименование}' успешно обновлён.")
            update_product_window.destroy()
        else:
            messagebox.showerror("Ошибка", f"Товар '{наименование}' не найден.")

    btn_update = tk.Button(update_product_window, text="Обновить", command=confirm_update, **button_style)
    btn_update.pack(pady=10)

    btn_cancel = tk.Button(update_product_window, text="Отмена", command=update_product_window.destroy, **button_style)
    btn_cancel.pack(pady=5)

#Сортировка продуктов по категории
def get_products_by_category():
    category_window = tk.Toplevel()
    category_window.title("Выбор категории")
    category_window.geometry("400x200")
    category_window.resizable(False, False)

    label_style = {"font": ("Helvetica", 12)}
    entry_style = {"font": ("Helvetica", 12)}
    button_style = {
        "bg": "#ffffff",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 20,
        "height": 2
    }

    tk.Label(category_window, text="Введите категорию для фильтрации продуктов:", **label_style).pack(pady=10)
    entry_category = tk.Entry(category_window, **entry_style)
    entry_category.pack(pady=5)

    def filter_products():
        category = entry_category.get()

        if not category:
            messagebox.showerror("Ошибка", "Категория не может быть пустой.")
            return

        filtered_products = {name: details for name, details in products.items() if details['категория'] == category}

        if not filtered_products:
            messagebox.showinfo("Результаты", f"Нет продуктов в категории '{category}'.")
            return

        results_window = tk.Toplevel()
        results_window.title(f"Продукты в категории '{category}'")
        results_window.geometry("400x300")
        results_window.resizable(False, False)

        text_area = tk.Text(results_window, wrap=tk.WORD)
        text_area.pack(expand=True, fill=tk.BOTH)

        for product_name, product_details in filtered_products.items():
            product_info = (
                f"Наименование: {product_name}, "
                f"Категория: {product_details['категория']}, "
                f"Цена: {product_details['цена']} руб., "
                f"Срок годности: {product_details['срок_годности']}\n"
            )
            text_area.insert(tk.END, product_info)

        text_area.config(state=tk.DISABLED)

    btn_filter = tk.Button(category_window, text="Фильтровать", command=filter_products, **button_style)
    btn_filter.pack(pady=10)

    btn_cancel = tk.Button(category_window, text="Отмена", command=category_window.destroy, **button_style)
    btn_cancel.pack(pady=5)

# Поиск продуктов
def search_products():
    search_window = tk.Toplevel()
    search_window.title("Поиск товара")
    search_window.geometry("350x350")
    search_window.resizable(False, False)

    label_style = {"font": ("Helvetica", 12)}
    entry_style = {"font": ("Helvetica", 12)}
    button_style = {
        "bg": "#ffffff",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 20,
        "height": 2
    }

    tk.Label(search_window, text="Введите категорию\n(или оставьте пустым):", **label_style).pack(pady=10)
    entry_category = tk.Entry(search_window, **entry_style)
    entry_category.pack(pady=5)

    tk.Label(search_window, text="Введите наименование товара\n(или оставьте пустым):", **label_style).pack(pady=10)
    entry_name = tk.Entry(search_window, **entry_style)
    entry_name.pack(pady=5)

    def perform_search():
        категория = entry_category.get()
        наименование = entry_name.get()

        found = []
        for product_name, детали in products.items():
            if (категория and наименование and детали['категория'] == категория and product_name == наименование) or \
               (категория and детали['категория'] == категория) or \
               (наименование and product_name == наименование):
                found.append(f"{product_name}: {детали}")

        if found:
            results_window = tk.Toplevel()
            results_window.title("Результаты поиска")
            results_window.geometry("400x300")
            results_window.resizable(False, False)

            text_area = tk.Text(results_window, wrap=tk.WORD)
            text_area.pack(expand=True, fill=tk.BOTH)

            for item in found:
                text_area.insert(tk.END, item + "\n")

            text_area.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Поиск", "Товар не найден.")

    btn_search = tk.Button(search_window, text="Поиск", command=perform_search, **button_style)
    btn_search.pack(pady=10)

    btn_cancel = tk.Button(search_window, text="Отмена", command=search_window.destroy, **button_style)
    btn_cancel.pack(pady=5)

#Сортировка продуктов по цене
def sort_products_by_price():
    sorted_products = sorted(products.items(), key=lambda x: x[1]['цена'])

    if not sorted_products:
        messagebox.showinfo("Сортировка по цене", "Нет доступных товаров.")
        return

    sorted_window = tk.Toplevel()
    sorted_window.title("Сортировка товаров по цене")
    sorted_window.geometry("400x300")
    sorted_window.resizable(False, False)

    text_area = tk.Text(sorted_window, wrap=tk.WORD)
    text_area.pack(expand=True, fill=tk.BOTH)

    product_list = "\n".join([
        f"Наименование: {наименование}, Цена: {детали['цена']} руб., "
        f"Категория: {детали['категория']}, "
        f"Срок годности: {детали['срок_годности']}" 
        for наименование, детали in sorted_products
    ])

    text_area.insert(tk.END, product_list)
    text_area.config(state=tk.DISABLED)

    btn_close = tk.Button(sorted_window, text="Закрыть", command=sorted_window.destroy, 
                          bg="#ffffff", fg="black", font=("Helvetica", 12), relief=tk.RAISED, 
                          width=20, height=2)
    btn_close.pack(pady=10)

# Список всех продуктов
def list_all_products():
    if products:
        list_window = tk.Toplevel()
        list_window.title("Список всех товаров")
        list_window.geometry("400x300")
        list_window.resizable(False, False)

        product_list = "\n".join([
            f"Наименование: {название}, Категория: {детали['категория']}, "
            f"Цена: {детали['цена']} руб., Срок годности: {детали['срок_годности']}"
            for название, детали in products.items()
        ])

        text_area = tk.Text(list_window, wrap=tk.WORD)
        text_area.pack(expand=True, fill=tk.BOTH)
        
        text_area.insert(tk.END, product_list)
        text_area.config(state=tk.DISABLED)

        btn_close = tk.Button(list_window, text="Закрыть", command=list_window.destroy, 
                              bg="#ffffff", fg="black", font=("Helvetica", 12), relief=tk.RAISED, 
                              width=20, height=2)
        btn_close.pack(pady=10)

    else:
        messagebox.showinfo("Список товаров", "Нет доступных товаров.")
        
# Показать информацию о продуктах
def show_product_details():
    product_window = tk.Toplevel()
    product_window.title("Показать детали продукта")
    product_window.geometry("400x200")
    product_window.resizable(False, False)

    label_style = {"font": ("Helvetica", 12)}
    entry_style = {"font": ("Helvetica", 12)}
    button_style = {
        "bg": "#ffffff",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 20,
        "height": 2
    }

    tk.Label(product_window, text="Введите наименование продукта:", **label_style).pack(pady=10)
    entry_product_name = tk.Entry(product_window, **entry_style)
    entry_product_name.pack(pady=5)

    def display_product_details():
        наименование = entry_product_name.get()

        if not наименование:
            messagebox.showerror("Ошибка", "Наименование не может быть пустым.")
            return

        if наименование not in products:
            messagebox.showerror("Ошибка", f"Продукт '{наименование}' не найден.")
            return

        продукт = products[наименование]

        details_window = tk.Toplevel()
        details_window.title("Детали продукта")
        details_window.geometry("350x200")
        details_window.resizable(False, False)
        details_window.configure(bg="#f0f0f0")

        label_style = {"font": ("Helvetica", 12), "bg": "#f0f0f0"}
        button_style = {
            "bg": "#ffffff",
            "fg": "black",
            "font": ("Helvetica", 12),
            "relief": tk.RAISED,
            "width": 20,
            "height": 2
        }

        tk.Label(details_window, text=f"Наименование: {наименование}", **label_style).pack(pady=10)
        tk.Label(details_window, text=f"Категория: {продукт['категория']}", **label_style).pack(pady=5)
        tk.Label(details_window, text=f"Описание: {продукт['описание']}", **label_style).pack(pady=5)
        tk.Label(details_window, text=f"Цена: {продукт['цена']} руб.", **label_style).pack(pady=5)
        tk.Label(details_window, text=f"Срок годности: {продукт['срок_годности']}", **label_style).pack(pady=5)

        btn_close = tk.Button(details_window, text="Закрыть", command=details_window.destroy, **button_style)
        btn_close.pack(pady=20)

        tk.Frame(details_window, height=2, bg="#007BFF").pack(fill=tk.X, padx=5, pady=10)

    btn_show_details = tk.Button(product_window, text="Показать детали", command=display_product_details, **button_style)
    btn_show_details.pack(pady=10)

    btn_cancel = tk.Button(product_window, text="Отмена", command=product_window.destroy, **button_style)
    btn_cancel.pack(pady=5)

current_user = None
root = None

# Страницы
# Главная страница
def entry_page():
    global root
    root = tk.Tk()
    root.title("Главная страница")
    root.geometry("300x250")

    def on_login():
        user_name, user_role = login_user()
        if user_name:
            messagebox.showinfo("Успех", f"Добро пожаловать, {user_name}! Ваша роль: {user_role}.")
            root.withdraw()

            if user_role == 'Администратор':
                admin_menu()
            elif user_role == 'Модератор':
                moderator_menu()
            else:
                user_menu()

    def on_register():
        register_user()

    def on_exit():
        root.quit()

    button_style = {
        "bg": "#FFFFFF",
        "fg": "black", 
        "font": ("Helvetica", 14),
        "relief": tk.RAISED, 
        "width": 20,
        "height": 2
    }

    btn_login = tk.Button(root, text="Войти в систему", command=on_login, **button_style)
    btn_login.pack(pady=10)

    btn_register = tk.Button(root, text="Зарегистрироваться", command=on_register, **button_style)
    btn_register.pack(pady=10)

    btn_exit = tk.Button(root, text="Выйти", command=on_exit, **button_style)
    btn_exit.pack(pady=10)

    root.mainloop()

# Страница администратора
def admin_menu():
    admin_window = tk.Toplevel()
    admin_window.title("Меню администратора")
    admin_window.geometry("450x500")
    admin_window.configure(bg="#f0f0f0")

    def on_choice(choice):
        try:
            if choice == '1':
                list_all_users()
            elif choice == '2':
                show_user_details()
            elif choice == '3':
                add_user()
            elif choice == '4':
                delete_user()
            elif choice == '5':
                update_user()
            elif choice == '6':
                assign_role()
            elif choice == '7':
                admin_window.destroy()
                root.deiconify()
            else:
                messagebox.showerror("Ошибка", "Неверный выбор. Пожалуйста, попробуйте снова.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    button_style = {
        "bg": "#FFFFFF",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 40,
        "height": 2
    }

    btn_list_users = tk.Button(admin_window, text="Список всех пользователей", command=lambda: on_choice('1'), **button_style)
    btn_list_users.pack(pady=10)

    btn_user_details = tk.Button(admin_window, text="Подробная информация о пользователе", command=lambda: on_choice('2'), **button_style)
    btn_user_details.pack(pady=10)

    btn_add_user = tk.Button(admin_window, text="Добавить пользователя", command=lambda: on_choice('3'), **button_style)
    btn_add_user.pack(pady=10)

    btn_delete_user = tk.Button(admin_window, text="Удалить пользователя", command=lambda: on_choice('4'), **button_style)
    btn_delete_user.pack(pady=10)

    btn_update_user = tk.Button(admin_window, text="Обновить данные пользователя", command=lambda: on_choice('5'), **button_style)
    btn_update_user.pack(pady=10)

    btn_assign_role = tk.Button(admin_window, text="Переназначить роль пользователю", command=lambda: on_choice('6'), **button_style)
    btn_assign_role.pack(pady=10)

    btn_return = tk.Button(admin_window, text="Вернуться в главное меню", command=lambda: on_choice('7'), **button_style)
    btn_return.pack(pady=10)

# Страница модератора
def moderator_menu():
    moderator_window = tk.Toplevel()
    moderator_window.title("Меню модератора")
    moderator_window.geometry("400x600")
    moderator_window.configure(bg="#f0f0f0")

    def on_choice(choice):
        if choice == '1':
            add_product()
        elif choice == '2':
            delete_product()
        elif choice == '3':
            update_product()
        elif choice == '4':
            list_all_products()
        elif choice == '5':
            show_product_details()
        elif choice == '6':
            search_products()
        elif choice == '7':
            get_products_by_category()
        elif choice == '8':
            moderator_window.destroy()
            entry_page()
        else:
            messagebox.showerror("Ошибка", "Неверный выбор. Пожалуйста, попробуйте снова.")

    button_style = {
        "bg": "#FFFFFF",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 35,
        "height": 2
    }

    btn_add_product = tk.Button(moderator_window, text="Добавить новый товар", command=lambda: on_choice('1'), **button_style)
    btn_add_product.pack(pady=10)

    btn_delete_product = tk.Button(moderator_window, text="Удалить товар", command=lambda: on_choice('2'), **button_style)
    btn_delete_product.pack(pady=10)

    btn_update_product = tk.Button(moderator_window, text="Обновить товар", command=lambda: on_choice('3'), **button_style)
    btn_update_product.pack(pady=10)

    btn_list_products = tk.Button(moderator_window, text="Список всех товаров", command=lambda: on_choice('4'), **button_style)
    btn_list_products.pack(pady=10)

    btn_product_details = tk.Button(moderator_window, text="Подробное описание товаров", command=lambda: on_choice('5'), **button_style)
    btn_product_details.pack(pady=10)

    btn_search_products = tk.Button(moderator_window, text="Поиск товаров", command=lambda: on_choice('6'), **button_style)
    btn_search_products.pack(pady=10)

    btn_sort_categories = tk.Button(moderator_window, text="Фильтрация по категориям", command=lambda: on_choice('7'), **button_style)
    btn_sort_categories.pack(pady=10)

    btn_return = tk.Button(moderator_window, text="Вернуться в главное меню", command=lambda: on_choice('8'), **button_style)
    btn_return.pack(pady=10)

# Страница пользователя
def user_menu():
    user_window = tk.Toplevel()
    user_window.title("Меню пользователя")
    user_window.geometry("400x400")
    user_window.configure(bg="#f0f0f0")

    def on_choice(choice):
        if choice == '1':
            list_all_products()
        elif choice == '2':
            show_product_details()
        elif choice == '3':
            search_products()
        elif choice == '4':
            sort_products_by_price()
        elif choice == '5':
            user_window.destroy()
            entry_page()
        else:
            messagebox.showerror("Ошибка", "Неверный выбор. Пожалуйста, попробуйте снова.")

    button_style = {
        "bg": "#FFFFFF",
        "fg": "black",
        "font": ("Helvetica", 12),
        "relief": tk.RAISED,
        "width": 35,
        "height": 2
    }

    btn_view_products = tk.Button(user_window, text="Посмотреть все продукты", command=lambda: on_choice('1'), **button_style)
    btn_view_products.pack(pady=10)

    btn_show_details = tk.Button(user_window, text="Показать детали продукта", command=lambda: on_choice('2'), **button_style)
    btn_show_details.pack(pady=10)

    btn_search_products = tk.Button(user_window, text="Поиск продуктов", command=lambda: on_choice('3'), **button_style)
    btn_search_products.pack(pady=10)

    btn_sort_price = tk.Button(user_window, text="Сортировка по возрастанию цены", command=lambda: on_choice('4'), **button_style)
    btn_sort_price.pack(pady=10)

    btn_return = tk.Button(user_window, text="Вернуться в главное меню", command=lambda: on_choice('5'), **button_style)
    btn_return.pack(pady=10)

entry_page()