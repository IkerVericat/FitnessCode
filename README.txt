Guardar codi Github

Avans de modificar el codi realitzar un "git pull origin main" ⚠️‼️

git status
git add .  |  git add nom_arxiu
git commit -m "comentari"
git push

# Com he estructurat aquest programa

=== app.py ===

- Conté el punt d'entrada de la aplicació Flask
- Té definides les rutes @app.route i la configuració principal.
- Importa les classes i les funcions d'altres fitxers



/models

/entrenament.py

- Defineix la classe base Entrenament.
- Potser també la classe Usuari si vols tenir-la aquí (o en un fitxer separat).


/cardio.py

Defineix la classe Cardio que hereta de Entrenament


/forca.py

Defineix la classe Forca que hereta de Entrenament


/usuari.py
Defineix la classe Usuari


/utils/csv_utils.py
Funcions per guardar i carregar rutines/progressos des de fitxers CSV.
(guardar_entrenament, carregar_entrenaments, etc)
