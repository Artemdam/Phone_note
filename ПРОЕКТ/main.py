import tkinter as tk
from tkinter import ttk
import sqlite3

# Создаем класс главного окна 
class Main(tk.Frame):
    def __init__(self, root): 
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

############################################################################
    # Создание и работа с главным окном     
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)  
        toolbar.pack(side=tk.TOP, fill=tk.X)                         
############################################################################ КНОПКИ

        # ДОБАВИТЬ
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_add = tk.Button(toolbar, bg='#d7d7d7', bd=1,
                            image=self.add_img, command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # ОБНОВИТЬ
        self.upd_img = tk.PhotoImage(file='./img/update.png')
        btn_upd = tk.Button(toolbar, bg='#d7d7d7', bd=1,
                            image=self.upd_img, command=self.open_update_dialog)
        btn_upd.pack(side=tk.LEFT)

        # УДАЛИТЬ
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                               image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # ПОИСК
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        # ОБНОВИТЬ
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0, 
                                image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)
############################################################################ СОЗДАНИЕ ТАБЛИЦЫ
        # Добавляем столбцы
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'phone', 'email'),
                                 height=45, show='headings')
        
        # Добавить параметры колонкам 
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)

        # Подписи колонок
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')

        # Упаковка
        self.tree.pack(side=tk.LEFT)

        # Ползунок
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
############################################################################ ВСЕ МЕТОДЫ
    # Добавление данных
    def records(self, name, phone, email):
        self.db.insert_data(name, phone, email)
        self.view_records()

    # Отображение данных в TreeView
    def view_records(self):
        self.db.cur.execute(''' SELECT * FROM users ''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]
        
    # Метод обновления данных
    def update_record(self, name, phone, email):
        id = self.tree.set(self.tree.selection()[0],  '#1')
        self.db.cur.execute(''' UPDATE users SET name=?, phone=?, email=? WHERE ID=? ''',
                            (name, phone, email, id))
        self.db.conn.commit()
        self.view_records()

    # Удаление записей
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.cur.execute('''DELETE FROM users WHERE id=?''',
                              (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # Поиск записи
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.cur.execute(
            '''SELECT * FROM users WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]
############################################################################ ВЫЗОВ КЛАССОВ
    
    # Метод вызывающий окно добавления
    def open_child(self):
        Child()

    # Метод вызывающий окно обновления
    def open_update_dialog(self):
        Update()

    # метод отвечающий за вызов окно поиска
    def open_search_dialog(self):
        Search()  
############################################################################
# Дочернее окно
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить контакт')
        self.geometry('400x220')
        self.resizable(False,False)
        self.grab_set()
        self.focus_set()
############################################################################
        label_name = tk.Label(self, text='ФИО: ')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон: ')
        label_phone.place(x=50, y=80)
        label_email= tk.Label(self, text='E-mail: ')
        label_email.place(x=50, y=110)
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
############################################################################

        # Кнопка закрытия 
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        # Кнопка добавления
        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(x=220, y=170)
        self.btn_add.bind('<Button-1>', lambda event:
                          self.view.records(self.entry_name.get(),
                                            self.entry_phone.get(),
                                            self.entry_email.get()))

############################################################################
        
# Класс редактирования контактов
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()

    def init_update(self):
        self.title('Редактировать позицию')
        self.btn_add.destroy()

        self.btn_upd = ttk.Button(self, text='Редактировать')
        self.btn_upd.bind('<Button-1>', lambda event:
                          self.view.update_record(self.entry_name.get(),
                                                self.entry_phone.get(),
                                                self.entry_email.get()))
        self.btn_upd.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_upd.place(x=200, y=170)

    def default_data(self):
        self.db.cur.execute('''SELECT * FROM users WHERE ID=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1')),)
        
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_phone.insert(0, row[3])
############################################################################
        
# Класс поиска записи
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', 
                        lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', 
                        lambda event: self.destroy(), add='+')
############################################################################

# Класс Базы данных
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cur = self.conn.cursor()
        self.cur.execute(''' CREATE TABLE IF NOT EXISTS users(
                                id INTEGER PRIMARY KEY NOT NULL,
                                name TEXT,
                                phone TEXT,
                                email TEXT ) ''')
        self.conn.commit()
   
    def insert_data (self, name, phone, email):
        self.cur.execute(''' INSERT INTO users (name, phone, email)
                         VALUES  (?, ?, ?)''', (name, phone, email))
        self.conn.commit()

############################################################################

if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга')
    root.geometry('645x450')
    root.resizable(False,False)
    root.configure(bg='White')
    root.mainloop()
