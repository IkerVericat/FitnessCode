from .entrenaments import Entrenament


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