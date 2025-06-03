from .entrenaments import Entrenament

# Classe Forca que hereta d'Entrenament
class Forca(Entrenament):
    def __init__(self, nom, descripcio, exercicis, pes_kg):
        super().__init__(nom, descripcio, exercicis)
        self.pes_kg = pes_kg  # atribut públic

    # Conversió a diccionari per a guardar en CSV
    def to_dict(self):
        d = super().to_dict()
        d['pes_kg'] = self.pes_kg
        return d

    def unitat(self):
        return "kg"