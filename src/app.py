import json
import csv
import os
from flask import Flask, render_template, request, redirect, url_for, session
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from models.entrenaments import Entrenament
from models.forca import Forca
from models.cardio import Cardio
from models.usuari import Usuari
from utils.csv_utils import editar_rutina_csv, eliminar_entrenament_csv, guardar_entrenament, carregar_entrenaments, carregar_exercicis, eliminar_rutina_csv

app = Flask(__name__)
app.secret_key = 'daw2025'

# --- Rutes Flask ---

@app.route('/')
def index():
    rutines = []
    if os.path.isfile('data/rutines.csv'):
        with open('data/rutines.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rutines.append({
                    'titol': row.get('titol', 'Sense títol'),
                    'exercicis': json.loads(row.get('exercicis', '[]'))
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
                    'titol': row.get('titol', 'Sense títol'),
                    'exercicis': json.loads(row.get('exercicis', '[]'))
                })
    rutina = rutines[idx]
    return render_template('rutina.html', rutina=rutina, idx=idx)

@app.route('/editar_rutina/<int:idx>', methods=['GET', 'POST'])
def editar_rutina(idx):
    rutines = carregar_entrenaments()
    if idx < 0 or idx >= len(rutines):
        return redirect(url_for('index'))
    rutina = rutines[idx]
    if request.method == 'POST':
        nou_titol = request.form.get('titol', '').strip()
        if not nou_titol:
            nou_titol = 'Sense títol'
        rutina['titol'] = nou_titol
        rutines[idx] = rutina

        # Abans de guardar, assegura't que totes tenen titol
        for r in rutines:
            if 'titol' not in r or not r['titol']:
                r['titol'] = 'Sense títol'

        # Actualitza les sèries
        for i, exercici in enumerate(rutina['exercicis']):
            for j, serie in enumerate(exercici['series']):
                kg = request.form.get(f'kg_{i}_{j}', serie['kg'])
                reps = request.form.get(f'reps_{i}_{j}', serie['reps'])
                serie['kg'] = int(kg) if str(kg).strip() != '' else 0
                serie['reps'] = int(reps) if str(reps).strip() != '' else 0

        rutines[idx] = rutina
        # Guarda totes les rutines al CSV
        with open('data/rutines.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['titol', 'exercicis'])
            writer.writeheader()
            for r in rutines:
                titol = r.get('titol', 'Sense títol')
                exercicis = r.get('exercicis', [])
                writer.writerow({'titol': titol, 'exercicis': json.dumps(exercicis)})
        return redirect(url_for('detall_rutina', idx=idx))
    return render_template('editar_rutina.html', rutina=rutina, idx=idx)


usuari = Usuari("Iker", "ikervericat@iesmontsia.org")

@app.route('/registrar_entrenament/<int:idx>', methods=['GET', 'POST'])
def registrar_entrenament(idx):
    rutines = carregar_entrenaments()
    if idx < 0 or idx >= len(rutines):
        return redirect(url_for('index'))
    rutina = rutines[idx]
    if request.method == 'POST':
        realitzades = []
        for i, exercici in enumerate(rutina['exercicis']):
            ex_realitzat = {'nom': exercici['nom'], 'series': []}
            for j, serie in enumerate(exercici['series']):
                kg = request.form.get(f'kg_{i}_{j}', '')
                reps = request.form.get(f'reps_{i}_{j}', '')
                completada = request.form.get(f'completada_{i}_{j}') == 'on'
                ex_realitzat['series'].append({
                    'kg': kg,
                    'reps': reps,
                    'completada': completada
                })
                rutina['exercicis'][i]['series'][j]['kg'] = kg
                rutina['exercicis'][i]['series'][j]['reps'] = reps
            realitzades.append(ex_realitzat)
        # Desa les dades a progressos.csv
        titol = rutina.get('titol', 'Sense títol')
        with open('data/progressos.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([idx, titol, json.dumps(realitzades)])
        # Desa la rutina actualitzada a rutines.csv
        rutines[idx] = rutina
        with open('data/rutines.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['titol', 'exercicis'])
            writer.writeheader()
            for r in rutines:
                titol = r.get('titol', 'Sense títol')
                exercicis = r.get('exercicis', [])
                writer.writerow({'titol': titol, 'exercicis': json.dumps(exercicis)})
        session['ultim_entrenament'] = realitzades
        return redirect(url_for('progressos'))
    return render_template('entrenament.html', rutina=rutina, idx=idx)

@app.route('/progressos')
def progressos():
    progressos = []
    with open('data/progressos.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                idx, titol, realitzades = row
                realitzades = json.loads(realitzades)
                data = {'rutina': titol, 'exercicis': realitzades}
                progressos.append(data)
            except Exception:
                continue

    # Exemple: mostra l'evolució del primer exercici de la primera rutina
    dates = []
    pesos = []
    if progressos:
        for i, prog in enumerate(progressos):
            if prog['exercicis']:
                ex = prog['exercicis'][0]  # Primer exercici
                pes = 0
                for s in ex['series']:
                    try:
                        pes = max(pes, float(s['kg']) if s['kg'] else 0)
                    except:
                        pass
                pesos.append(pes)
                dates.append(f"Entrenament {i+1}")

    # Genera la gràfica
    fig, ax = plt.subplots(figsize=(7, 4))
    if pesos:
        ax.plot(dates, pesos, marker='o', color='#ffc107')
        ax.set_title('Evolució del pes màxim (primer exercici)', color='#ffc107')
        ax.set_xlabel('Sessió')
        ax.set_ylabel('Kg')
        ax.set_facecolor('#222')
        fig.patch.set_facecolor('#181818')
        ax.tick_params(colors='#fff')
        ax.spines['bottom'].set_color('#ffc107')
        ax.spines['left'].set_color('#ffc107')
    else:
        ax.text(0.5, 0.5, 'Encara no hi ha dades!', ha='center', va='center', color='#fff', fontsize=16)
        ax.axis('off')
        fig.patch.set_facecolor('#181818')

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', transparent=True)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    # Passa també la taula de progressos si vols
    return render_template('progressos.html', img_base64=img_base64, usuari=usuari, progressos=usuari.progressos)

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

@app.route('/eliminar_entrenament', methods=['POST'])
def eliminar_entrenament():
    data = request.form['data']
    rutina = request.form['rutina']
    exercici = request.form['exercici']
    eliminar_entrenament_csv(data, rutina, exercici)
    return redirect(url_for('progressos'))

@app.route('/eliminar_rutina', methods=['POST'])
def eliminar_rutina():
    titol = request.form['titol']
    eliminar_rutina_csv(titol)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
