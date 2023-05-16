import pyglet
import pyglet.font


class Gui:
    widgets = []
    selected = None

    def __init__(self, view):
        self.view = view

        self.l_grid_space = pyglet.text.Label("",
                                              font_name="Casablanca Antique Plain",
                                              font_size=12,
                                              anchor_y='top',
                                              x=10, y=self.view.window.height)
        self.register(self.l_grid_space)
        self.l_info = pyglet.text.Label("",
                                        font_name="Casablanca Antique Plain",
                                        font_size=16,
                                        anchor_x='right', anchor_y='bottom',
                                        x=self.view.window.width, y=0)
        self.register(self.l_info)
        self.l_pos = pyglet.text.Label("",
                                        font_name="Casablanca Antique Plain",
                                        font_size=16,
                                        anchor_x='right', anchor_y='bottom',
                                        x=self.view.window.width, y=18)
        self.register(self.l_pos)

    def register(self, widget):
        self.widgets.append(widget)

    def render(self):
        self.update()
        batch = pyglet.graphics.Batch()
        for widget in self.widgets:
            widget.batch = batch
        batch.draw()

    def update(self):
        self.l_grid_space.text = str(self.view.camera.grid_space)
        self.l_info.text = str(self.selected)


