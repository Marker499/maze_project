import random
from typing import List, Tuple


class EllerMazeGenerator:
    """Класс для генерации лабиринтов методом Эллера"""
    def __init__(self, width: int, height: int, seed: int = None):
        if width <= 1 or height <= 1:
            raise ValueError("Лабиринт должен быть хотя бы 2 на 2")
        self.width = width
        self.height = height

        if seed is not None:
            random.seed(seed)

        self.horizontal_walls = [[1] * width for _ in range(height + 1)]
        self.vertical_walls = [[1] * (width + 1) for _ in range(height)]

        self.entrance = (0, 0)
        self.exit = (width - 1, height - 1)

        self._set_borders()

    def _create_entrance_and_exit(self):
        entrance_col = self.entrance[1]
        self.horizontal_walls[0][entrance_col] = 0

        exit_col = self.exit[1]
        self.horizontal_walls[self.height][exit_col] = 0

    def _set_borders(self):
        """Устанавливает границы лабиринта."""
        # Верхняя и нижняя границы
        for col in range(self.width):
            self.horizontal_walls[0][col] = 1  # Верхняя граница
            self.horizontal_walls[self.height][col] = 1  # Нижняя граница

        # Левая и правая границы
        for row in range(self.height):
            self.vertical_walls[row][0] = 1  # Левая граница
            self.vertical_walls[row][self.width] = 1  # Правая граница

    def generate(self) -> Tuple[List[List[int]], List[List[int]]]:
        """
        Генерирует лабиринт с использованием алгоритма Эллера.

        Returns:
            Кортеж из двух матриц: горизонтальные стены и вертикальные стены
        """
        row_sets = self._init_sets()

        for row in range(self.height):
            # Шаг 1: Присваиваем множества
            row_sets = self._assign_sets(row_sets)

            # Шаг 2: Объединяем ячейки в строке
            row_sets, vertical_walls_to_remove = self._merge_adjacent_cells(row_sets, row)

            # Шаг 3: Добавляем вертикальные соединения
            horizontal_walls_to_remove = self._add_vertical_connections(row_sets, row)

            # Шаг 4: Удаляем стены
            self._remove_walls(vertical_walls_to_remove, horizontal_walls_to_remove)

            # Шаг 5: Подготавливаем множества для следующей строки
            row_sets = self._create_next_row_sets(row_sets, row)

            # Шаг 6: Для последней строки - обязательное объединение
            if row == self.height - 1:
                self._finalize_last_row(row_sets, row)

        self._create_entrance_and_exit()

        return self.horizontal_walls, self.vertical_walls

    def _init_sets(self) -> List[int]:
        return [-1] * self.width

    def _assign_sets(self, row_sets: List[int]) -> List[int]:
        for col in range(self.width):
            if row_sets[col] == -1:
                # Находим максимальное множество и назначаем следующее
                max_set = max(row_sets) if max(row_sets) >= 0 else 0
                row_sets[col] = max_set + 1
        return row_sets

    def _merge_adjacent_cells(self, row_sets: List[int], row: int) -> Tuple[List[int], List[List[int]]]:
        """
        Объединяет соседние ячейки в строке с вероятностью.

        Args:
            row_sets: Текущие множества строки
            row: Номер текущей строки

        Returns:
            Кортеж (обновленные множества, вертикальные стены для удаления)
        """
        walls_to_remove = []

        for col in range(self.width - 1):
            # Если ячейки в разных множествах, возможно объединение
            if row_sets[col] != row_sets[col + 1]:
                if random.random() > 0.5:  # 50% вероятность объединения
                    # Объединяем множества
                    old_set = row_sets[col + 1]
                    new_set = row_sets[col]

                    for i in range(self.width):
                        if row_sets[i] == old_set:
                            row_sets[i] = new_set

                    # Убираем вертикальную стену
                    walls_to_remove.append([row, col + 1])

        return row_sets, walls_to_remove

    def _add_vertical_connections(self, row_sets: List[int], row: int) -> List[List[int]]:
        """
        Добавляет вертикальные соединения между строками.

        Args:
            row_sets: Множества текущей строки
            row: Номер текущей строки

        Returns:
            Список горизонтальных стен для удаления
        """
        if row == self.height - 1:
            return []  # Для последней строки не добавляем

        walls_to_remove = []

        # Создаем словарь для отслеживания, был ли уже переход из каждого множества
        set_has_connection = {}

        for col in range(self.width):
            current_set = row_sets[col]

            # Если для этого множества еще не было соединения, создаем его с вероятностью
            if current_set not in set_has_connection:
                set_has_connection[current_set] = False

            # Решаем, создавать ли вертикальное соединение
            if not set_has_connection[current_set] or random.random() > 0.3:
                walls_to_remove.append([row + 1, col])
                set_has_connection[current_set] = True

        return walls_to_remove

    def _create_next_row_sets(self, row_sets: List[int], row: int) -> List[int]:
        """
        Создает множества для следующей строки на основе текущей.

        Args:
            row_sets: Множества текущей строки
            row: Номер текущей строки

        Returns:
            Множества для следующей строки
        """
        if row == self.height - 1:
            return row_sets  # Для последней строки просто возвращаем

        next_row_sets = [-1] * self.width

        for col in range(self.width):
            # Если есть вертикальное соединение, сохраняем множество
            if self.horizontal_walls[row + 1][col] == 0:
                next_row_sets[col] = row_sets[col]

        return next_row_sets

    def _finalize_last_row(self, row_sets: List[int], row: int):
        """
        Завершающая обработка последней строки.

        Args:
            row_sets: Множества последней строки
            row: Номер строки (последней)
        """
        # Объединяем все соседние ячейки из разных множеств
        for col in range(self.width - 1):
            if row_sets[col] != row_sets[col + 1]:
                # Убираем вертикальную стену
                self.vertical_walls[row][col + 1] = 0

                # Объединяем множества
                old_set = row_sets[col + 1]
                new_set = row_sets[col]

                for i in range(self.width):
                    if row_sets[i] == old_set:
                        row_sets[i] = new_set

    def _remove_walls(self, vertical_walls: List[List[int]], horizontal_walls: List[List[int]]):
        """
        Удаляет стены на основе списков стен для удаления.

        Args:
            vertical_walls: Список вертикальных стен для удаления
            horizontal_walls: Список горизонтальных стен для удаления
        """
        # Удаляем вертикальные стены
        for wall in vertical_walls:
            row, col = wall
            self.vertical_walls[row][col] = 0

        # Удаляем горизонтальные стены
        for wall in horizontal_walls:
            row, col = wall
            self.horizontal_walls[row][col] = 0

    def get_maze_matrix(self) -> List[List[int]]:
        """
        Возвращает единую матрицу лабиринта для визуализации.
        Значения: 0 - проход, 1 - стена.
        """
        # Создаем матрицу большего размера для учета стен
        maze_width = self.width * 2 + 1
        maze_height = self.height * 2 + 1
        maze = [[1] * maze_width for _ in range(maze_height)]

        # Заполняем проходы
        for row in range(self.height):
            for col in range(self.width):
                # Ячейка лабиринта (проход)
                maze[row * 2 + 1][col * 2 + 1] = 0

                # Проверяем горизонтальные стены справа
                if col < self.width - 1 and self.vertical_walls[row][col + 1] == 0:
                    maze[row * 2 + 1][col * 2 + 2] = 0

                # Проверяем вертикальные стены снизу
                if row < self.height - 1 and self.horizontal_walls[row + 1][col] == 0:
                    maze[row * 2 + 2][col * 2 + 1] = 0

        return maze

    def print_maze(self):
        """Выводит лабиринт в консоль в текстовом виде."""
        maze = self.get_maze_matrix()

        for row in maze:
            for cell in row:
                if cell == 1:
                    print("██", end="")
                else:
                    print("  ", end="")
            print()