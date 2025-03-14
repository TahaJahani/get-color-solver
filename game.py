import hashlib
import json
from copy import copy
from typing import List
from bottle import Bottle

class Game:
    def __init__(self, maximum_depth: int):
        self.bottles: List[Bottle] = []
        self.seen_states: List[str] = []
        self.maximum_depth: int = maximum_depth

    def add_bottle(self, bottle):
        self.bottles.append(bottle)

    def print(self):
        for index, bottle in enumerate(self.bottles):
            print(index, end=". ")
            bottle.print()

    def pour(self, src, dst):
        src_bottle = self.bottles[src]
        dst_bottle = self.bottles[dst]
        src_bottle.pour_to(dst_bottle)

    def won(self):
        won = True
        for bottle in self.bottles:
            if not bottle.is_done():
                won = False
                break
        return won

    def get_state(self):  # performance...
        colors = []
        for bottle in self.bottles:
            colors.append(str(bottle.colors))
        colors = sorted(colors)
        return hashlib.sha512(str(colors).encode()).hexdigest()

    def print_path(self, path):
        for item in path:
            print(item)
        print("---------")
        print(f"{len(path)} steps")

    def solve(self, path=None):
        if path is None:
            path = []
        if len(path) > self.maximum_depth:
            return
        current_state = self.get_state()
        if current_state in self.seen_states:
            return
        self.seen_states.append(current_state)
        if self.won():
            self.print_path(path)
            exit(0)
        for src_index, src in enumerate(self.bottles):
            for dst_index, dst in enumerate(self.bottles):
                if src_index == dst_index:
                    continue
                if src.can_pour_to(dst) and src.good_to_pour_to(dst):
                    src_colors = copy(src.colors)
                    dst_color = copy(dst.colors)
                    src.pour_to(dst)
                    path.append(f"{src_index} -> {dst_index}")
                    self.solve(path)
                    path.pop()
                    src.colors = src_colors
                    dst.colors = dst_color

    @staticmethod
    def load_json(file_name):
        with open(file_name, "r") as f:
            data = json.load(f)
        game = Game(data['max_depth'])
        for bottles_data in data['bottles']:
            bottle = Bottle(bottles_data['colors'], bottles_data['capacity'])
            game.add_bottle(bottle)
        return game