from docxtpl import DocxTemplate #pip install docxtpl
from datetime import datetime
from pathlib import Path

# Cargar plantilla
BASE_DIR = Path(__file__).parent
doc = DocxTemplate(BASE_DIR / "plantilla.docx")

# Datos dinámicos
contexto = {
    "cliente": "Empresa ABC",
    "fecha": datetime.now().strftime("%d/%m/%Y"),
    "productos": [
        {"nombre": "Camiseta", "precio": 12.5},
        {"nombre": "Pantalón", "precio": 29.9},
        {"nombre": "Zapatillas", "precio": 59.95},
    ],
    "total": 12.5 + 29.9 + 59.95
}

# Renderizar documento
doc.render(contexto)

# Guardar resultado
doc.save(BASE_DIR / "informe_generado.docx")

print("Documento generado correctamente")