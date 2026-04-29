import xlwings as xw #pip install xlwings
from pathlib import Path

# Ruta donde se guardará el Excel
archivo_salida = Path("informe_ventas_xlwings.xlsx").absolute()

# Datos de ejemplo
ventas = [
    ["Producto", "Unidades", "Precio unitario", "Total"],
    ["Camiseta", 25, 12.50, None],
    ["Pantalón", 10, 29.90, None],
    ["Zapatillas", 8, 59.95, None],
    ["Mochila", 15, 24.50, None],
]

# Abrir Excel
app = xw.App(visible=True)
app.display_alerts = False

try:
    # Crear libro nuevo
    wb = xw.Book()
    sheet = wb.sheets[0]
    sheet.name = "Ventas"

    # Escribir datos desde A1
    sheet.range("A1").value = ventas

    # Añadir fórmulas en la columna Total
    for fila in range(2, 6):
        sheet.range(f"D{fila}").formula = f"=B{fila}*C{fila}"

    # Total general
    sheet.range("C7").value = "Suma Total"
    sheet.range("D7").formula = "=SUM(D2:D5)"

    # Formato de cabecera
    sheet.range("A1:D1").font.bold = True
    sheet.range("A1:D1").color = (220, 230, 241)

    # Formato numérico
    sheet.range("C2:D7").number_format = "#.##0,00 €"

    # Ajustar ancho de columnas
    sheet.autofit()

    # Guardar archivo
    wb.save(archivo_salida)

finally:
    # Cerrar libro y Excel
    wb.close()
    app.quit()

print(f"Archivo generado: {archivo_salida}")