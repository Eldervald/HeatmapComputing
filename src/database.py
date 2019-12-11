from src.settings import Settings
from src.probability import intersect_distributions


class Database:
    data = dict()
    standart_deviation = Settings.standart_deviation

    def __init__(self):
        self.data = dict()
        self.standart_deviation = Settings.standart_deviation

    def get_data_by_category_deviation(self, category: str, deviation_id: int, objects):
        self.update_data_by_category_deviation(category, deviation_id, objects)
        return Database.data[(category, deviation_id)]

    def update_data_by_category_deviation(self, category: str, deviation_id: int, objects):
        if (category, deviation_id) not in self.data:
            self.data[(category, deviation_id)] = \
                intersect_distributions(Settings.data_shape,
                                        objects,
                                        self.standart_deviation[deviation_id])

    def is_empty(self):
        return len(self.data) == 0
