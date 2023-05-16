import pyglet
import math
import world_map


class Camera:
    _world: world_map.World_Map
    counter = 0.0
    dt = 0.0

    def __init__(self, x=0.0, y=0.0, z=1.0, window=None):
        self.x = x
        self.y = y
        self.z = z
        self.window = window
        self.generate_grid_lines()
        self._old_coord = (self.x, self.y, self.z)
        self.snap_to_grid = True

    @property
    def grid_space(self):
        return int(64.0 / float(self.z))

    @grid_space.setter
    def grid_space(self, w):
        w = int(pyglet.math.clamp(num=w, min_val=16.0, max_val=self.window.height - 2))
        self.z = 64 / w

    @property
    def world(self):
        return self._world

    @world.setter
    def world(self, world):
        self._world = world
        self.zoom(0)

    def to_camera_space(self, x_world, y_world):
        x = (self.window.width / 2 + (x_world - self.x) * self.grid_space)
        y = (self.window.height / 2 + (y_world - self.y) * self.grid_space)
        return x, y

    def to_world_space(self, x_camera, y_camera):
        x = self.x + (x_camera - self.window.width  / 2) / self.grid_space
        y = self.y + (y_camera - self.window.height / 2) / self.grid_space
        return x, y

    def generate_grid_lines(self):
        W = self.window.width
        H = self.window.height
        left = (self.x - (W / 2 / self.grid_space))
        right = (self.x + (W / 2 / self.grid_space))
        down = (self.y - (H / 2 / self.grid_space))
        up = (self.y + (H / 2 / self.grid_space))
        color = [64, 64, 64, 255]
        self.grid_lines = []

        for i in range(math.ceil(left), math.floor(right) + 1, 1):
            x, y = self.to_camera_space(i, 0)
            self.grid_lines.append(pyglet.shapes.Line(x, 0, x, H, color=color))
        for j in range(math.ceil(down), math.floor(up) + 1, 1):
            x, y = self.to_camera_space(0, j)
            self.grid_lines.append(pyglet.shapes.Line(0, y, W, y, color=color))

    def draw_grid(self):
        new_coord = (self.x, self.y, self.z)
        if new_coord != self._old_coord:
            self.generate_grid_lines()
        batch_grid = pyglet.graphics.Batch()
        line: pyglet.shapes.Line
        for line in self.grid_lines:
            line.batch=batch_grid
        batch_grid.draw()
        self._old_coord = new_coord

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
        token_batch = pyglet.graphics.Batch()
        sprites = []
        m_buffer: pyglet.image.BufferManager = pyglet.image.get_buffer_manager()
        if not self.world:
            return
        for token in self.world.tokens:
            x_camera, y_camera = self.to_camera_space(token.x, token.y)
            image: pyglet.image.ImageData = token.picture.get_image_data()
            sprite = pyglet.sprite.Sprite(x=x_camera, y=y_camera, img=image, batch=token_batch)
            sprite.scale_x = self.grid_space * token.width  / token.picture.width
            sprite.scale_y = self.grid_space * token.height / token.picture.height
            sprite.rotation = token.rotation
            token.rotation += self.dt * 36 * self.z
            sprites.append(sprite)

        token_batch.draw()


    def render(self, dt):
        self.dt = dt
        self.draw_tokens()
        self.draw_grid()
        #self.draw_sweep()
        self.draw_world_origin()
        self.draw_camera_center()

    def zoom(self, dz):
        self.grid_space = self.grid_space + dz

    def get_token(self, x_camera, y_camera):
        result = None
        smallest_dist = math.inf
        for token in self.world.tokens:
            dist = math.dist((x_camera, y_camera), self.to_camera_space(token.x, token.y))
            if dist < min(token.width*self.grid_space/2, smallest_dist):
                result = token
                smallest_dist = dist
        return result

