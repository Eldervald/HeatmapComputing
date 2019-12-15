from src.settings import Settings
from src.database import Database
import matplotlib.pyplot as plt
from src.coordinate_system import CoordinateSystem
from src.probability import get_distribution_in_region, get_distribution_in_points
from PIL import Image
import numpy as np


# DATA_SHAPE = (200, 200)
# TOP_LEFT_COORDINATE = (53.610826, 23.777779)
# BOTTOM_RIGHT_COORDINATE = (53.718562, 23.864186)
# HEATMAP_SHAPE = (30, 30)
# STANDART_DEVIATION = [25, 15, 5, 0]
# RADIUS = 5
# IMG_PATH = "../BlackRealtors/BlackRealtors/wwwroot/images/final_map.png"

class MapGenerator:
    def __init__(self):
        self.coordinate_system = CoordinateSystem(shape=Settings.data_shape,
                                                  top_left=Settings.top_left_coordinate,
                                                  bottom_right=Settings.bottom_right_coordinate)
        self.database = Database()

    def calculate_map(self, data):
        orgs_probability_result_list = list()

        all_objects = data["coordinatesImportance"]

        for categoryDict in all_objects:
            category = str(categoryDict['organizationType'])
            detailed_orgs = categoryDict['organizations']

            if detailed_orgs is None:
                print('No organizations of type : ' + category)
                continue

            deviation_id = categoryDict['importanceLevel']
            if deviation_id == 0:
                print('No defined importance level of type : ' + category)
                continue

            orgs_coordinates = list()
            print('Organizations of type : ' + category)
            for org in detailed_orgs:
                longitude = org['coordinates']['longitude']
                latitude = org['coordinates']['latitude']
                coordinate = self.coordinate_system.to_cartesian(longitude=longitude, latitude=latitude)
                orgs_coordinates.append(coordinate)
                print(coordinate)

            orgs_probability_result_list.append(self.database.get_data_by_category_deviation(
                category, deviation_id, orgs_coordinates)
            )

        heatmap = get_distribution_in_region(get_distribution_in_points(orgs_probability_result_list), Settings.radius)

        plt.imshow(heatmap)
        plt.show()

        result = list()
        for longitude in np.linspace(Settings.top_left_coordinate.longitude,
                             Settings.bottom_right_coordinate.longitude,
                             Settings.heatmap_shape[0]):
            for latitude in np.linspace(Settings.top_left_coordinate.latitude,
                                 Settings.bottom_right_coordinate.latitude,
                                 Settings.heatmap_shape[1]):
                i, j = self.coordinate_system.to_cartesian(longitude=longitude, latitude=latitude)
                # print(heatmap[i, j], i, j)
                result.append((longitude, latitude, np.power(heatmap[i, j], 0.3)))
        return result
