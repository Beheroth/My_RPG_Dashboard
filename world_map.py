import world_token


class World_Map:
    tokens: list[world_token.Token] = []

    def __init__(self):
        test_token = world_token.Token(picture_path="resources/token.png", rotation=0.0)
        self.tokens.append(test_token)
        lea_token = world_token.Token(x=-1, y=-1, width=2, height=2, picture_path="resources/lea.png", rotation=0.0)
        self.tokens.append(lea_token)


    def load_from_json(self, file_path="data/map1.json"):
        import json
        with open(file_path, "r") as f:
            data = json.load(f)
            print(data)

    def move_token(self, token, x, y):
        token.x = x
        token.y = y
