import os
import subprocess
subprocess.run("cls", shell=True, check=False) # Windows cls, Mac/Linux "clear"


# Definir la carpeta donde se guardarán los archivos
carpeta = "archivos"

#Ejemplo para mostrar el commit push de GitHub


# Crear la carpeta si no existe
if not os.path.exists(carpeta):
    os.makedirs(carpeta)

# Paso 1: nombres "mal escritos" (inconsistentes)
archivos_mal_escritos = [
    "Rpt-VntsEnero.TXT",
    "analisis DATOS_2025.TxT",
    "proy final-v1.txt",
    "Doc_InformeFINAL.txt",
    "resuReunion_ult.txt"
]

# Crear los archivos con nombres inconsistentes
for archivo in archivos_mal_escritos:
    with open(os.path.join(carpeta, archivo), "w", encoding="utf-8") as f:
        f.write("Contenido de prueba\n")

# Paso 2: renombrar automáticamente con prefijo corto
prefijo = "arc_"

for indice, nombre_viejo in enumerate(archivos_mal_escritos, start=1):
    ruta_vieja = os.path.join(carpeta, nombre_viejo)
    nombre_nuevo = f"{prefijo}{indice:02d}.txt"
    ruta_nueva = os.path.join(carpeta, nombre_nuevo)
    os.rename(ruta_vieja, ruta_nueva)

print("✅ Proceso completo: creados con nombres inconsistentes y renombrados automáticamente.")
