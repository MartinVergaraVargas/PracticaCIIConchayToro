import pandas as pd
import os

def guardar_nombres_columnas_en_excel(archivos_excel, nombre_excel_salida):
    # Crear un DataFrame vacío para almacenar los nombres de las columnas
    df_resultado = pd.DataFrame()

    for archivo in archivos_excel:
        # Leer solo la primera fila de cada archivo para obtener los nombres de las columnas
        df_temporal = pd.read_excel(archivo, nrows=0)

        # Obtener los nombres de las columnas como una lista
        nombres_columnas = df_temporal.columns.tolist()

        # Crear un DataFrame temporal con una columna que contiene los nombres de las columnas
        df_temporal = pd.DataFrame({f'Columnas - {archivo}': nombres_columnas})

        # Agregar el DataFrame temporal al DataFrame principal
        df_resultado = pd.concat([df_resultado, df_temporal], axis=1)

    # Guardar el DataFrame en un archivo Excel
    df_resultado.to_excel(nombre_excel_salida, index=False)
# Lista de archivos Excel que deseas procesar
archivos_excel = ['RFR_pbi_21-22 - copia.xlsx', 'RFR_pbi_21-22.xlsx', 'RFR_pbi_22-23 - copia.xlsx', 'RFR_pbi_22-23.xlsx']

# Nombre del archivo Excel de salida
nombre_excel_salida = 'columnas.xlsx'

# Llamar a la función para guardar los nombres de las columnas en el archivo Excel de salida
guardar_nombres_columnas_en_excel(archivos_excel, nombre_excel_salida)
