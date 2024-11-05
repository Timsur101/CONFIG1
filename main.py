import os
import shutil
import zipfile
import yaml
import tkinter as tk
from tkinter import scrolledtext

class ShellEmulator:
    def __init__(self, config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        
        self.fs_path = config['filesystem_path']
        self.startup_script = config['startup_script']
        
        self.temp_dir = 'temp_fs'
        self.current_dir = self.temp_dir
        
        self.unpack_filesystem()
        
        self.init_gui()
        
        self.run_startup_script()

    def unpack_filesystem(self):
        """ Распаковываем файловую систему """
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir)
        
        with zipfile.ZipFile(self.fs_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)

    def run_startup_script(self):
        """ Выполняем команды из стартового скрипта """
        with open(self.startup_script, 'r') as file:
            for line in file:
                self.execute_command(line.strip())

    def execute_command(self, command):
        """ Обработка и выполнение команд """
        if command == 'exit':
            self.root.quit()
        elif command.startswith('cd'):
            self.change_directory(command[3:])
        elif command == 'ls':
            self.list_directory()
        elif command == 'pwd':
            self.print_working_directory()
        elif command.startswith('rmdir'):
            self.remove_directory(command[6:])
        else:
            self.output_text.insert(tk.END, f"Unknown command: {command}\n")
    
    def change_directory(self, path):
        """ Обрабатываем команду cd """
        new_path = os.path.join(self.current_dir, path)
        if os.path.isdir(new_path):
            self.current_dir = new_path
            self.output_text.insert(tk.END, f"Changed directory to {self.current_dir}\n")
        else:
            self.output_text.insert(tk.END, f"No such directory: {path}\n")
    
    def list_directory(self):
        """ Обрабатываем команду ls """
        items = os.listdir(self.current_dir)
        self.output_text.insert(tk.END, '\n'.join(items) + '\n')
    
    def print_working_directory(self):
        """ Обрабатываем команду pwd """
        self.output_text.insert(tk.END, f"{self.current_dir}\n")
    
    def remove_directory(self, dir_name):
        """ Обрабатываем команду rmdir """
        target_dir = os.path.join(self.current_dir, dir_name)
        if os.path.isdir(target_dir):
            shutil.rmtree(target_dir)
            self.output_text.insert(tk.END, f"Removed directory: {dir_name}\n")
        else:
            self.output_text.insert(tk.END, f"No such directory: {dir_name}\n")
    
    def init_gui(self):
        """ Инициализация графического интерфейса """
        self.root = tk.Tk()
        self.root.title("Shell Emulator")
        
        self.output_text = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.output_text.pack()
        
        self.entry = tk.Entry(self.root, width=80)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.pack()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
    
    def on_enter(self, event):
        """ Обработка ввода команды """
        command = self.entry.get()
        self.entry.delete(0, tk.END)
        self.output_text.insert(tk.END, f"> {command}\n")
        self.execute_command(command)
    
    def on_exit(self):
        """ Очистка временной директории при выходе """
        shutil.rmtree(self.temp_dir)
        self.root.quit()
    
    def run(self):
        """ Запуск GUI """
        self.root.mainloop()

if __name__ == "__main__":
    emulator = ShellEmulator('config.yaml')
    emulator.run()
