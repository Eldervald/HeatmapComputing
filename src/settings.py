from src.coordinate_system import Coordinate

class Settings:
    data_shape = (200, 200)
    top_left_coordinate = Coordinate(latitude=23.712759, longitude=53.760859)
    bottom_right_coordinate = Coordinate(latitude=23.977118, longitude=53.600244)
    heatmap_shape = (30, 30)
    standart_deviation = [25, 15, 5, 0]
    radius = 5
    img_path = "../BlackRealtors/BlackRealtors/wwwroot/images/final_map.png"