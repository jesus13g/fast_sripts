import tkinter as tk

# Función para dibujar el borde en el Canvas
def dibujar_borde(canvas):
    x1, y1, x2, y2 = canvas.bbox("all")  # Obtener las coordenadas del borde del canvas
    canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)  # Dibujar el rectángulo del borde

# Crear la ventana principal
ventana_principal = tk.Tk()

# Crear el frame ajustable
frame_ajustable = tk.Frame(ventana_principal, width=200, height=200, bg="white")
frame_ajustable.pack(expand=True, fill="both")

# Crear el canvas
canvas = tk.Canvas(frame_ajustable, bg="white")
canvas.pack(expand=True, fill="both")

# Dibujar el borde alrededor del frame
canvas.bind("<Configure>", lambda event: dibujar_borde(canvas))

# Agregar elementos al frame
label = tk.Label(frame_ajustable, text="Contenido del Frame", bg="white")
label.pack()

# Ejecutar el bucle principal de la aplicación
ventana_principal.mainloop()
