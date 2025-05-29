import json
from flask import Flask, render_template, request, redirect, url_for
from models.entrenaments import Entrenament
from models.forca import Forca
from models.cardio import Cardio
from utils.csv_utils import guardar_entrenament, carregar_entrenaments, carregar_exercicis


app = Flask(__name__)


# --- Rutes Flask ---

@app.route('/')
def index():
    entrenaments = carregar_entrenaments()
    return render_template('index.html', entrenaments=entrenaments)


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


@app.route('/nova_rutina', methods=['GET', 'POST'])
def nova_rutina():
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
    return render_template('crear_rutina.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
