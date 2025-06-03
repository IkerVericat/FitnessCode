import csv
import os
import json


# Utils per a gestionar rutines i progressos d'entrenament
CSV_FILE = os.path.join('data', 'rutines.csv')
PROGRESSOS_FILE = os.path.join('data', 'progressos.csv')

# Funcions per a gestionar rutines d'entrenament
def guardar_entrenament(entrenament):
    os.makedirs('data', exist_ok=True)
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=entrenament.to_dict().keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(entrenament.to_dict())

def carregar_entrenaments():
    rutines = []
    if os.path.isfile('data/rutines.csv'):
        with open('data/rutines.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                exercicis = json.loads(row.get('exercicis', '[]'))
                
                # 🔒 Completa imatges si cal
                exercicis_totals = carregar_exercicis()
                for e in exercicis:
                    if 'imatge' not in e:
                        trobat = next((ex for ex in exercicis_totals if ex['nom'] == e['nom']), None)
                        e['imatge'] = trobat['imatge'] if trobat else 'barbell.png'

                rutines.append({
                    'titol': row.get('titol', 'Sense títol'),
                    'exercicis': exercicis
                })
    return rutines


def carregar_rutina(idx):
    rutines = []
    if os.path.isfile('data/rutines.csv'):
        with open('data/rutines.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rutines.append({
                    'titol': row.get('titol', 'Sense títol'),
                    'exercicis': json.loads(row.get('exercicis', '[]'))
                })
    if idx < 0 or idx >= len(rutines):
        return None
    return rutines[idx]


# Funcions per a gestionar exercicis
def carregar_exercicis():
    exercicis = []
    EXERCICIS_FILE = os.path.join('data', 'exercicis.csv')
    if not os.path.isfile(EXERCICIS_FILE):
        print(f"⚠️ Fitxer {EXERCICIS_FILE} no trobat.")
        return exercicis
    with open(EXERCICIS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            exercici = {
                'nom': row['nom'],
                'muscul': row['muscul'],
                'imatge': row.get('imatge', 'barbell.png')
            }
            exercicis.append(exercici)
    return exercicis



def afegir_exercici_a_rutina(nom_rutina, exercici):
    """
    Afegeix un exercici (diccionari) a la rutina amb nom 'nom_rutina'.
    L'exercici s'afegeix a la llista d'exercicis de la rutina al fitxer rutines.csv.
    """
    # 💡 Comprova si falta la imatge, i l’afegeix buscant-la
    if 'imatge' not in exercici:
        exercicis_totals = carregar_exercicis()
        for e in exercicis_totals:
            if e['nom'] == exercici['nom']:
                exercici['imatge'] = e.get('imatge', 'barbell.png')
                break
        else:
            exercici['imatge'] = 'barbell.png'  # Per defecte si no trobat

    rutines = []
    updated = False

    # Carrega totes les rutines
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Carrega la llista d'exercicis
            exercicis = json.loads(row.get('exercicis', '[]'))
            if row.get('titol') == nom_rutina:
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


# Funcions per a gestionar progressos d'entrenament
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

def editar_rutina_csv(titol_original, nova_rutina):
    """
    titol_original: títol de la rutina a modificar (clau primària)
    nova_rutina: diccionari amb les dades noves (ha de tenir les mateixes claus que les altres rutines)
    """
    if not os.path.isfile(CSV_FILE):
        return False
    rutines = []
    updated = False
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('titol') == titol_original:
                rutines.append(nova_rutina)
                updated = True
            else:
                rutines.append(row)
    if updated:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=nova_rutina.keys())
            writer.writeheader()
            writer.writerows(rutines)
        return True
    return False