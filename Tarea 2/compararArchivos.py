import difflib

def comparar_archivos(archivo1, archivo2):
    with open(archivo1, 'r', encoding='utf-8') as f1, open(archivo2, 'r', encoding='utf-8') as f2:
        lineas1 = f1.readlines()
        lineas2 = f2.readlines()

    diferencias = list(diff(lineas1, lineas2))

    if diferencias:
        print("Diferencias encontradas:")
        for diferencia in diferencias:
            print(diferencia)
    else:
        print("Los archivos son iguales.")

def diff(a, b):
    matcher = difflib.SequenceMatcher(None, a, b)
    for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):
        if tag == 'delete':
            yield f"Eliminar {i1+1}-{i2} de la primera línea"
        elif tag == 'insert':
            yield f"Insertar '{b[j1]}' en la línea {j1+1} del segundo archivo"
        elif tag == 'replace':
            yield (f"Reemplazar {i1+1}-{i2} de la primera línea "
                   f"con '{b[j1]}' en la línea {j1+1} del segundo archivo")

# Reemplaza 'archivo1.txt' y 'archivo2.txt' con los nombres reales de tus archivos
comparar_archivos('columnas21-22.txt', 'columnas22-23.txt')
