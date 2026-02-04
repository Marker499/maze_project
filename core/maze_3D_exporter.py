from .maze_generator import EllerMazeGenerator
import numpy as np
import struct


class Maze3DExporter:
    def __init__(self,
                 maze_generator: EllerMazeGenerator,
                 cell_size:float=10,
                 wall_height:float=5,
                 wall_thickness:float=1,
                 floor_thickness:float=1):
        self.maze_generator = maze_generator
        self.cell_size = cell_size
        self.wall_height = wall_height
        self.wall_thickness = wall_thickness
        self.floor_thickness = floor_thickness

        self.vertices = []
        self.faces = []
        self.vertex_dict = {}

    def _add_vertex(self,
                    x:float, y:float, z:float):
        '''Создание вершины'''
        vertex = (x, y, z)
        if vertex not in self.vertex_dict:
            self.vertex_dict[vertex] = len(self.vertices)
            self.vertices.append(vertex)
        return self.vertex_dict[vertex]

    def _add_face(self, v1: int, v2: int, v3: int, v4: int = None):
        '''Создание 1 грани, 1 грань - 2 треугольника'''
        if v4 is None:
            self.faces.append((v1, v2, v3))
        else:
            self.faces.append((v1, v2, v3))
            self.faces.append((v1, v3, v4))

    def _create_cube(self,
                    x:float, y:float, z:float,
                     width:float, height:float, depth:float):
        '''Создание элемента(параллелепипеда) - каждый параллелепипед имеет 8 вершин и 6 граней '''
        v0 = self._add_vertex(x, y, z)
        v1 = self._add_vertex(x + width, y, z)
        v2 = self._add_vertex(x + width, y + depth, z)
        v3 = self._add_vertex(x, y + depth, z)
        v4 = self._add_vertex(x, y, z + height)
        v5 = self._add_vertex(x + width, y, z + height)
        v6 = self._add_vertex(x + width, y + depth, z + height)
        v7 = self._add_vertex(x, y + depth, z + height)

        self._add_face(v0, v3, v2, v1)
        self._add_face(v0, v4, v7, v3)
        self._add_face(v0, v1, v5, v4)
        self._add_face(v1, v2, v6, v5)
        self._add_face(v2, v3, v7, v6)
        self._add_face(v4, v5, v6, v7)


    def _create_floor(self):
        '''Создания пола'''
        total_width = self.maze_generator.width * self.cell_size
        total_height = self.maze_generator.height * self.cell_size
        self._create_cube(0,0,0, total_width, self.floor_thickness, total_height)

    def _create_vertical_wall(self, row: int, col: int, is_present: bool):
        '''Создание вертикальной стены'''
        if not is_present:
            return
        x = col * self.cell_size - self.wall_thickness / 2
        y = row * self.cell_size
        z = 0
        self._create_cube(x, y, z, self.wall_thickness, self.wall_height, self.cell_size)

    def _create_horizontal_wall(self, row: int, col: int, is_present: bool):
        '''Создание горизонтальной стены'''
        if not is_present:
            return
        x = col * self.cell_size
        y = row * self.cell_size - self.wall_thickness / 2
        z = 0
        self._create_cube(x, y, z, self.cell_size, self.wall_height, self.wall_thickness)

    def generate_3D_model(self):
        '''Генерация 3Д модели'''
        self.vertices = []
        self.faces = []
        self.vertex_dict = {}
        self._create_floor()

        for row in range(self.maze_generator.height):
            for col in range(self.maze_generator.width + 1):
                is_present = self.maze_generator.vertical_walls[row][col] == 1
                self._create_vertical_wall(row, col, is_present)

        for row in range(self.maze_generator.height + 1):
            for col in range(self.maze_generator.width):
                is_present = self.maze_generator.horizontal_walls[row][col] == 1
                self._create_horizontal_wall(row, col, is_present)

    def _export_to_stl_ascii(self, file_name:str):
        '''Экспорт в текстовый stl (чтобы мы могли его прочитать)'''
        with open(file_name, 'w') as f:
            f.write('solid maze_3D\n')
            for face in self.faces:
                v1, v2, v3 = face

                p1 = np.array(self.vertices[v1])
                p2 = np.array(self.vertices[v2])
                p3 = np.array(self.vertices[v3])

                normal = np.cross(p2 - p1, p3 - p1)
                normal = normal / np.linalg.norm(normal)
                if np.isnan(normal).any():
                    normal = np.array([0.0, 0.0, 1.0])
                f.write(f'  facet normal {normal[0]} {normal[1]} {normal[2]}\n')
                f.write('    outer loop\n')
                for v_i in face:
                    vertex = self.vertices[v_i]
                    f.write(f'      vertex {vertex[0]} {vertex[1]} {vertex[2]}\n')
                f.write('    endloop\n')
                f.write('  endfacet\n')
            f.write('endsolid maze_3D\n')

    def _export_to_stl_binary(self, file_name: str):
        '''Экспорт в цифровой stl (чтобы он весил меньше)'''
        with open(file_name, 'wb') as f:
            header = b'3D Maze Model' + b' ' * 67
            f.write(header)

            num_faces = len(self.faces)
            f.write(struct.pack('<I', num_faces))
            for face in self.faces:
                v1, v2, v3 = face

                p1 = np.array(self.vertices[v1])
                p2 = np.array(self.vertices[v2])
                p3 = np.array(self.vertices[v3])

                normal = np.cross(p2 - p1, p3 - p1)
                normal = normal / np.linalg.norm(normal)
                if np.isnan(normal).any():
                    normal = np.array([0.0, 0.0, 1.0])
                f.write(struct.pack('<fff', *normal))
                for v_i in face:
                    vertex = self.vertices[v_i]
                    f.write(struct.pack('<fff', *vertex))
                f.write(struct.pack('<H', 0))


    def export_to_stl(self, file_name:str, is_ascii: bool = True):
        '''Общий экспорт в stl'''
        if is_ascii:
            self._export_to_stl_ascii(file_name)
        else:
            self._export_to_stl_binary(file_name)




