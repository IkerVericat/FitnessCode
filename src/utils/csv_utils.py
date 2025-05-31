import csv
import os
import json

CSV_FILE = os.path.join('data', 'rutines.csv')
PROGRESSOS_FILE = os.path.join('data', 'progressos.csv')

def guardar_entrenament(entrenament):
    os.makedirs('data', exist_ok=True)
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=entrenament.to_dict().keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(entrenament.to_dict())

def carregar_entrenaments():
    entrenaments = []
    if not os.path.isfile(CSV_FILE):
        return entrenaments
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tipus = row.get('tipus', '')
            nom = row.get('nom', '')
            descripcio = row.get('descripcio', '')
            exercicis = json.loads(row.get('exercicis', '[]'))
            if tipus == 'Cardio':
                distancia = row.get('distancia_km', '')
                entrenaments.append({'tipus': 'Cardio', 'nom': nom, 'descripcio': descripcio, 'exercicis': exercicis, 'distancia_km': distancia})
            elif tipus == 'Forca':
                pes = row.get('pes_kg', '')
                entrenaments.append({'tipus': 'Forca', 'nom': nom, 'descripcio': descripcio, 'exercicis': exercicis, 'pes_kg': pes})
            else:
                entrenaments.append({'tipus': tipus, 'nom': nom, 'descripcio': descripcio, 'exercicis': exercicis})
    return entrenaments

def carregar_exercicis():
    exercicis = []
    EXERCICIS_FILE = os.path.join('data', 'exercicis.csv')
    if not os.path.isfile(EXERCICIS_FILE):
        return exercicis
    with open(EXERCICIS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            exercicis.append(row)
    return exercicis

def afegir_exercici_a_rutina(nom_rutina, exercici):
    """
    Afegeix un exercici (diccionari) a la rutina amb nom 'nom_rutina'.
    L'exercici s'afegeix a la llista d'exercicis de la rutina al fitxer rutines.csv.
    """
    rutines = []
    updated = False

    # Carrega totes les rutines
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Carrega la llista d'exercicis
            exercicis = json.loads(row.get('exercicis', '[]'))
            if row.get('nom') == nom_rutina:
                exercicis.append(exercici)
                row['exercicis'] = json.dumps(exercicis)
                updated = True
            rutines.append(row)

    # Si s'ha trobat i modificat la rutina, guarda-ho tot de nou
    if updated:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rutines[0].keys())
            writer.writeheader()
            writer.writerows(rutines)
        return True
    return False

def afegir_progres(progres):
    os.makedirs('data', exist_ok=True)
    file_exists = os.path.isfile(PROGRESSOS_FILE)
    with open(PROGRESSOS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=progres.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(progres)

def carregar_progressos(usuari=None):
    progressos = []
    if not os.path.isfile(PROGRESSOS_FILE):
        return progressos
    with open(PROGRESSOS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if usuari is None or row.get('usuari') == usuari:
                progressos.append(row)
    return progressos

def eliminar_entrenament_csv(data, rutina, exercici):
    if not os.path.isfile(PROGRESSOS_FILE):
        return
    entrenaments = []
    with open(PROGRESSOS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not (row['data'] == data and row['rutina'] == rutina and row['exercici'] == exercici):
                entrenaments.append(row)
    with open(PROGRESSOS_FILE, 'w', newline='', encoding='utf-8') as f:
        if entrenaments:
            writer = csv.DictWriter(f, fieldnames=entrenaments[0].keys())
            writer.writeheader()
            writer.writerows(entrenaments)

def eliminar_rutina_csv(titol):
    if not os.path.isfile(CSV_FILE):
        return
    rutines = []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('titol') != titol:
                rutines.append(row)
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        if rutines:
            writer = csv.DictWriter(f, fieldnames=rutines[0].keys())
            writer.writeheader()
            writer.writerows(rutines)