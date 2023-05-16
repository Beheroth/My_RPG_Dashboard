import pyglet
from PIL import Image, ImageDraw
import PIL


class Token:
    picture = None

    def __init__(self, picture_path=None, x=0.0, y=0.0, width=1.0, height=1.0, rotation=0.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        if picture_path:
            stenciled = self.apply_circular_stencil(picture_path)
            self.set_picture(stenciled)

    def set_picture(self, picture_path):
        self.picture = pyglet.image.load(picture_path)
        self.picture.anchor_x = self.picture.width  // 2
        self.picture.anchor_y = self.picture.height // 2

    def apply_circular_stencil(self, picture_path):
        base = Image.open(picture_path).convert("RGBA")
        bg   = Image.new(mode="RGBA", size=base.size, color=(255, 255, 255, 0))
        mask = Image.new(mode="RGBA", size=base.size, color=(0, 0, 0, 255))
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, base.size[0]-1, base.size[1]-1), fill=(255, 255, 255, 0))
        im = Image.composite(bg, base, mask)
        new_path = "{}_tmp.png".format(picture_path)
        im.save(fp=new_path)
        return new_path
