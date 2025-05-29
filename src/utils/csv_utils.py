import csv
import os
import json
from models.entrenaments import Entrenament
from models.forca import Forca
from models.cardio import Cardio
from models.usuari import Usuari

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
                entrenaments.append(Cardio(nom, descripcio, exercicis, distancia))
            elif tipus == 'Forca':
                pes = row.get('pes_kg', '')
                entrenaments.append(Forca(nom, descripcio, exercicis, pes))
            else:
                entrenaments.append(Entrenament(nom, descripcio, exercicis))
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