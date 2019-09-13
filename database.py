from collections import defaultdict
from itertools import combinations

class DataBase:
    def __init__(self, path):
        self.path = path
        self.list_cities, self.dict_distances = self.load_data()
        self.complete_graph()

    def load_data(self):
        list_cities = []
        dict_distances = defaultdict(dict)
        with open(self.path) as f:
            lines = f.read().splitlines()
            parsing_distances = False
            for i in lines:
                if len(i) == 0 or i[0] == "#":
                    continue
                list_line = i.split(",")
                if len(list_line) == 2 and not parsing_distances:
                    list_cities.append((list_line[0], list_line[1]))
                elif len(list_line) == 3:
                    parsing_distances = True
                    id_orig = list_line[0]
                    id_dest = list_line[1]
                    cost = float(list_line[2])
                    dict_distances[id_orig][id_dest] = cost
                    dict_distances[id_dest][id_orig] = cost
                else:
                    raise ValueError("Incorrect format")
        return list_cities, dict_distances

    def complete_graph(self):
        list_ids = [i[0] for i in self.list_cities]
        values = [list(i.values()) for i in self.dict_distances.values()]
        values = [item for sublist in values for item in sublist]
        max_value = max(values)
        combs = combinations(list_ids, 2)
        for x, y in combs:
            if y not in self.dict_distances[x]:
                self.dict_distances[x][y] = max_value * 100
                self.dict_distances[y][x] = max_value * 100

    def get_distance(self, x, y):
        if x == y:
            return -1
        return self.dict_distances[x][y]

    def get_cities(self):
        return self.list_cities









