import pygame
from config import settings

class Renderer:
    def __init__(self, screen, player, world_map):
        self.screen = screen
        self.player = player
        self.map = world_map

    def draw(self, camera_x, camera_y):
        tile_size = settings.TILE_SIZE

        tiles_x = settings.WIDTH // tile_size
        tiles_y = settings.HEIGHT // tile_size

        offset_x = int(camera_x - tiles_x // 2)
        offset_y = int(camera_y - tiles_y // 2)

        offset_x = max(0, min(offset_x, len(self.map[0]) - tiles_x))
        offset_y = max(0, min(offset_y, len(self.map) - tiles_y))

        for row in range(tiles_y):
            for col in range(tiles_x):
                map_x = col + offset_x
                map_y = row + offset_y

                if 0 <= map_x < len(self.map[0]) and 0 <= map_y < len(self.map):
                    tile = self.map[map_y][map_x]

                    color = (50, 50, 50) if tile == "." else (100, 100, 100)

                    pygame.draw.rect(
                        self.screen,
                        color,
                        (col * tile_size, row * tile_size, tile_size, tile_size)
                    )

        # Получаем реальные пиксельные координаты
        px, py, size, _ = self.player.get_pixel_position()
        draw_x = px - offset_x * tile_size
        draw_y = py - offset_y * tile_size

        pygame.draw.rect(
            self.screen,
            settings.PLAYER_COLOR,
            (draw_x, draw_y, size, size)
        )

        font = pygame.font.SysFont(None, 24)
        coords_text = font.render(f"({self.player.x}, {self.player.y})", True, (255, 255, 255))
        self.screen.blit(coords_text, (10, 10))
