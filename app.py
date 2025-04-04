import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Función para actualizar la calificación seleccionada
def update_rating(category, value):
    ratings[category] = value
    update_stars(category)

# Función para actualizar la visualización de las estrellas
def update_stars(category):
    for i in range(5):
        img = star_filled if i < ratings[category] else star_empty
        star_buttons[category][i].config(image=img)
        star_buttons[category][i].image = img

# Función para calcular la propina basada en la lógica difusa
def calculate_tip():
    service = ratings['service']
    food = ratings['food']
    
    # Definir las variables difusas para el servicio y la comida
    service_rating = ctrl.Antecedent(np.arange(1, 6, 1), 'service')
    food_rating = ctrl.Antecedent(np.arange(1, 6, 1), 'food')
    tip_percentage = ctrl.Consequent(np.arange(0, 16, 1), 'tip_percentage')  # Rango de 0 a 15%

    # Definir las funciones de membresía para el servicio
    service_rating['Excelente'] = fuzz.trapmf(service_rating.universe, [4.5, 5, 5, 5])
    service_rating['Bueno'] = fuzz.trapmf(service_rating.universe, [3.5, 4, 4.5, 5])
    service_rating['Regular'] = fuzz.trapmf(service_rating.universe, [2.5, 3, 3.5, 4])
    service_rating['Malo'] = fuzz.trapmf(service_rating.universe, [1.5, 2, 2.5, 3])
    service_rating['Pesimo'] = fuzz.trapmf(service_rating.universe, [1, 1, 1.5, 2])

    # Definir las funciones de membresía para la comida
    food_rating['Excelente'] = fuzz.trapmf(food_rating.universe, [4.5, 5, 5, 5])
    food_rating['Bueno'] = fuzz.trapmf(food_rating.universe, [3.5, 4, 4.5, 5])
    food_rating['Regular'] = fuzz.trapmf(food_rating.universe, [2.5, 3, 3.5, 4])
    food_rating['Malo'] = fuzz.trapmf(food_rating.universe, [1.5, 2, 2.5, 3])
    food_rating['Pesimo'] = fuzz.trapmf(food_rating.universe, [1, 1, 1.5, 2])

    # Definir las funciones de membresía para la propina (0% a 15%)
    tip_percentage['Generosa'] = fuzz.trapmf(tip_percentage.universe, [15, 15, 15, 15])
    tip_percentage['Adecuada'] = fuzz.trapmf(tip_percentage.universe, [5, 8, 12, 15])
    tip_percentage['Regular'] = fuzz.trapmf(tip_percentage.universe, [0, 3, 7, 10])
    tip_percentage['Ausente'] = fuzz.trapmf(tip_percentage.universe, [0, 0, 0, 0])

    # Definir las reglas basadas en la tabla proporcionada
    rule1 = ctrl.Rule(service_rating['Excelente'] & food_rating['Excelente'], tip_percentage['Generosa'])
    rule2 = ctrl.Rule(service_rating['Excelente'] & food_rating['Bueno'], tip_percentage['Generosa'])
    rule3 = ctrl.Rule(service_rating['Excelente'] & food_rating['Regular'], tip_percentage['Adecuada'])
    rule4 = ctrl.Rule(service_rating['Excelente'] & food_rating['Malo'], tip_percentage['Regular'])
    rule5 = ctrl.Rule(service_rating['Excelente'] & food_rating['Pesimo'], tip_percentage['Ausente'])
    rule6 = ctrl.Rule(service_rating['Bueno'] & food_rating['Excelente'], tip_percentage['Generosa'])
    rule7 = ctrl.Rule(service_rating['Bueno'] & food_rating['Bueno'], tip_percentage['Generosa'])
    rule8 = ctrl.Rule(service_rating['Bueno'] & food_rating['Regular'], tip_percentage['Adecuada'])
    rule9 = ctrl.Rule(service_rating['Bueno'] & food_rating['Malo'], tip_percentage['Regular'])
    rule10 = ctrl.Rule(service_rating['Bueno'] & food_rating['Pesimo'], tip_percentage['Ausente'])
    rule11 = ctrl.Rule(service_rating['Regular'] & food_rating['Excelente'], tip_percentage['Generosa'])
    rule12 = ctrl.Rule(service_rating['Regular'] & food_rating['Bueno'], tip_percentage['Adecuada'])
    rule13 = ctrl.Rule(service_rating['Regular'] & food_rating['Regular'], tip_percentage['Regular'])
    rule14 = ctrl.Rule(service_rating['Regular'] & food_rating['Malo'], tip_percentage['Ausente'])
    rule15 = ctrl.Rule(service_rating['Regular'] & food_rating['Pesimo'], tip_percentage['Ausente'])
    rule16 = ctrl.Rule(service_rating['Malo'] & food_rating['Excelente'], tip_percentage['Adecuada'])
    rule17 = ctrl.Rule(service_rating['Malo'] & food_rating['Bueno'], tip_percentage['Adecuada'])
    rule18 = ctrl.Rule(service_rating['Malo'] & food_rating['Regular'], tip_percentage['Regular'])
    rule19 = ctrl.Rule(service_rating['Malo'] & food_rating['Malo'], tip_percentage['Ausente'])
    rule20 = ctrl.Rule(service_rating['Malo'] & food_rating['Pesimo'], tip_percentage['Ausente'])
    rule21 = ctrl.Rule(service_rating['Pesimo'] & food_rating['Excelente'], tip_percentage['Regular'])
    rule22 = ctrl.Rule(service_rating['Pesimo'] & food_rating['Bueno'], tip_percentage['Regular'])
    rule23 = ctrl.Rule(service_rating['Pesimo'] & food_rating['Regular'], tip_percentage['Ausente'])
    rule24 = ctrl.Rule(service_rating['Pesimo'] & food_rating['Malo'], tip_percentage['Ausente'])
    rule25 = ctrl.Rule(service_rating['Pesimo'] & food_rating['Pesimo'], tip_percentage['Ausente'])

    # Crear el sistema de control y simulación
    tip_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25])
    tip_sim = ctrl.ControlSystemSimulation(tip_ctrl)

    # Ingresar las calificaciones en el sistema de control
    tip_sim.input['service'] = service
    tip_sim.input['food'] = food

    # Ejecutar la simulación
    tip_sim.compute()

    # Obtener el valor de la propina calculada
    tip = round(tip_sim.output['tip_percentage'], 2)
    
    # Mostrar la propina sugerida
    result_label.config(text=f"Propina sugerida: {tip}%")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Calculadora de Propinas")
root.geometry("300x400")

# Crear un marco principal para centrar el contenido
main_frame = tk.Frame(root)
main_frame.pack(expand=True)

# Diccionario para almacenar las calificaciones de servicio y comida
ratings = {'service': 0, 'food': 0}
star_buttons = {'service': [], 'food': []}

# Cargar imágenes de estrellas llenas y vacías
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

# Etiqueta para mostrar la propina sugerida
result_label = Label(main_frame, text="Propina sugerida: ")
result_label.pack()

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()