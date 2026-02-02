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

def main():
    eel.start('index.html', size=(1200, 800))


if __name__ == '__main__':
    main()
