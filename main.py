import pyglet
import view
import world_map


def test():
    world = world_map.World_Map()
    #world.load_from_json(file_path="data/map1.json")
    v = view.View()
    v.use_world(world)
    v.start()

    pyglet.app.run()


if __name__ == '__main__':
    test()
