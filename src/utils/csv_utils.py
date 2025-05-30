import csv
import os
import json

CSV_FILE = os.path.join('data', 'rutines.csv')

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