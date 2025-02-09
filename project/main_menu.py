import tkinter as tk
import subprocess
import sys
from PIL import Image, ImageTk
import pygame

# Инициализация Pygame Mixer (чтобы музыка не дублировалась)
if not pygame.mixer.get_init():
    pygame.mixer.init()

# Проверка, запущена ли музыка
if not pygame.mixer.music.get_busy():
    pygame.mixer.music.load("AUDIO-2025-02-09-19-19-04.mp3")  # Укажите ваш файл
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)  # Музыка играет бесконечно

# Функция для запуска Pygame-игры
def run_pygame_game(game_file):
    pygame.mixer.music.stop()  # Останавливаем музыку перед запуском игры
    root.destroy()
    subprocess.run([sys.executable, game_file])
    pygame.mixer.music.play(-1)  # Возобновляем музыку при возврате

# Функция для запуска игры "Камень, ножницы, бумага"
def run_rps_game():
    pygame.mixer.music.stop()  # Останавливаем музыку перед запуском игры
    root.destroy()
    subprocess.run([sys.executable, "rps_game.py"])
    pygame.mixer.music.play(-1)  # Возобновляем музыку при возврате

# Создание окна меню
root = tk.Tk()
root.title("Главное меню")
root.geometry("800x600")

# Загрузка фонового изображения
background_image = Image.open("Screenshot_49.png")
background_image = background_image.resize((800, 600))
bg_photo = ImageTk.PhotoImage(background_image)

# Установка фонового изображения
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Заголовок меню
label = tk.Label(root, text="Choose a game", font=("Arial", 20, "bold"), bg="#dfe6e9")
label.place(relx=0.5, rely=0.1, anchor="center")

# Кнопки выбора игры
btn_rps = tk.Button(root, text="Rock, scissors, paper", font=("Arial", 14), width=30, command=run_rps_game)
btn_rps.place(relx=0.5, rely=0.4, anchor="center")

btn_race = tk.Button(root, text="Racing game", font=("Arial", 14), width=30, command=lambda: run_pygame_game("racing_game.py"))
btn_race.place(relx=0.5, rely=0.5, anchor="center")

btn_tank = tk.Button(root, text="Tank battle", font=("Arial", 14), width=30, command=lambda: run_pygame_game("tank_game.py"))
btn_tank.place(relx=0.5, rely=0.6, anchor="center")

# Кнопка выхода
def quit_application():
    pygame.mixer.music.stop()  # Останавливаем музыку перед выходом
    root.quit()

btn_exit = tk.Button(root, text="Выход", font=("Arial", 14), width=30, command=quit_application)
btn_exit.place(relx=0.5, rely=0.7, anchor="center")

# Запуск главного цикла Tkinter
root.mainloop()
