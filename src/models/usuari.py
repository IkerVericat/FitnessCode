class Usuari:
    def __init__(self, nom, email):
        self.nom = nom
        self.email = email
        self.progressos = []
        

    def to_dict(self):
        return {
            'nom': self.nom,
            'email': self.email,
            'progressos': [progres.to_dict() for progres in self.progressos]
        }

    def afegir_progres(self, data, rutina, exercici, kg, reps):
        self.progressos.append({
            'data': data,
            'rutina': rutina,
            'exercici': exercici,
            'kg': kg,
            'reps': reps
        })

    def guardar_progressos_csv(self, filepath):
        import csv
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['data', 'rutina', 'exercici', 'kg', 'reps'])
            writer.writeheader()
            for p in self.progressos:
                writer.writerow(p)