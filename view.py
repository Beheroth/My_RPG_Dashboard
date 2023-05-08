import pyglet
import camera


class View:
    window = None
    camera = None

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.display = pyglet.canvas.get_display()
        self.screens = self.display.get_screens()
        self.window = pyglet.window.Window(fullscreen=True, screen=self.screens[0])
        self.fps_display = pyglet.window.FPSDisplay(window=self.window, samples=120)
        self.camera = camera.Camera(window=self.window)

        @self.window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):

            if buttons & pyglet.window.mouse.LEFT:
                if modifiers & pyglet.window.key.MOD_CTRL:
                    self.camera.zoom(dy)
                elif modifiers & pyglet.window.key.MOD_SHIFT:
                    self.camera.x -= dx / self.camera.grid_width
                    self.camera.y -= dy / self.camera.grid_width

    def render_gui(self):
        import pyglet.font
        batch_gui = pyglet.graphics.Batch()
        label = pyglet.text.Label('Menu',
                                  font_name="Casablanca Antique Plain",
                                  font_size=36,
                                  x=10, y=self.window.height,
                                  batch=batch_gui)
        label.anchor_y = 'top'

        batch_gui.draw()

        # button_menu = pyglet.gui.PushButton(x=0, y=0, pressed=pressed, depressed=None, batch=self.batch_gui)

    def start(self):

        def render(dt):
            self.window.clear()
            self.camera.render(dt)
            self.fps_display.draw()
            self.render_gui()

        pyglet.clock.schedule_interval(render, 1 / 60)
