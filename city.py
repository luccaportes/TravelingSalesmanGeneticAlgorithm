class City:
    def __init__(self, index, label, db):
        self.index = index
        self.label = label
        self.db = db

    def distance(self, city):
        return self.db.get_distance(self.index, city.index)

    def __repr__(self):
        return "(" + str(self.index) + ", " + str(self.label) + ")"