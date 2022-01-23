import pygame

from src import state, logic, constants
from src.ui_logic import menu, draw, window, select

event_handlers = {
    'select': select,
    'draw': draw,
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
    state.window = pygame.display.set_mode(state.resolution, pygame.RESIZABLE)
    state.background = logic.create_background()

    pygame.draw.rect(state.window, constants.BLACK, (0, 0, state.menu.width, state.resolution[1]))
    state.window.blit(state.background.image, (state.menu.width, 0),
                      area=logic.background_display_rectangle(state.menu.width, 0))

    logic.draw_buttons()

    pygame.display.update()

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

            window(event)

            if state.moving.on:
                continue

            if pygame.mouse.get_pos()[0] <= state.menu.width:
                menu(event)
            else:
                event_handlers[state.selected_mode](event)

        state.clock.tick(300)

    logic.save()
    pygame.quit()
