from django.db import models
from django.utils.timezone import now
# Ya no necesitamos importar timezone si solo usamos auto_now_add en DateField

# Create your models here.

class TbGenerated(models.Model):
    """
    Modelo para almacenar la información generada (data_string)
    junto con su fecha de creación. Corresponde a la tabla 'tb_generated'.
    """
    # --- Campo ID (Automático) ---
    # Django añade automáticamente un campo 'id' como clave primaria
    # numérica autoincremental (AutoField), cumpliendo tu requisito.

    # --- Campo para Guardar la Información ---
    data_string = models.CharField(
        max_length=11,              # Longitud máxima de 11 caracteres (VARCHAR(11))
        verbose_name="Información Guardada", # Nombre legible (opcional)
        help_text="La cadena de datos generada (máx 11 caracteres)." # Texto de ayuda (opcional)
        # Puedes añadir más opciones si las necesitas, como:
        # null=True, blank=True, # Si quieres permitir que este campo esté vacío
        # unique=True,          # Si cada cadena debe ser única en la tabla
    )

    # --- Campo para la Fecha de Creación ---
    data_created = models.DateField(
        verbose_name="Fecha de Creación",
        auto_now_add=True  # <-- ¡IMPORTANTE! Usamos SOLO esta opción.
                           # Guarda la fecha automáticamente SOLO al crear el registro.
                           # Esto evita el error E160.
    )

    # --- Configuración Adicional (Opcional pero Recomendada) ---
    class Meta:
        db_table = 'tb_generated'  # Nombre exacto de la tabla en la base de datos
        verbose_name = "Registro Generado"
        verbose_name_plural = "Registros Generados"
        ordering = ['-data_created', 'id'] # Ordenar por defecto: los más nuevos primero

    # --- Representación en Texto del Objeto (Opcional pero Recomendada) ---
    def __str__(self):
        # Usamos self.pk que siempre apunta a la clave primaria (usualmente 'id')
        return f"ID: {self.pk} | Dato: {self.data_string} | Creado: {self.data_created}"