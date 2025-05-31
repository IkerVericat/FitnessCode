import json
import csv
import os
from flask import Flask, render_template, request, redirect, url_for
from models.entrenaments import Entrenament
from models.forca import Forca
from models.cardio import Cardio
from models.usuari import Usuari
from utils.csv_utils import eliminar_entrenament_csv, guardar_entrenament, carregar_entrenaments, carregar_exercicis, eliminar_rutina_csv


app = Flask(__name__)


# --- Rutes Flask ---

@app.route('/')
def index():
    rutines = []
    if os.path.isfile('data/rutines.csv'):
        with open('data/rutines.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rutines.append({
                    'titol': row['titol'],
                    'exercicis': json.loads(row['exercicis'])
                })
    return render_template('index.html', rutines=rutines, exercicis=carregar_exercicis())


@app.route('/entrenaments', methods=['GET', 'POST'])
def entrenaments():
    if request.method == 'POST':
        tipus = request.form['tipus']
        nom = request.form['nom']
        descripcio = request.form['descripcio']
        exercicis = request.form['exercicis']
        try:
            exercicis = json.loads(exercicis)
        except Exception:
            pass
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
    exercicis = carregar_exercicis()
    return render_template('entrenament.html', exercicis=exercicis)


@app.route('/crear_rutina', methods=['GET', 'POST'])
def crear_rutina():
    if request.method == 'POST':
        titol = request.form['titol']
        exercicis = json.loads(request.form['exercicis'])
        # Desa la rutina al CSV
        with open('data/rutines.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['titol', 'exercicis'])
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow({'titol': titol, 'exercicis': json.dumps(exercicis)})
        return redirect(url_for('index'))
    return render_template('crear_rutina.html', exercicis=carregar_exercicis())


@app.route('/rutina/<int:idx>')
def detall_rutina(idx):
    rutines = []
    if os.path.isfile('data/rutines.csv'):
        with open('data/rutines.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rutines.append({
                    'titol': row['titol'],
                    'exercicis': json.loads(row['exercicis'])
                })
    rutina = rutines[idx]
    return render_template('rutina.html', rutina=rutina)



# --- Usuari i els seus progresos ---

usuari = Usuari("Iker", "ikervericat@iesmontsia.org")

@app.route('/afegir_progres', methods=['POST'])
def afegir_progres():
    data = request.form['data']
    rutina = request.form['rutina']
    exercici = request.form['exercici']
    kg = request.form['kg']
    reps = request.form['reps']
    usuari.afegir_progres(data, rutina, exercici, kg, reps)
    usuari.guardar_progressos_csv('data/progresos_usuari.csv')
    return redirect(url_for('index'))

@app.route('/progressos')
def veure_progressos():
    return render_template('progressos.html', progressos=usuari.progressos, usuari=usuari)

@app.route('/eliminar_entrenament', methods=['POST'])
def eliminar_entrenament():
    data = request.form['data']
    rutina = request.form['rutina']
    exercici = request.form['exercici']
    eliminar_entrenament_csv(data, rutina, exercici)
    return redirect(url_for('progresos'))

@app.route('/eliminar_rutina', methods=['POST'])
def eliminar_rutina():
    titol = request.form['titol']
    eliminar_rutina_csv(titol)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
