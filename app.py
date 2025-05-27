from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import csv
import os

app = Flask(__name__)

# --- Classes ---

class Entrenament:
    def __init__(self, nom, descripcio, exercicis):
        self.nom = nom
        self.descripcio = descripcio
        self.exercicis = exercicis

    # Conversió a diccionari per a guardar en CSV
    def to_dict(self):
        return {
            'tipus': self.__class__.__name__,
            'nom': self.nom,
            'descripcio': self.descripcio,
            'exercicis': self.exercicis
        }
    
    # Mètode per a obtenir la unitat de mesura
    def unitat(self):
        return "unitats"


# --- Herències d'Entrenament ---

# classe cardio
class Cardio(Entrenament):
    def __init__(self, nom, descripcio, exercicis, _distancia_km):
        super().__init__(nom, descripcio, exercicis)
        self.__distancia_km = _distancia_km  # atribut privat

    def to_dict(self):
        d = super().to_dict()
        d['distancia_km'] = self.__distancia_km
        return d

    def unitat(self):
        return "km"
    

# classe força
class Forca(Entrenament):
    def __init__(self, nom, descripcio, exercicis, pes_kg):
        super().__init__(nom, descripcio, exercicis)
        self.pes_kg = pes_kg  # atribut públic

    def to_dict(self):
        d = super().to_dict()
        d['pes_kg'] = self.pes_kg
        return d

    def unitat(self):
        return "kg"



# --- Funcions auxiliars ---

CSV_FILE = 'rutines.csv'

def guardar_entrenament(entrenament):
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
            if row['tipus'] == 'Cardio':
                entrenaments.append(Cardio(row['nom'], row['descripcio'], row['exercicis'], row['distancia_km']))
            elif row['tipus'] == 'Forca':
                entrenaments.append(Forca(row['nom'], row['descripcio'], row['exercicis'], row['pes_kg']))
            else:
                entrenaments.append(Entrenament(row['nom'], row['descripcio'], row['exercicis']))
    return entrenaments





# --- Rutes Flask ---

@app.route('/')
def index():
    entrenaments = carregar_entrenaments()
    return render_template('index.html', entrenaments=entrenaments)

@app.route('/rutina', methods=['GET', 'POST'])
def rutina():
    if request.method == 'POST':
        tipus = request.form['tipus']
        nom = request.form['nom']
        descripcio = request.form['descripcio']
        exercicis = request.form['exercicis']
        if tipus == 'Cardio':
            distancia = request.form['distancia']
            entrenament = Cardio(nom, descripcio, exercicis, distancia)
        elif tipus == 'Forca':
            pes = request.form['pes']
            entrenament = Forca(nom, descripcio, exercicis, pes)
        else:
            entrenament = Entrenament(nom, descripcio, exercicis)
        guardar_entrenament(entrenament)
        return redirect(url_for('index'))
    return render_template('rutines.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
