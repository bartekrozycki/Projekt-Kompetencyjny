import pygame

from src import state, logic, ui_logic
from src.constants import *

event_handlers = {
    'select': ui_logic.select,
    'draw': ui_logic.draw,
}

button_shortcuts = {
    pygame.K_s: 'select',
    pygame.K_d: 'draw',
    pygame.K_c: 'clear'
}

if __name__ == '__main__':
    logic.load()

    pygame.font.init()
    pygame.display.init()

    state.font_consolas = pygame.font.SysFont('Consolas', 15)
    state.resolution = (pygame.display.Info().current_w - 200, pygame.display.Info().current_h - 300)
    state.display = pygame.display.set_mode(state.resolution, pygame.RESIZABLE)
    logic.create_background()

    state.display.blit(state.background, (MENU_W, 0), logic.get_workspace_rect())

    logic.draw_buttons()
    pygame.display.update()

    clock = pygame.time.Clock()
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key in button_shortcuts.keys():
                    logic.press_button(button_shortcuts[event.key])
                elif event.key == pygame.K_q:
                    running = False
                    break

            ui_logic.window(event)

            if state.window.moving:
                continue

            if pygame.mouse.get_pos()[0] <= MENU_W:
                ui_logic.menu(event)
            else:
                event_handlers[state.selected_mode](event)

        clock.tick(3000)

    logic.save()
    pygame.quit()
