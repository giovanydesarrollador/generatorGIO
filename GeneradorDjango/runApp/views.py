from django.shortcuts import render
from django.http import HttpResponse
import random
import string
from .models import TbGenerated
# Create your views here.
def index(request):
    return HttpResponse("<h1>¡Hola desde la app GioGenerator!</h1>")

# --- Función MODIFICADA para Generar una Contraseña Candidata ---
def generate_candidate_password(length=10): # Longitud fija en 10 por defecto
    """
    Genera una cadena aleatoria de 10 caracteres:
    exactamente 8 dígitos y 2 letras (excluyendo i, I, l, L, o, O).
    Nota: ñ/Ñ no están en string.ascii_letters, por lo que no es necesario excluirlas explícitamente.
    """
    if length != 10:
        # Forzar longitud 10 según el requisito, ignorando el parámetro si es distinto
        length = 10
        print("Advertencia: Se forzó la longitud de la contraseña a 10 caracteres.")

    # --- Define los caracteres permitidos ---
    digits = string.digits       # '0123456789'
    all_ascii_letters = string.ascii_letters # a-z, A-Z
    forbidden_letters = "iIlLoO" # Letras prohibidas
    # Crea la cadena de letras permitidas filtrando las prohibidas
    allowed_letters = "".join(c for c in all_ascii_letters if c not in forbidden_letters)

    # --- Define la composición exacta ---
    num_letters = 2
    num_digits = 8 # Asegura que num_letters + num_digits == length (10)

    # --- Genera los caracteres requeridos ---
    # Elige 2 letras aleatorias del conjunto permitido
    chosen_letters = random.choices(allowed_letters, k=num_letters)
    # Elige 8 dígitos aleatorios
    chosen_digits = random.choices(digits, k=num_digits)

    # --- Combina y mezcla ---
    password_chars = chosen_letters + chosen_digits
    random.shuffle(password_chars)

    # --- Une para formar la contraseña final ---
    password = "".join(password_chars)

    return password


# --- Vista Principal (SIN CAMBIOS EN SU LÓGICA INTERNA) ---
def generate_and_save_view(request):
    """
    Vista para generar, verificar unicidad y guardar la contraseña.
    Utiliza la nueva lógica de generate_candidate_password.
    """
    context = {} # Diccionario para pasar datos a la plantilla
    new_password = None
    message = ""
    max_attempts = 100 # Límite para evitar bucles infinitos si algo va mal
    attempts = 0

    if request.method == 'POST':
        print("Solicitud POST recibida para generar contraseña.") # Mensaje de depuración
        while attempts < max_attempts:
            attempts += 1
            print(f"Intento #{attempts}...") # Mensaje de depuración

            # 1. Genera una contraseña candidata (ahora usará la nueva función)
            #    Llama a la función sin argumentos para usar el default de 10
            candidate = generate_candidate_password()
            print(f"Candidato generado: {candidate}") # Mensaje de depuración

            # 2. Verifica si ya existe en la base de datos
            #    La verificación sigue siendo la misma
            is_unique = not TbGenerated.objects.filter(data_string=candidate).exists()
            print(f"¿Es único? {is_unique}") # Mensaje de depuración

            if is_unique:
                # 3. Si es única, guárdala en la BD (la lógica de guardado no cambia)
                try:
                    # El modelo TbGenerated tiene max_length=11, así que una de 10 cabe perfectamente.
                    generated_obj = TbGenerated.objects.create(data_string=candidate)
                    new_password = generated_obj.data_string # O simplemente 'candidate'
                    message = f"Cadena generada y guardada con éxito (ID: {generated_obj.pk})!"
                    print(message) # Mensaje de depuración
                    break # Sal del bucle while, ya encontramos una
                except Exception as e:
                    # Manejo básico de errores al guardar (poco probable si la validación es correcta)
                    message = f"Error al guardar la contraseña: {e}"
                    print(message) # Mensaje de depuración
                    break # Sal del bucle si hay error al guardar
            else:
                 print(f"Contraseña '{candidate}' ya existe. Generando otra...") # Mensaje de depuración
                 # Si no es única, el bucle while continuará para generar otra

        if not new_password and attempts >= max_attempts:
            message = f"No se pudo generar una cadena única después de {max_attempts} intentos."
            print(message) # Mensaje de depuración

        context['new_password'] = new_password
        context['message'] = message

    # Siempre renderiza la plantilla, ya sea en GET o después de POST
    return render(request, 'runApp/generator.html', context)