from .entrenaments import Entrenament

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