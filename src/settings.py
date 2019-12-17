from src.coordinate_system import Coordinate


class Settings:
    data_shape = (200, 200)
    top_left_coordinate = Coordinate(longitude=23.712759, latitude=53.760859)
    bottom_right_coordinate = Coordinate(longitude=23.977118, latitude=53.600244)
    heatmap_shape = (200, 200)
    standart_deviation = [10, 5, 2, 0]
    radius = 10
    img_path = "../BlackRealtors/BlackRealtors/wwwroot/images/final_map.png"