import pygame
import sys
from menu_runner import start_game  # только этот импорт

def run_main_menu():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Главное меню")

    FONT = pygame.font.SysFont(None, 48)
    BUTTON_COLOR = (70, 70, 200)
    HOVER_COLOR = (100, 100, 255)
    TEXT_COLOR = (255, 255, 255)
    BG_COLOR = (20, 20, 40)

    clock = pygame.time.Clock()

    class Button:
        def __init__(self, text, center_pos, callback):
            self.text = text
            self.callback = callback
            self.rect = pygame.Rect(0, 0, 300, 60)
            self.rect.center = center_pos
            self.text_surf = FONT.render(text, True, TEXT_COLOR)
            self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        def draw(self, surface):
            mouse_pos = pygame.mouse.get_pos()
            color = HOVER_COLOR if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(surface, color, self.rect, border_radius=10)
            surface.blit(self.text_surf, self.text_rect)

        def handle_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.callback()

    def open_settings():
        print("Открытие настроек...")

    def exit_game():
        nonlocal running
        running = False

    buttons = [
        Button("Зайти в игру", (WIDTH // 2, HEIGHT // 2 - 100), start_game),
        Button("Настройки",   (WIDTH // 2, HEIGHT // 2),       open_settings),
        Button("Выход",       (WIDTH // 2, HEIGHT // 2 + 100), exit_game),
    ]

    running = True
    while running:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for btn in buttons:
                btn.handle_event(event)

        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
