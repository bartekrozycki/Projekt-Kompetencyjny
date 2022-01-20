import pickle
from types import SimpleNamespace

import pygame

from src import state, logic, constants
from src.state import drawing, selecting
from src.ui_logic import menu, draw, window, select


def saveRoadsToFile():
    roads_file = open(constants.ROADS_FILENAME, 'wb')
    pickle.dump(state.roads, roads_file)
    roads_file.close()


def readRoadsFromFile():
    try:
        roads_file = open(constants.ROADS_FILENAME, 'rb')
        state.roads = pickle.load(roads_file)
        roads_file.close()
    except EOFError:
        print("Empty file")
    except FileNotFoundError:
        print("Not found any roads file")


if __name__ == '__main__':
    readRoadsFromFile()
    pygame.font.init()
    state.font_consolas = pygame.font.SysFont('Consolas', 15)

    pygame.display.init()

    res_w, res_h = state.resolution = (pygame.display.Info().current_w - 200, pygame.display.Info().current_h - 300)
    state.window = pygame.display.set_mode(state.resolution, pygame.RESIZABLE)

    state.background = logic.recreate_background()

    pygame.draw.rect(state.window, constants.BLACK, (0, 0, state.menu.width, state.resolution[1]))
    state.window.blit(state.background.image, (state.menu.width, 0), area=logic.background_display_rectangle(0, 0))

    state.buttons.extend([SimpleNamespace(use=logic.button_select, text="Select", activable=True),
                          SimpleNamespace(use=logic.button_draw, text="Draw", activable=True),
                          SimpleNamespace(use=logic.button_clear_workspace, text="Clear", activable=False)])
    logic.render_buttons()

    pygame.display.update()

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break
            window(event)
            if pygame.mouse.get_pos()[0] <= state.menu.width:
                menu(event)
            elif drawing.on:
                draw(event)
            elif selecting.on:
                select(event)

        state.clock.tick(60)
    saveRoadsToFile()

    pygame.quit()
