import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import random
import string
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

# --- Lógica de Generación de Contraseñas Modificada ---

# Definir las letras permitidas UNA SOLA VEZ para eficiencia
# Excluimos 'i', 'I', 'o', 'O', 'l', 'L' de string.ascii_letters
# 'ñ' y 'Ñ' no están en string.ascii_letters
EXCLUDED_CHARS = "iIoOlL" # Actualizamos la lista de excluidos
ALLOWED_LETTERS = "".join(c for c in string.ascii_letters if c not in EXCLUDED_CHARS)
# print(f"Letras permitidas: {ALLOWED_LETTERS}") # Para depuración

def generar_contrasena_especifica(longitud=10):
    """
    Genera UNA contraseña aleatoria con máximo 10 caracteres,
    solo números y letras (excluyendo i, I, o, O, l, L), con un máximo de 2 letras.
    """
    if longitud > 10: longitud = 10
    if longitud <= 0: return ""

    max_letras_posibles = min(2, longitud)
    num_letras = random.randint(0, max_letras_posibles)
    num_digitos = longitud - num_letras

    # Usar la cadena de letras filtrada
    letras = random.choices(ALLOWED_LETTERS, k=num_letras)
    digitos = random.choices(string.digits, k=num_digitos)

    lista_caracteres = letras + digitos
    random.shuffle(lista_caracteres)
    contrasena_final = "".join(lista_caracteres)
    return contrasena_final

def generar_multiples_contrasenas_unicas(cantidad, longitud=10):
    """
    Genera una cantidad específica de contraseñas ÚNICAS.
    """
    if cantidad <= 0: return []
    if longitud > 10: longitud = 10
    if longitud <= 0: return []

    contrasenas_generadas = set()
    max_intentos = cantidad * 100
    intentos = 0

    while len(contrasenas_generadas) < cantidad and intentos < max_intentos:
        nueva_contrasena = generar_contrasena_especifica(longitud)
        if nueva_contrasena:
             contrasenas_generadas.add(nueva_contrasena)
        intentos += 1

    if len(contrasenas_generadas) < cantidad:
        print(f"Advertencia: Solo se pudieron generar {len(contrasenas_generadas)} únicas de {cantidad}.")
        # Podríamos añadir un messagebox aquí si se prefiere una notificación GUI

    return list(contrasenas_generadas)

# --- Funciones de la Interfaz Gráfica (Sin cambios) ---
def ejecutar_generacion():
    """Se ejecuta al presionar el botón 'Generar'."""
    try:
        cantidad_str = entry_cantidad.get()
        if not cantidad_str:
            messagebox.showerror("Error", "Por favor, introduce una cantidad.")
            return
        cantidad = int(cantidad_str)
        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser un número positivo.")
            return
    except ValueError:
        messagebox.showerror("Error", "Por favor, introduce un número válido para la cantidad.")
        return

    text_area_passwords.config(state=tk.NORMAL)
    text_area_passwords.delete('1.0', tk.END)

    status_label.config(text="Generando...")
    app.update_idletasks()

    lista_contrasenas = generar_multiples_contrasenas_unicas(cantidad, 10)

    if lista_contrasenas:
        text_area_passwords.insert(tk.INSERT, "\n".join(lista_contrasenas))
        status_label.config(text=f"¡Se generaron {len(lista_contrasenas)} contraseñas únicas!")
        button_copy.config(state=tk.NORMAL if PYPERCLIP_AVAILABLE else tk.DISABLED)
    else:
        status_label.config(text="No se pudieron generar contraseñas.")
        button_copy.config(state=tk.DISABLED)

    text_area_passwords.config(state=tk.DISABLED)

def copiar_al_portapapeles():
    """Copia el contenido del área de texto al portapapeles."""
    if not PYPERCLIP_AVAILABLE:
        messagebox.showwarning("Copiado no disponible",
                               "La biblioteca 'pyperclip' no está instalada.\n"
                               "Instálala con: pip install pyperclip")
        return

    contrasenas_texto = text_area_passwords.get('1.0', tk.END).strip()
    if contrasenas_texto:
        try:
            pyperclip.copy(contrasenas_texto)
            status_label.config(text="¡Contraseñas copiadas al portapapeles!")
        except Exception as e:
            messagebox.showerror("Error al Copiar", f"No se pudo copiar al portapapeles:\n{e}")
            status_label.config(text="Error al copiar.")
    else:
        status_label.config(text="Nada que copiar.")

# --- Creación de la Interfaz Gráfica (Solo cambio en título) ---
app = tk.Tk()
app.title("Generador de Contraseñas Específicas (Sin i, o, l)") # Título actualizado
app.geometry("400x450")

frame_input = ttk.Frame(app, padding="10")
frame_input.pack(pady=10, fill=tk.X)

label_cantidad = ttk.Label(frame_input, text="Cantidad de contraseñas a generar:")
label_cantidad.pack(side=tk.LEFT, padx=5)

entry_cantidad = ttk.Entry(frame_input, width=10)
entry_cantidad.pack(side=tk.LEFT, padx=5)
entry_cantidad.insert(0, "10")

button_generate = ttk.Button(app, text="Generar Contraseñas", command=ejecutar_generacion)
button_generate.pack(pady=5)

text_area_passwords = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=45, height=15, state=tk.DISABLED)
text_area_passwords.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

frame_buttons_bottom = ttk.Frame(app, padding="5")
frame_buttons_bottom.pack(pady=5, fill=tk.X)

button_copy = ttk.Button(frame_buttons_bottom, text="Copiar Todo", command=copiar_al_portapapeles, state=tk.DISABLED)
if PYPERCLIP_AVAILABLE:
    button_copy.pack(side=tk.LEFT, padx=10, expand=True)
else:
    pass

status_label = ttk.Label(app, text="Introduce la cantidad y presiona 'Generar'")
status_label.pack(pady=5)

app.mainloop()