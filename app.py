import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk

def update_rating(category, value):
    ratings[category] = value
    update_stars(category)

def update_stars(category):
    for i in range(5):
        img = star_filled if i < ratings[category] else star_empty
        star_buttons[category][i].config(image=img)
        star_buttons[category][i].image = img

def calculate_tip():
    service = ratings['service']
    food = ratings['food']
    
    if service >= 4 and food >= 4:
        tip = "15%"
    elif service >= 3 and food >= 3:
        tip = "10%"
    elif service >= 2 and food >= 2:
        tip = "5%"
    else:
        tip = "0%"
    
    result_label.config(text=f"Propina sugerida: {tip}")

root = tk.Tk()
root.title("Calculadora de Propinas")
root.geometry("300x400")

# Crear un marco principal para centrar el contenido
main_frame = tk.Frame(root)
main_frame.pack(expand=True)

ratings = {'service': 0, 'food': 0}
star_buttons = {'service': [], 'food': []}

# Cargar imágenes de estrellas
star_filled = ImageTk.PhotoImage(Image.open("estrella_llena.jpg").resize((40, 40)))
star_empty = ImageTk.PhotoImage(Image.open("estrella_vacia.jpg").resize((40, 40)))

# Crear sección de servicio
Label(main_frame, text="Servicio").pack()
frame_service = tk.Frame(main_frame)
frame_service.pack()
for i in range(5):
    btn = Button(frame_service, image=star_empty, command=lambda i=i: update_rating('service', i+1))
    btn.pack(side=tk.LEFT)
    star_buttons['service'].append(btn)

# Crear sección de comida
Label(main_frame, text="Comida").pack()
frame_food = tk.Frame(main_frame)
frame_food.pack()
for i in range(5):
    btn = Button(frame_food, image=star_empty, command=lambda i=i: update_rating('food', i+1))
    btn.pack(side=tk.LEFT)
    star_buttons['food'].append(btn)

# Botón para calcular propina
Button(main_frame, text="Calcular Propina", command=calculate_tip).pack()
result_label = Label(main_frame, text="Propina sugerida: ")
result_label.pack()

root.mainloop()
