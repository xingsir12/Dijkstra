from tkinter import messagebox, Tk
import pygame
import sys
import time

#Размер экрана
window_width = 800
window_height = 800

window = pygame.display.set_mode((window_width, window_height))

#Количество клеток
columns = 40
rows = 40

box_width = window_width // columns
box_height = window_height // rows

#Клетки, очередь, путь
grid = []
queue = []
path = []

#Тело приложения
class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width,
                                      self.y * box_height, box_width - 2, box_height - 2))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])


# Создание клеток
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)

# Установка сетки
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

#Главная функция
def main():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None
    start_box_set = False

#Пока исполняется функция
    while True:
        for event in pygame.event.get():
            # Выход из приложения
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Установка контроля мыши
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Нажатие левой кнопки мыши
                    x, y = pygame.mouse.get_pos()
                    i = x // box_width
                    j = y // box_height
                    if not start_box_set and not grid[i][j].wall:
                        start_box = grid[i][j]
                        start_box.start = True
                        start_box.visited = True
                        queue.append(start_box)
                        start_box_set = True
            #Если мышь в движении при клике
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Рисуем стены
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                # Ставим клетку цели
                if event.buttons[2] and not target_box_set:
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True
            # Начало алгоритма
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True
                start_time = time.time()
                if event.key == pygame.K_s:
                    begin_search = False
                elif event.key == pygame.K_c:
                    begin_search = True

#При начале поиска пути
        if begin_search:
            shortest_path_length = 0
            total_seconds = 0
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True

                if current_box == target_box: #Если полностью выполнился цикл
                    searching = False

                    while current_box.prior != start_box: #Пока путь не равен начальному значению
                        path.append(current_box.prior)
                        current_box = current_box.prior
                        shortest_path_length += 1 #Счетчик клеток
                        total_seconds += 5 #Счетчик для секунд

                    #Функция для перевода секунд в минуты для пути
                    def seconds_to_minutes(seconds):
                        minutes = seconds // 60
                        remaining_seconds = seconds % 60
                        return minutes, remaining_seconds

                    minutes, seconds = seconds_to_minutes(total_seconds)

                    end_time = time.time()
                    execution_time = end_time - start_time
                    print("Время выполнения цикла:", execution_time, "секунд")
                    print("Время предполагаемого пути: ", total_seconds , "секунд или ", f"{minutes} минуты {seconds} секунд")
                    print(f"Количество клеток кратчайшего пути: {shortest_path_length}")

                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("Ошибка", "Не найден путь.")
                    searching = False

        #Рисуем определенным цветом клетки:
        window.fill((0, 0, 0))


        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, (100, 100, 100)) #grey

                if box.queued:
                    box.draw(window, (200, 0, 0)) #green
                if box.visited:
                    box.draw(window, (0, 200, 0)) #red
                if box in path:
                    box.draw(window, (0, 0, 200)) #blue

                if box.start:
                    box.draw(window, (0, 200, 200)) #light blue
                if box.wall:
                    box.draw(window, (10, 10, 10)) #black
                if box.target:
                    box.draw(window, (200, 200, 0)) #yellow

        pygame.display.flip()


main()