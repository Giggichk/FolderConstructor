import os
import shutil
import pathlib
import sys

import customtkinter as custom
from PIL import Image
import tkinter.filedialog as dialog_window

from searcher import list_all_contents
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class ToplevelWindowDelete(custom.CTkToplevel):
    def __init__(self, parent, scrollable_frame, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.scrollable_frame = scrollable_frame
        self.geometry("310x150")
        self.grab_set()

        self.questian_frame = custom.CTkFrame(self, width=200, height=450, fg_color='#575757')
        self.questian_frame.grid(padx=0, pady=7)

        self.label_delete = custom.CTkLabel(self.questian_frame, text=f'Вы точно хотите удалить?', width=100, height=70)
        self.label_delete.grid()

        self.choice_frame = custom.CTkFrame(self.questian_frame, width=100, height=100)
        self.choice_frame.grid()

        with open(resource_path('data.txt'), 'r', encoding='utf-8') as file_data:
            path = file_data.read()
            self.ye_button = custom.CTkButton(self.choice_frame, text='Да', command=lambda b=path: self.delete_file(b))
            self.ye_button.grid(row=0, column=0, pady=10, ipadx=10, ipady=10)

        self.not_button = custom.CTkButton(self.choice_frame, text='Нет', command=self.not_delete_file)
        self.not_button.grid(row=0, column=1, pady=10, ipadx=10, ipady=10)

    def delete_file(self, path):
        parent_folder = os.path.dirname(path)

        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)

        open(resource_path('data.txt'), 'w').close()

        if os.path.exists(parent_folder):
            contents = list_all_contents(parent_folder)
            self.scrollable_frame.update_content(contents)

        self.destroy()

    def not_delete_file(self):
        self.destroy()


class ToplevelWindowNotCorrect(custom.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x150")

        self.label = custom.CTkLabel(self, text="Некорректный путь к файлу/папке")
        self.label.pack(padx=20, pady=20)
        self.grab_set()


class ToplevelWindowNotIsDir(custom.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x150")

        self.label = custom.CTkLabel(self, text="Невозможно отсортировать \nнепосредственно файл!")
        self.label.pack(padx=20, pady=20)
        self.grab_set()


class ToplevelWindowNotExists(custom.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x150")

        self.label = custom.CTkLabel(self, text="Файл или папка не существует!")
        self.label.pack(padx=20, pady=20)
        self.grab_set()


class ToplevelWindowFailed(custom.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x150")

        self.label = custom.CTkLabel(self, text="Файл Data.txt пустой!")
        self.label.pack(padx=20, pady=20)
        self.grab_set()


class ToplevelWindowInfo(custom.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x400")

        with open(resource_path('data.txt'), 'r', encoding='utf-8') as file_data:
            path = file_data.read()
            self.label = custom.CTkLabel(self, text=f"Полный путь\n{path}")
            self.label.pack(padx=20, pady=20)
            self.grab_set()


class MainFrame(custom.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=480, height=730, fg_color='#363636')


class ClearButton(custom.CTkButton):
    def __init__(self, master, command_unvis, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(master, text='Очистить', font=("Verdana", 12, 'bold'), fg_color='white', border_color='black',
                       text_color='black', border_width=2, command=command_unvis.univisible_buttons)


class UpdateButton(custom.CTkButton):
    def __init__(self, master, command_up, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(master, text='Обновить', font=("Verdana", 12, 'bold'), fg_color='white', border_color='black',
                       text_color='black', border_width=2, command=self.update)

        self.command_up = command_up

    def update(self):
        with open(resource_path('data.txt'), 'r', encoding='utf-8') as file_data:
            path = file_data.read()
            if not path == '' and os.path.isdir(path):
                content = list_all_contents(path)
                self.command_up.update_content(content)


class ImageFrame(custom.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=370, height=370, fg_color='#363636')
        self.image = custom.CTkImage(dark_image=Image.open(resource_path('acetone-2025724-224628-241.png')), size=(370, 370))
        self.vv_Label = custom.CTkLabel(self, text='', image=self.image)
        self.vv_Label.pack()


class ScrollDictFrame(custom.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.color = '#D4D4D8'
        self.configure(width=445, height=200)
        self.buttons = []

    def update_content(self, content_list):
        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()

        for i_content in content_list:
            button = custom.CTkButton(
                self,
                text=f'{os.path.normpath(i_content)}',
                fg_color=self.color,
                text_color='black',
                command=lambda path=os.path.normpath(i_content): self.invisible_buttons(path))
            button.pack(anchor='w')
            self.buttons.append(button)

    def invisible_buttons(self, name_path):
        for btn in self.buttons:
            if name_path == btn._text:
                btn.configure(fg_color='red', state='disable')
            else:
                btn.configure(state='disabled')

        with open(resource_path('data.txt'), 'w', encoding='utf-8') as file_data:
            file_data.write(name_path)

    def univisible_buttons(self):
        for btn in self.buttons:
            btn.configure(fg_color=self.color, state='normal')
        open(resource_path('data.txt'), 'w', encoding='utf-8').close()


class MenuButtons(custom.CTkFrame):
    def __init__(self, master, scrollable_frame, **kwargs):
        super().__init__(master, **kwargs)

        self.scrollable_frame = scrollable_frame

        self.configure(fg_color='#404040')
        self.menu_button_load = custom.CTkButton(self, text='Загрузить', font=("Verdana", 14, 'bold'), fg_color='white',
                                            border_color='black', text_color='black', border_width=2, command=self.choose_folder)
        self.menu_button_sort = custom.CTkButton(self, text='Отсортировать', font=("Verdana", 14, 'bold'), fg_color='white',
                                            border_color='black', text_color='black', border_width=2, command=self.sort_func)
        self.menu_button_delete = custom.CTkButton(self, text='Удалить', font=("Verdana", 14, 'bold'), fg_color='white', hover_color='red',
                                            border_color='black', text_color='black', border_width=2, command=self.delete_of_path)
        self.menu_button_info = custom.CTkButton(self, text='Информация', font=("Verdana", 14, 'bold'), fg_color='white',
                                            border_color='black', text_color='black', border_width=2, command=self.open_toplevel_info)
        self.menu_button_load.grid(row=0, column=0, padx=15, pady=5, ipadx=10, ipady=10)
        self.menu_button_sort.grid(row=0, column=1, padx=15, pady=5, ipadx=10, ipady=10)
        self.menu_button_delete.grid(row=1, column=0, padx=15, pady=5, ipadx=10, ipady=10)
        self.menu_button_info.grid(row=1, column=1, padx=15, pady=5, ipadx=10, ipady=10)

    def sort_func(self):
        with open(resource_path('data.txt'), 'r', encoding='utf-8') as file_data:
            folder_path = file_data.read().strip()

        if not folder_path or not os.path.exists(folder_path):
            ToplevelWindowNotExists(self)
            return

        if not os.path.isdir(folder_path):
            ToplevelWindowNotIsDir(self)
            return

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            if os.path.isdir(file_path):
                continue

            file_extension = pathlib.Path(filename).suffix.lstrip('.').lower()
            if not file_extension:
                file_extension = "no_extension"

            target_folder = os.path.join(folder_path, file_extension)
            os.makedirs(target_folder, exist_ok=True)

            shutil.move(file_path, os.path.join(target_folder, filename))

        content = list_all_contents(folder_path)
        self.scrollable_frame.update_content(content)


    def open_toplevel_info(self):
        with open(resource_path('data.txt'), 'r', encoding='utf-8') as file_data:
            path = file_data.read().strip()

            if not path:
                self.failed_operation = ToplevelWindowFailed(self)
            else:
                if os.path.exists(path):
                    self.toplevel_window = ToplevelWindowInfo(self)
                else:
                    self.toplevel_window_not_correct = ToplevelWindowNotCorrect(self)

    def choose_folder(self):
        self.folder = dialog_window.askdirectory(title="Выберите папку")
        if not self.folder:
            return
        with open(resource_path('data.txt'), 'w', encoding='utf-8') as file_data:
            file_data.write(self.folder)
        content = list_all_contents(self.folder)
        self.scrollable_frame.update_content(content)

    def delete_of_path(self):
        with open(resource_path('data.txt'), 'r', encoding='utf-8') as file_data:
            path = file_data.read().strip()
            if os.path.exists(path):
                ToplevelWindowDelete(self, scrollable_frame=self.scrollable_frame)


class App(custom.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x730")
        self.title("FolderConstructor")
        self.resizable(width=False, height=False)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.main_frame = MainFrame(self)
        self.main_frame.grid(padx=15, pady=0)

        self.top_image = ImageFrame(self.main_frame)
        self.top_image.grid()

        self.scrollable_frame = ScrollDictFrame(self.main_frame)
        self.scrollable_frame.grid()

        self.update_btn = UpdateButton(self.main_frame, self.scrollable_frame)
        self.update_btn.grid(sticky='w', row=3)

        self.clear_btn = ClearButton(self.main_frame, self.scrollable_frame)
        self.clear_btn.grid(sticky='e', row=3)

        self.menu_buttons = MenuButtons(self.main_frame, scrollable_frame=self.scrollable_frame)
        self.menu_buttons.grid(pady=5)

    def on_close(self):
        with open(resource_path('data.txt'), 'w', encoding='utf-8') as f:
            f.write('')

        self.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()