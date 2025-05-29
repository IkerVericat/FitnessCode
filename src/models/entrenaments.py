import json

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
            'exercicis': json.dumps(self.exercicis)
        }
    
    # Mètode per a obtenir la unitat de mesura
    def unitat(self):
        return "unitats"