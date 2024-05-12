import pygame
import sys
from Button import ImageButton

pygame.init()

width = 960
height = 600
max_fps = 60

display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dijkstra's algorithm")
main_back = pygame.image.load('dij.jpg')
main_back2 = pygame.image.load('dij(4).jpg')
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
                print("Кнопка 'Старт' была нажата!")
                fade()
                new_game()

            if event.type == pygame.USEREVENT and event.button == settings_button:
                print("Кнопка 'Настройки' была нажата!")
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
    display.fill((0, 0, 0))
    display.blit(main_back2, (0, 0))




    running = True
    while running:
        from Dijkstra import Box

        display.fill((0, 0, 0))
        display.blit(game_display, (0, 0))

        columns = 25
        rows = 25

        box_width = width // columns
        box_height = height // rows

        grid = []
        queue = []
        path = []

        for i in range(columns):
            arr = []
            for j in range(rows):
                arr.append(Box(i, j))
            grid.append(arr)

        # Set Neighbours
        for i in range(columns):
            for j in range(rows):
                grid[i][j].set_neighbours()

        def main():
            begin_search = False
            target_box_set = False
            searching = True
            target_box = None
            start_box_set = False

            while True:
                for event in pygame.event.get():
                    # Quit Window
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    # Mouse Controls
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button click
                            x, y = pygame.mouse.get_pos()
                            i = x // box_width
                            j = y // box_height
                            if not start_box_set and not grid[i][j].wall:
                                start_box = grid[i][j]
                                start_box.start = True
                                start_box.visited = True
                                queue.append(start_box)
                                start_box_set = True

                    elif event.type == pygame.MOUSEMOTION:
                        x = pygame.mouse.get_pos()[0]
                        y = pygame.mouse.get_pos()[1]
                        # Draw Wall
                        if event.buttons[0]:
                            i = x // box_width
                            j = y // box_height
                            grid[i][j].wall = True
                        # Set Target
                        if event.buttons[2] and not target_box_set:
                            i = x // box_width
                            j = y // box_height
                            target_box = grid[i][j]
                            target_box.target = True
                            target_box_set = True
                    # Start Algorithm
                    if event.type == pygame.KEYDOWN and target_box_set:
                        begin_search = True

                if begin_search:
                    if len(queue) > 0 and searching:
                        current_box = queue.pop(0)
                        current_box.visited = True
                        if current_box == target_box:
                            searching = False
                            while current_box.prior != start_box:
                                path.append(current_box.prior)
                                current_box = current_box.prior
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

                window.fill((0, 0, 0))

                for i in range(columns):
                    for j in range(rows):
                        box = grid[i][j]
                        box.draw(window, (100, 100, 100))

                        if box.queued:
                            box.draw(window, (200, 0, 0))
                        if box.visited:
                            box.draw(window, (0, 200, 0))
                        if box in path:
                            box.draw(window, (0, 0, 200))

                        if box.start:
                            box.draw(window, (0, 200, 200))
                        if box.wall:
                            box.draw(window, (10, 10, 10))
                        if box.target:
                            box.draw(window, (200, 200, 0))

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