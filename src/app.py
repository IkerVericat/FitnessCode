import json
import csv
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
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
from datetime import datetime



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
    exercicis = carregar_exercicis()
    if request.method == 'POST':
        titol = request.form.get('titol', '').strip()
        exercicis_json = request.form.get('exercicis', '[]')
        try:
            exercicis_llista = json.loads(exercicis_json)
        except Exception:
            exercicis_llista = []
        if not titol:
            titol = 'Sense títol'
        # Desa la rutina al CSV
        if os.path.isfile('data/rutines.csv'):
            mode = 'a'
            write_header = False
        else:
            mode = 'w'
            write_header = True
        with open('data/rutines.csv', mode, encoding='utf-8', newline='') as f:
            fieldnames = ['titol', 'exercicis']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerow({'titol': titol, 'exercicis': json.dumps(exercicis_llista)})
        return redirect(url_for('index'))
    return render_template('crear_rutina.html', exercicis=exercicis)


@app.route('/rutina/<int:idx>', endpoint='rutina')
def mostrar_rutina(idx):
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

        # Actualitza les sèries de la rutina editada
        for i, exercici in enumerate(rutina['exercicis']):
            for j, serie in enumerate(exercici['series']):
                kg = request.form.get(f'kg_{i}_{j}', serie.get('kg', 0))
                reps = request.form.get(f'reps_{i}_{j}', serie.get('reps', 0))
                serie['kg'] = int(kg) if str(kg).strip() != '' else 0
                serie['reps'] = int(reps) if str(reps).strip() != '' else 0

        rutines[idx] = rutina

        # Guarda totes les rutines al CSV sense perdre els títols
        with open('data/rutines.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['titol', 'exercicis'])
            writer.writeheader()
            for r in rutines:
                titol = r['titol'] if 'titol' in r and r['titol'] else 'Sense títol'
                exercicis = r['exercicis'] if 'exercicis' in r else []
                writer.writerow({'titol': titol, 'exercicis': json.dumps(exercicis)})
        return redirect(url_for('rutina', idx=idx))
    return render_template('editar_rutina.html', rutina=rutina, idx=idx)


usuari = Usuari("Senyor/a", "señor@exemple.org")

@app.route('/registrar_entrenament/<int:idx>', methods=['GET', 'POST'])
def registrar_entrenament(idx):
    rutines = carregar_entrenaments()
    if idx < 0 or idx >= len(rutines):
        return redirect(url_for('index'))
    rutina = rutines[idx]
    if request.method == 'POST':
        realitzades = []
        for i, exercici in enumerate(rutina['exercicis']):
            if exercici.get('muscul') == 'cardiovascular':
                distancia_km = request.form.get(f'distancia_km_{i}', '')
                temps_minuts = request.form.get(f'temps_minuts_{i}', '')
                realitzades.append({
                    'nom': exercici['nom'],
                    'muscul': exercici['muscul'],
                    'imatge': exercici.get('imatge', ''),
                    'distancia_km': distancia_km,
                    'temps_minuts': temps_minuts
                })
            else:
                ex_realitzat = {'nom': exercici['nom'], 'series': []}
                for j, serie in enumerate(exercici.get('series', [])):
                    kg = request.form.get(f'kg_{i}_{j}', '')
                    reps = request.form.get(f'reps_{i}_{j}', '')
                    completada = request.form.get(f'completada_{i}_{j}') == 'on'
                    ex_realitzat['series'].append({
                        'kg': kg,
                        'reps': reps,
                        'completada': completada
                    })
                realitzades.append(ex_realitzat)
        titol = rutina.get('titol', 'Sense títol')
        data_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('data/progressos.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([data_hora, titol, json.dumps(realitzades)])
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
    import csv, json
    progressos = []
    with open('data/progressos.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                data_hora, titol, realitzades = row
                realitzades = json.loads(realitzades)
                for ex in realitzades:
                    if ex.get('muscul') == 'cardiovascular':
                        progressos.append({
                            'data': data_hora,
                            'rutina': titol,
                            'exercici': ex['nom'],
                            'distancia_km': ex.get('distancia_km', ''),
                            'temps_minuts': ex.get('temps_minuts', '')
                        })
                    else:
                        for serie in ex.get('series', []):
                            progressos.append({
                                'data': data_hora,
                                'rutina': titol,
                                'exercici': ex['nom'],
                                'kg': serie.get('kg', ''),
                                'reps': serie.get('reps', '')
                            })
            except Exception:
                continue
    # Agrupa per rutina per a les gràfiques
    rutines_grafiques = {}
    with open('data/progressos.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                data_hora, titol, realitzades = row
                realitzades = json.loads(realitzades)
                if titol not in rutines_grafiques:
                    rutines_grafiques[titol] = []
                if realitzades:
                    ex = realitzades[0]
                    pes = 0
                    for s in ex['series']:
                        try:
                            pes = max(pes, float(s['kg']) if s['kg'] else 0)
                        except:
                            pass
                    rutines_grafiques[titol].append(pes)
            except Exception:
                continue

    # Genera una gràfica per cada rutina amb dades
    grafiques = {}
    for rutina, pesos in rutines_grafiques.items():
        if not pesos:
            continue
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.plot(range(1, len(pesos)+1), pesos, marker='o', color='#ffc107')
        ax.set_title(f'Evolució {rutina}', color='#ffc107')
        ax.set_xlabel('Sessió')
        ax.set_ylabel('Kg')
        ax.set_facecolor('#222')
        fig.patch.set_facecolor('#181818')
        ax.tick_params(colors='#fff')
        ax.spines['bottom'].set_color('#ffc107')
        ax.spines['left'].set_color('#ffc107')
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png', transparent=True)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close(fig)
        grafiques[rutina] = img_base64

    return render_template('progressos.html', progressos=progressos, grafiques=grafiques, usuari=usuari)

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

@app.route('/pujar_media/<int:idx>/<int:exercici>', methods=['POST'])
def pujar_media(idx, exercici):
    rutina = carregar_rutina(idx)
    fitxer = request.files.get('media')
    if fitxer and fitxer.filename:
        nom_fitxer = f"{rutina['titol']}_{exercici}_{fitxer.filename}"
        ruta = os.path.join('static', 'media', nom_fitxer)
        fitxer.save(ruta)
        if 'media' not in rutina['exercicis'][exercici]:
            rutina['exercicis'][exercici]['media'] = []
        rutina['exercicis'][exercici]['media'].append(nom_fitxer)
        # Desa la rutina actualitzada
        # Carrega totes les rutines
        rutines = []
        if os.path.isfile('data/rutines.csv'):
            with open('data/rutines.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rutines.append({
                        'titol': row.get('titol', 'Sense títol'),
                        'exercicis': json.loads(row.get('exercicis', '[]'))
                    })
        # Actualitza la rutina corresponent
        rutines[idx] = rutina
        with open('data/rutines.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['titol', 'exercicis'])
            writer.writeheader()
            for r in rutines:
                writer.writerow({'titol': r['titol'], 'exercicis': json.dumps(r['exercicis'])})
        flash('Fitxer pujat correctament!', 'success')
    else:
        flash('No s\'ha seleccionat cap fitxer.', 'danger')
    return redirect(url_for('rutina', idx=idx))


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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
