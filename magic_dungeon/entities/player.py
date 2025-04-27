import pygame
from config import settings

class Player:
    def __init__(self):
        self.size = settings.TILE_SIZE
        self.x = 50.0
        self.y = 50.0
        self.target_x = self.x
        self.target_y = self.y

        self.move_speed = 0.2  # скорость в клетках за кадр (по умолчанию)
        self.move_cooldown = 150
        self.last_move_time = 0

        self.move_direction = (0, 0)
        self.is_moving = False

    def update_from_input(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1

        self.move_direction = (dx, dy)
        self.is_moving = (dx != 0 or dy != 0)

        # Режим бега по Shift
        is_shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        if is_shift:
            self.move_speed = 0.35      # быстрее перемещение
            self.move_cooldown = 80     # чаще шаги
        else:
            self.move_speed = 0.2
            self.move_cooldown = 150

    def tick_move(self):
        if not self.is_moving:
            self.target_x = self.x
            self.target_y = self.y
            return

        now = pygame.time.get_ticks()
        dx, dy = self.move_direction
        if now - self.last_move_time >= self.move_cooldown:
            tx = self.target_x + dx
            ty = self.target_y + dy
            if 0 <= tx < 100 and 0 <= ty < 100:
                self.target_x = tx
                self.target_y = ty
                self.last_move_time = now

    def update_position(self):
        if abs(self.x - self.target_x) > self.move_speed:
            self.x += self.move_speed if self.x < self.target_x else -self.move_speed
        else:
            self.x = self.target_x

        if abs(self.y - self.target_y) > self.move_speed:
            self.y += self.move_speed if self.y < self.target_y else -self.move_speed
        else:
            self.y = self.target_y

    def set_target_by_mouse(self, mouse_pos, camera_offset):
        mx, my = mouse_pos
        offset_x, offset_y = camera_offset
        self.target_x = mx // self.size + offset_x
        self.target_y = my // self.size + offset_y

    def get_pixel_position(self):
        return self.x * self.size, self.y * self.size, self.size, self.size
