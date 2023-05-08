import pyglet
import math
import world_map


class Camera:
    counter = 0.0
    dt = 0.0

    def __init__(self, x=0.0, y=0.0, z=1.0, window=None, world=None):
        self.x = x
        self.y = y
        self.z = z
        self.window = window
        self.grid_width = int(64.0 / float(z))
        self.world = world

    def to_camera_space(self, x_world, y_world):
        x = (self.window.width / 2 + (x_world - self.x) * self.grid_width)
        y = (self.window.height / 2 + (y_world - self.y) * self.grid_width)
        return x, y

    def to_world_space(self, x_camera, y_camera):
        x = self.window.width  / 2 + x_camera
        y = self.window.height / 2 + y_camera
        return x, y

    def draw_grid(self):
        batch_grid = pyglet.graphics.Batch()
        W = self.window.width
        H = self.window.height
        left = (self.x - (W / 2 / self.grid_width))
        right = (self.x + (W / 2 / self.grid_width))
        down = (self.y - (H / 2 / self.grid_width))
        up = (self.y + (H / 2 / self.grid_width))
        color = [64, 64, 64, 255]
        lines = []

        for i in range(math.ceil(left), math.floor(right) + 1, 1):
            x, y = self.to_camera_space(i, 0)
            lines.append(pyglet.shapes.Line(x, 0, x, H, color=color, batch=batch_grid))
        for j in range(math.ceil(down), math.floor(up) + 1, 1):
            x, y = self.to_camera_space(0, j)
            lines.append(pyglet.shapes.Line(0, y, W, y, color=color, batch=batch_grid))
        batch_grid.draw()

    def draw_sweep(self):
        color = [80, 80, 80, 255]
        speed = self.window.height
        line = pyglet.shapes.Line(0, self.counter, self.window.width, self.counter, color=color)
        self.counter = (self.counter + self.dt * speed) % self.window.height
        line.draw()

    def draw_world_origin(self):
        batch_origin = pyglet.graphics.Batch()
        W = self.window.width
        H = self.window.height
        x, y = self.to_camera_space(0, 0)
        color = [100, 100, 100, 255]
        lines = [pyglet.shapes.Line(0, y, W, y, color=color, batch=batch_origin),
                 pyglet.shapes.Line(x, 0, x, H, color=color, batch=batch_origin)]

        batch_origin.draw()

    def draw_camera_center(self):
        batch_camera_center = pyglet.graphics.Batch()
        W = self.window.width
        H = self.window.height
        x, y = self.to_camera_space(self.x, self.y)
        color = [255, 255, 0, 255]
        lines = [pyglet.shapes.Line(W*0.5-10, y, W*0.5+10, y, width=2, color=color, batch=batch_camera_center),
                 pyglet.shapes.Line(x, H*0.5-10, x, H*0.5+10, width=2, color=color, batch=batch_camera_center)]
        batch_camera_center.draw()


    def draw_tokens(self):
        for token in self.world.tokens:
            token_pic = token.get_img()

    def render(self, dt):
        self.dt = dt
        self.draw_tokens()
        self.draw_grid()
        self.draw_sweep()
        self.draw_world_origin()
        self.draw_camera_center()


    def zoom(self, dy):
        self.grid_width = int(pyglet.math.clamp(num=self.grid_width + dy, min_val=16.0, max_val=self.window.height - 2))
