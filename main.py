import time
from core import EllerMazeGenerator, Maze3DExporter
import eel
#
# maze_generator = EllerMazeGenerator(10, 10, 10)
# horizontal, vertical = maze_generator.generate()
# print("Горизонтальные стены (1 - есть стена, 0 - нет стены):")
# for i, row in enumerate(horizontal):
#     print(f"Строка {i}: {row}")
#
# print("Вертикальные стены (1 - есть стена, 0 - нет стены):")
# for i, row in enumerate(vertical):
#     print(f"Строка {i}: {row}")
#
# maze_generator.print_maze()
# exporter = Maze3DExporter(maze_generator, 10, 8, 2, 2)
# exporter.generate_3D_model()
# exporter.export_to_stl('7.stl', True)
eel.init('web')

maze_generator = None
exporter = None

@eel.expose
def generate(width: int, height: int, seed: int):
    global maze_generator
    maze_generator = EllerMazeGenerator(width, height, seed)
    maze_generator.generate()
    return maze_generator.get_maze_matrix()



@eel.expose
def export_to_stl(
        file_name: str, 
        cell_size: float = 10,
        wall_height: float = 5,
        wall_thickness: float = 1,
        floor_thickness: float = 1,
        is_ascii: bool = False
    ):
    global maze_generator, exporter
    if maze_generator is None:
        return False
    if len(file_name) == 0:
        file_name = f"maze_{round(time.time())}.stl"
    
    exporter = Maze3DExporter(maze_generator, cell_size, wall_height, wall_thickness, floor_thickness)
    exporter.generate_3D_model()
    exporter.export_to_stl(file_name, is_ascii)
    return True


def main():
    eel.start('index.html', size=(1200, 800))


if __name__ == '__main__':
    main()
