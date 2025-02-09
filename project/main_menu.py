import tkinter as tk
import subprocess
import sys
from PIL import Image, ImageTk  # Убедитесь, что Pillow установлена: pip install pillow

# Функция для запуска Pygame-игры
def run_pygame_game(game_file):
    root.destroy()  # Закрываем главное меню
    subprocess.run([sys.executable, game_file])  # Запускаем выбранную Pygame-игру

# Функция для запуска игры "Камень, ножницы, бумага"
def run_rps_game():
    root.destroy()  # Закрываем главное меню
    subprocess.run([sys.executable, "rps_game.py"])  # Запускаем Tkinter-игру

# Создание окна меню
root = tk.Tk()
root.title("Главное меню")
root.geometry("800x600")  # Увеличиваем размеры для отображения фона

# Загрузка фонового изображения
background_image = Image.open("Screenshot_49.png")  # Укажите путь к вашему изображению
background_image = background_image.resize((800, 600))  # Масштабируем под размер окна
bg_photo = ImageTk.PhotoImage(background_image)

# Установка фонового изображения
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Заполняет весь экран

# Заголовок меню
label = tk.Label(root, text="Выберите игру", font=("Arial", 20, "bold"), bg="#dfe6e9")
label.place(relx=0.5, rely=0.1, anchor="center")  # Размещаем поверх фона

# Кнопки выбора игры
btn_rps = tk.Button(root, text="Камень, ножницы, бумага", font=("Arial", 14), width=30, command=run_rps_game)
btn_rps.place(relx=0.5, rely=0.4, anchor="center")

btn_race = tk.Button(root, text="Гоночная игра", font=("Arial", 14), width=30, command=lambda: run_pygame_game("racing_game.py"))
btn_race.place(relx=0.5, rely=0.5, anchor="center")

btn_tank = tk.Button(root, text="Танковая битва", font=("Arial", 14), width=30, command=lambda: run_pygame_game("tank_game.py"))
btn_tank.place(relx=0.5, rely=0.6, anchor="center")

# Кнопка выхода
btn_exit = tk.Button(root, text="Выход", font=("Arial", 14), width=30, command=root.quit)
btn_exit.place(relx=0.5, rely=0.7, anchor="center")

# Запуск главного цикла Tkinter
root.mainloop()
