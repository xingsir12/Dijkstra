import pygame
from tkinter import messagebox, Tk
import sys
from Button import ImageButton
import time

pygame.init()

width = 960
height = 600
max_fps = 60

display = pygame.display.set_mode((width, height),)
pygame.display.set_caption("Dijkstra's algorithm")
main_back = pygame.image.load('dij.jpg')
main_back2 = pygame.image.load('dij(4).jpg')
main_back3 = pygame.image.load('dij(2).jpg')

clock = pygame.time.Clock()

pygame.display.set_caption('Алгоритм Дейкстры')

icon = pygame.image.load('cherry.png')
pygame.display.set_icon(icon)


def main_menu():
    start_button = ImageButton(width/2-(352/2), 250, 350, 84, "Начать использовать",
                               "green_button2.jpg", "green_button2_hover.jpg", "odin-klik-myshki.mp3")

    settings_button = ImageButton(width / 2 - (352 / 2), 350, 350, 84, "Настройки",
                               "green_button2.jpg", "green_button2_hover.jpg", "odin-klik-myshki.mp3")

    exit_button = ImageButton(width/2-(252/2), 450, 252, 74, "Выйти",
                               "green_button2.jpg", "green_button2_hover.jpg", "odin-klik-myshki.mp3")

    running = True
    while running:
        display.fill((0, 0, 0))
        display.blit(main_back, (0, 0))

        font = pygame.font.Font(None, 72)
        text_surface = font.render("Алгоритм Дейкстры", True, 'black')
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        display.blit(text_surface, text_rect)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == start_button:
                fade()
                new_game()

            if event.type == pygame.USEREVENT and event.button == settings_button:
                fade()
                settings_menu()

            if event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
                pygame.quit()
                sys.exit()

            for btn in [start_button, settings_button, exit_button]:
                btn.handle_event(event)

        for btn in [start_button, settings_button, exit_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(display)

        pygame.display.flip()

def settings_menu():
    audio_button = ImageButton(width / 2 - (252 / 2), 270, 252, 74, "Аудио", "green_button2.jpg",
                               "green_button2_hover.jpg", "odin-klik-myshki.mp3")
    video_button = ImageButton(width / 2 - (252 / 2), 360, 252, 74, "Видео", "green_button2.jpg",
                               "green_button2_hover.jpg", "odin-klik-myshki.mp3")
    back_button = ImageButton(width / 2 - (252 / 2), 450, 252, 74, "Назад", "green_button2.jpg",
                              "green_button2_hover.jpg", "odin-klik-myshki.mp3")


    running = True
    while running:
        display.fill((0, 0, 0))
        display.blit(main_back2, (0, 0))

        font = pygame.font.Font(None, 72)
        text_surface = font.render("НАСТРОЙКИ", True, 'black')
        text_rect = text_surface.get_rect(center=(width / 2, 100))
        display.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Возврат в меню
                if event.key == pygame.K_ESCAPE:
                    fade()
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_button:
                fade()
                running = False

            for btn in [audio_button, video_button, back_button]:
                btn.handle_event(event)

        for btn in [audio_button, video_button, back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(display)

        pygame.display.flip()


def new_game():
    pygame.display.set_caption('Выбери начальную позицию')

    begin_search = False
    target_box_set = False
    searching = True
    target_box = None
    start_box_set = False


    # Тело приложения
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

    # Количество клеток
    columns = 32
    rows = 20

    box_width = width // columns
    box_height = height // rows

    # Клетки, очередь, путь
    grid = []
    queue = []
    path = []

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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Удаление клетки старта при нажатии клавиши Backspace
                    pygame.display.set_caption('Выбери начальную позицию')
                    start_box.start = False
                    start_box_set = False

                elif event.key == pygame.K_2:  # Удаление клетки цели при нажатии клавиши Delete
                    pygame.display.set_caption('Выбери конечную цель')
                    target_box.target = False
                    target_box_set = False

                elif event.key == pygame.K_3:
                    start_box.start = False
                    target_box.target = False
                    begin_search = False
                    target_box_set = False
                    searching = False
                    target_box = None
                    start_box_set = False
                    current_box.visited = False
                    neighbour.queued = False

                    # Возврат в меню
                elif event.key == pygame.K_ESCAPE:
                    pygame.display.set_caption('Алгоритм Дейкстры')
                    fade()
                    running = False

            # Установка контроля мыши
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Нажатие левой кнопки мыши
                    x, y = pygame.mouse.get_pos()
                    i = x // box_width
                    j = y // box_height
                    if not start_box_set and not grid[i][j].wall:
                        pygame.display.set_caption('Выбери конечную цель')
                        start_box = grid[i][j]
                        start_box.start = True
                        start_box.visited = True
                        queue.append(start_box)
                        start_box_set = True

            # Удаление стен при помощи правой кнопки мыши
            elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[2]:
                    x, y = pygame.mouse.get_pos()
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = False

            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                # Рисуем стены
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                # Рисуем стены
                elif event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = False
                # Ставим клетку цели
                if event.buttons[2] and not target_box_set:
                    pygame.display.set_caption('Рисуй стены или нажми Enter')
                    i = x // box_width
                    j = y // box_height
                    target_box = grid[i][j]
                    target_box.target = True
                    target_box_set = True

            # Начало алгоритма
            if event.type == pygame.KEYDOWN and target_box_set:
                pygame.display.set_caption('Чтобы остановить нажмите S')
                begin_search = True
                start_time = time.time()
                if event.key == pygame.K_s:
                    pygame.display.set_caption('Чтобы продолжить нажмите C')
                    begin_search = False
                elif event.key == pygame.K_c:
                    begin_search = True
                elif event.key == pygame.K_ESCAPE:
                    pygame.display.set_caption('Алгоритм Дейкстры')
                    fade()
                    running = False

        if begin_search:
            shortest_path_length = 0
            total_seconds = 0

            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True

                if current_box == target_box: #Если полностью выполнился цикл
                    pygame.display.set_caption('Алгоритм Дейкстры')
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

                    Tk().wm_withdraw()
                    messagebox.showinfo("Итоги", f"Время выполнения цикла: {execution_time} секунд\n"
                    f"Время предполагаемого пути: {total_seconds} секунд или {minutes} минуты {seconds} секунд\n"
                    f"Количество клеток кратчайшего пути: {shortest_path_length}")

                    print("Время выполнения цикла:", execution_time, "секунд")
                    print("Время предполагаемого пути: ", total_seconds , "секунд или ",
                          f"{minutes} минуты {seconds} секунд")
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
        display.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(display, (100, 100, 100)) #grey

                if box.queued:
                    box.draw(display, (200, 0, 0)) #green
                if box.visited:
                    box.draw(display, (0, 200, 0)) #red
                if box in path:
                    box.draw(display, (0, 0, 200)) #blue

                if box.start:
                    box.draw(display, (0, 200, 200)) #light blue
                if box.wall:
                    box.draw(display, (10, 10, 10)) #black
                if box.target:
                    box.draw(display, (200, 200, 0)) #yellow



        pygame.display.flip()


def fade():
    running = True
    fade_alpha = 0  # Уровень прозрачности для анимации

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Анимация затухания текущего экрана
        fade_surface = pygame.Surface((width, height))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        display.blit(fade_surface, (0, 0))

        # Увеличение уровня прозрачности
        fade_alpha += 5
        if fade_alpha >= 105:
            fade_alpha = 255
            running = False

        pygame.display.flip()
        clock.tick(max_fps)  # Ограничение FPS


if __name__ == "__main__":
    main_menu()