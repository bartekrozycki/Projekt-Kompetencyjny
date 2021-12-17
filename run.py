import pygame
from pygame.event import Event

from src import state, logic, ui, constants

if __name__ == '__main__':
    pygame.font.init()
    state.font_consolas = pygame.font.SysFont('Consolas', 15)

    pygame.display.init()

    state.resolution = (pygame.display.Info().current_w - 100, pygame.display.Info().current_h - 150)
    state.window = pygame.display.set_mode(state.resolution, pygame.RESIZABLE)

    state.background = logic.create_background(-state.resolution[0], -state.resolution[1])

    pygame.draw.rect(state.window, constants.BLACK, (0, 0, state.menu.width, state.resolution[1]))
    state.window.blit(state.background.image, (state.menu.width, 0), logic.background_display_rectangle(0, 0))

    logic.create_button(logic.mode_cursor, "nothing")
    logic.create_button(logic.mode_draw_single, "draw road")

    pygame.display.update()


    def mouse_motion(event: Event):
        state.mouse_pos.x = event.pos[0]
        state.mouse_pos.y = event.pos[1]

        state.coordinates.x = event.pos[0] // state.cell.size
        state.coordinates.y = event.pos[1] // state.cell.size


    def video_resize(event: Event):
        state.resolution = event.size
        state.background = logic.create_background(*state.background.rect.topleft)
        pygame.draw.rect(state.window, constants.BLACK, (0, 0, state.menu.width, state.resolution[1]))
        state.window.blit(state.background.image, (state.menu.width, 0), logic.background_display_rectangle(0, 0))
        pygame.display.update()


    window_events = {
        pygame.MOUSEMOTION: mouse_motion,
        pygame.VIDEORESIZE: video_resize,
    }

    running = True
    while running:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                running = False
                break

            try:
                window_events[e.type](e)
            except KeyError:
                pass
            ui.handle_event(e)

        state.clock.tick(state.fps_limit)

    pygame.quit()
