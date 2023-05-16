import pyglet
from camera import Camera
from gui    import Gui


class View:
    window = None
    camera = None

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.display = pyglet.canvas.get_display()
        self.screens = self.display.get_screens()
        self.window = pyglet.window.Window(fullscreen=True, screen=self.screens[0])
        self.window.config.alpha_size = 8
        self.fps_display = pyglet.window.FPSDisplay(window=self.window, samples=120)
        self.camera = Camera(window=self.window)
        self.gui = Gui(view=self)

        @self.window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):

            if buttons & pyglet.window.mouse.LEFT:
                if modifiers & pyglet.window.key.MOD_CTRL:
                    self.camera.zoom(dy)
                elif modifiers & pyglet.window.key.MOD_SHIFT:
                    self.camera.x -= dx / self.camera.grid_space
                    self.camera.y -= dy / self.camera.grid_space

                elif self.gui.selected:
                    wx, wy = self.camera.to_world_space(x, y)
                    self.gui.selected.x = wx
                    self.gui.selected.y = wy

        @self.window.event
        def on_mouse_press(x, y, buttons, modifiers):
            if buttons & pyglet.window.mouse.LEFT:
                self.gui.selected = self.camera.get_token(x, y)

        @self.window.event
        def on_mouse_release(x, y, buttons, modifiers):
            token = self.gui.selected
            if token:
                target_x, target_y = self.camera.to_world_space(x, y)
                if self.camera.snap_to_grid:
                    x_base = (token.width  % 2) / 2
                    y_base = (token.height % 2) / 2
                    target_x = round(target_x + x_base) - x_base
                    target_y = round(target_y + y_base) - y_base
                self.camera.world.move_token(self.gui.selected, target_x, target_y)

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            wx, wy = self.camera.to_world_space(x, y)
            self.gui.l_pos.text = ("({:04.2f}, {:04.2f})".format(wx, wy))



    def render_gui(self):
        self.gui.render()

        # button_menu = pyglet.gui.PushButton(x=0, y=0, pressed=pressed, depressed=None, batch=self.batch_gui)

    def start(self):
        """create the view timer and pass it the render function"""

        def render(dt):
            self.window.clear()
            self.camera.draw_tokens()
            self.camera.render(dt)
            self.fps_display.draw()
            self.render_gui()

        pyglet.clock.schedule_interval(render, 1 / 60)

    def use_world(self, world):
        self.camera.world = world
