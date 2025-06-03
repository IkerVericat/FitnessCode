from .entrenaments import Entrenament


class Cardio(Entrenament):
    def __init__(self, nom, descripcio, exercicis, distancia_km, temps_minuts):
        super().__init__(nom, descripcio, exercicis)
        self.__distancia_km = distancia_km  # atribut privat
        self.__temps_minuts = temps_minuts  # atribut privat

    def to_dict(self):
        d = super().to_dict()
        d['distancia_km'] = self.__distancia_km
        d['temps_minuts'] = self.__temps_minuts
        return d

    def unitat(self):
        return "km i minuts"