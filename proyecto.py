import pandas as pd

# Ruta del archivo CSV
ruta_csv = r'C:\Users\salas\Downloads\archivo.csv'  
try:
    df = pd.read_csv(ruta_csv)
except FileNotFoundError:
    print(f"No se encontró el archivo: {ruta_csv}")
    exit()

# Mostrar cuántas filas hay
print(f"El archivo contiene {len(df)} filas.")

# Pedir un número al usuario entre 1 y 71

while True:
    try:
        numero = int(input("Introduce un número entre 1 y 71: "))
        if 1 <= numero <= 71:
            break
        else:
            print("Número fuera de rango. Intenta de nuevo.")
    except ValueError:
        print("Eso no es un número válido. Intenta de nuevo.")

# Mostrar la fila correspondiente (se resta 1 porque los índices en Python empiezan en 0)
fila = df.iloc[numero - 1]
print("\nContenido de la fila seleccionada:")
print(fila)