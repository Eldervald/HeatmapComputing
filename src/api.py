from src.settings import Settings
from src.database import Database
import matplotlib.pyplot as plt
from src.coordinate_system import CoordinateSystem
from src.probability import get_distribution_in_region, get_distribution_in_points
from PIL import Image
import numpy as np
from scipy import interpolate


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

            deviation_id = categoryDict['importanceLevel'] - 1
            if deviation_id < 0:
                print('No defined importance level of type : ' + category)
                continue

            orgs_coordinates = list()
            print('Organizations of type : ' + category)
            for org in detailed_orgs:
                longitude = org['coordinates']['longitude']
                latitude = org['coordinates']['latitude']
                coordinate = self.coordinate_system.to_cartesian_int(longitude=longitude, latitude=latitude)
                if coordinate is None:
                    continue
                orgs_coordinates.append(coordinate)
                print((coordinate.x, coordinate.y))

            orgs_probability_result_list.append(self.database.get_data_by_category_deviation(
                category, deviation_id, orgs_coordinates)
            )

        heatmap = get_distribution_in_region(get_distribution_in_points(orgs_probability_result_list), Settings.radius)
        # print(heatmap)

        plt.imshow(heatmap)
        plt.gca().invert_yaxis()
        plt.show()

        # plt.imshow(get_distribution_in_points(orgs_probability_result_list))
        # plt.gca().invert_yaxis()
        # plt.show()

        return self.interpolate_heatmap(heatmap)

    def interpolate_heatmap(self, heatmap):

        # xs = [i for i in range(Settings.data_shape[0])]
        # ys = [i for i in range(Settings.data_shape[1])]
        # f = interpolate.interp2d(xs, ys, heatmap, kind="cubic")
        #
        # xnew = np.linspace(0, np.round(abs(Settings.bottom_right_coordinate.longitude - Settings.top_left_coordinate.longitude)),
        #                    Settings.heatmap_shape[0])
        # ynew = np.linspace(0, np.round(abs(Settings.bottom_right_coordinate.latitude - Settings.top_left_coordinate.latitude)),
        #                    Settings.heatmap_shape[1])
        # 
        # result = f(xnew, ynew)

        result = list()

        for longitude in np.linspace(Settings.top_left_coordinate.longitude,
                                     Settings.bottom_right_coordinate.longitude,
                                     Settings.heatmap_shape[0]):
            for latitude in np.linspace(Settings.bottom_right_coordinate.latitude,
                                        Settings.top_left_coordinate.latitude,
                                        Settings.heatmap_shape[1]):
                point = self.coordinate_system.to_cartesian_int(longitude=longitude, latitude=latitude)
                if heatmap[point.x, point.y] < 0.0001:
                    continue
                result.append((longitude, latitude, np.power(heatmap[point.x, point.y], 0.3)))

        print(result)
        return result
