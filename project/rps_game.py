import tkinter as tk
from random import randint
from PIL import Image, ImageTk

# Global variables
youpoint = 0
pcpoint = 0
round_D = 1
round_Max = 3
wincombination = [(1, 2), (2, 3), (3, 1)]

# Function to load images
def load_images():
    return {
        "win": ImageTk.PhotoImage(Image.open("windows-12_large.png").resize((600, 400))),  # Победа
        "lose": ImageTk.PhotoImage(Image.open("bsod-2023-04-19_100831.jpg").resize((600, 400))),  # Поражение
        "tie": ImageTk.PhotoImage(Image.open("windows_mac_os_change-740x416.webp").resize((600, 400))),  # Ничья
        "background": ImageTk.PhotoImage(Image.open("og_og_1570535460269043702.jpg").resize((600, 600)))  # Фон игры
    }

# Function to handle the move
def play(choice):
    global youpoint, pcpoint, round_D
    if round_D > round_Max:
        return

    pchand = randint(1, 3)

    # Определение результата раунда
    if choice != pchand:
        if (choice, pchand) in wincombination:
            youpoint += 1
        else:
            pcpoint += 1
    else:
        youpoint += 1
        pcpoint += 1

    update_score()
    round_D += 1

    if round_D > round_Max:
        show_final_result()

# Function to update the score
def update_score():
    score_label.config(text=f"Score: {youpoint}:{pcpoint}")

# Function to show the final result with an image and custom text
def show_final_result():
    # Удаляем все элементы интерфейса
    for widget in root.winfo_children():
        widget.destroy()

    # Определяем результат
    if youpoint > pcpoint:
        result_image = result_images["win"]
        result_text = "YOU WIN! You saved your Windows system!"
    elif youpoint < pcpoint:
        result_image = result_images["lose"]
        result_text = "YOU LOSE! Your Windows system is gone!"
    else:
        result_image = result_images["tie"]
        result_text = "IT'S A TIE! You've switched to macOS!"

    # Показать результат с изображением и текстом
    result_label = tk.Label(root, image=result_image)
    result_label.pack()

    text_label = tk.Label(root, text=result_text, font=("Arial", 18, "bold"), bg="#ffffff")
    text_label.pack(pady=20)

    # Кнопка выхода в главное меню
    btn_menu = tk.Button(
        root, text="MAIN MENU", font=("Arial", 14, "bold"), bg="#3498db", fg="white",
        command=return_to_menu
    )
    btn_menu.pack(pady=10)

    # Кнопка рестарта игры
    btn_restart = tk.Button(
        root, text="RESTART GAME", font=("Arial", 14, "bold"), bg="#2ecc71", fg="white",
        command=restart_game
    )
    btn_restart.pack(pady=10)

# Function to restart the game
def restart_game():
    global youpoint, pcpoint, round_D
    youpoint = 0
    pcpoint = 0
    round_D = 1

    # Перезапуск интерфейса
    for widget in root.winfo_children():
        widget.destroy()
    setup_game_ui()

# Function to return to the main menu
def return_to_menu():
    root.destroy()

# Function to set up the game UI
def setup_game_ui():
    global score_label

    # Установка фона
    background_label = tk.Label(root, image=result_images["background"])
    background_label.place(relwidth=1, relheight=1)  # Заполняет всё окно

    # Header
    header_label = tk.Label(root, text="Rock, Scissors, Paper", font=("Arial", 22, "bold"), bg="#ffffff")
    header_label.pack(pady=20)

    # Score label
    score_label = tk.Label(root, text=f"Score: {youpoint}:{pcpoint}", font=("Arial", 16, "bold"), bg="#ffffff")
    score_label.pack(pady=10)

    # Buttons
    button_style = {
        "font": ("Arial", 12, "bold"),
        "width": 15,
        "height": 2,
        "relief": "flat",
        "fg": "white",
        "activeforeground": "black"
    }

    btn_rock = tk.Button(root, text="ROCK", bg="#3498db", activebackground="#2980b9", command=lambda: play(1), **button_style)
    btn_rock.pack(pady=10)

    btn_paper = tk.Button(root, text="PAPER", bg="#2ecc71", activebackground="#27ae60", command=lambda: play(3), **button_style)
    btn_paper.pack(pady=10)

    btn_scissors = tk.Button(root, text="SCISSORS", bg="#e74c3c", activebackground="#c0392b", command=lambda: play(2), **button_style)
    btn_scissors.pack(pady=10)

# Create the window
root = tk.Tk()
root.title("Rock, Scissors, Paper")
root.geometry("600x600")

# Загрузка изображений после создания root
result_images = load_images()

# Настройка начального интерфейса игры
setup_game_ui()

# Start the window
root.mainloop()
