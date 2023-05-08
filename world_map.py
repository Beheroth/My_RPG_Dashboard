import pyglet.image


class Token:

    def __init__(self, picture_path=None, x=0.0, y=0.0, width=1.0, height=1.0, orientation=0.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.orientation = orientation
        self.picture = None
        if picture_path:
            self.picture = pyglet.image.load(picture_path)


class World_Map:
    tokens = []

    def __init__(self):
        pass

    def load_from_json(self, file_path="data/map1.json"):
        import json
        with open(file_path, "r") as f:
            data = json.load(f)
            print(data)
