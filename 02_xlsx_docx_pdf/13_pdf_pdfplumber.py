import pdfplumber #pip install pdfplumber
from pathlib import Path

BASE_DIR = Path(__file__).parent
ruta_pdf = BASE_DIR / "factura_ejemplo.pdf"

with pdfplumber.open(ruta_pdf) as pdf:
    for i, pagina in enumerate(pdf.pages):
        print(f"\n--- Página {i + 1} ---")
        
        # Extraer texto
        texto = pagina.extract_text()
        print("Texto:")
        print(texto)

        # Extraer tablas (si existen)
        tablas = pagina.extract_tables()
        
        if tablas:
            print("\nTablas encontradas:")
            for tabla in tablas:
                for fila in tabla:
                    print(fila)
        else:
            print("\nNo se encontraron tablas en esta página")