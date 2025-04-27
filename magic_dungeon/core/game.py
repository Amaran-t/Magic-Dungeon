import pygame
from config import settings
from entities.player import Player
from graphics.renderer import Renderer
from core.world import generate_world_map
from menu_logic import run_main_menu  # НЕ импортирует Game, всё безопасно

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        info = pygame.display.Info()
        settings.WIDTH = info.current_w
        settings.HEIGHT = info.current_h

        pygame.display.set_caption("Подземелье мага")
        self.clock = pygame.time.Clock()

        self.world_map = generate_world_map()
        self.player = Player()
        self.renderer = Renderer(self.screen, self.player, self.world_map)
        self.running = True

        self.camera_x = self.player.x
        self.camera_y = self.player.y

        self.camera_anchor_x = self.player.x
        self.camera_anchor_y = self.player.y
        self.camera_following = False

    def run(self):
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(settings.FPS)

        pygame.quit()

    def _handle_events(self):
        tiles_x = settings.WIDTH // settings.TILE_SIZE
        tiles_y = settings.HEIGHT // settings.TILE_SIZE

        offset_x = int(self.camera_x - tiles_x // 2)
        offset_y = int(self.camera_y - tiles_y // 2)

        offset_x = max(0, min(offset_x, len(self.world_map[0]) - tiles_x))
        offset_y = max(0, min(offset_y, len(self.world_map) - tiles_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.player.set_target_by_mouse(event.pos, (offset_x, offset_y))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run_main_menu()  # безопасно вызывается

    def _update(self):
        self.player.update_from_input()
        self.player.tick_move()
        self.player.update_position()

        dist_x = abs(self.player.x - self.camera_anchor_x)
        dist_y = abs(self.player.y - self.camera_anchor_y)
        threshold = 2

        if dist_x > threshold or dist_y > threshold:
            self.camera_following = True

        if self.camera_following:
            dx = self.player.x - self.camera_x
            dy = self.player.y - self.camera_y
            max_cam_speed = 0.15

            if abs(dx) > max_cam_speed:
                self.camera_x += max_cam_speed if dx > 0 else -max_cam_speed
            else:
                self.camera_x = self.player.x

            if abs(dy) > max_cam_speed:
                self.camera_y += max_cam_speed if dy > 0 else -max_cam_speed
            else:
                self.camera_y = self.player.y

            if self.camera_x == self.player.x and self.camera_y == self.player.y:
                self.camera_anchor_x = self.player.x
                self.camera_anchor_y = self.player.y
                self.camera_following = False

    def _render(self):
        self.screen.fill(settings.BG_COLOR)
        self.renderer.draw(self.camera_x, self.camera_y)
        pygame.display.flip()
