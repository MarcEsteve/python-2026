import win32com.client #Sirve para interactuar con aplicaciones de Windows
import imapclient #Sirve para interactuar con servidores de correo
# import pyzmail #Sirve para interactuar con correos electrónicos
import subprocess #Sirve para ejecutar comandos del sistema de forma recomendada
# Limpiar la pantalla
subprocess.run(["cmd", "/c", "cls"], check=False)
# Como detectar que funciona correctamente
try:
    # Aqui se intenta conectar a la aplicación de Outlook
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
except:
    # Esta linea de código es para que no se muestre un error en caso de que no se pueda conectar a Outlook
    print("No se ha podido instalar pywin32.")
else:
    # Si se conecta correctamente a Outlook, se mostrará este mensaje
    print("pywin32 se ha instalado correctamente.")