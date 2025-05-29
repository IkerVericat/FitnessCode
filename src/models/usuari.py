class Usuari:
    def __init__(self, nom, email):
        self.nom = nom
        self.email = email
        self.rutines = []
        

    def to_dict(self):
        return {
            'nom': self.nom,
            'email': self.email,
            'rutines': [rutina.to_dict() for rutina in self.rutines]
        }