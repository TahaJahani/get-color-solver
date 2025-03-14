import hashlib
import json
from copy import copy
from typing import List
from pipe import Pipe

class Game:
    def __init__(self, maximum_depth: int):
        self.pipes: List[Pipe] = []
        self.seen_states: List[str] = []
        self.maximum_depth: int = maximum_depth

    def add_pipe(self, pipe):
        self.pipes.append(pipe)

    def print(self):
        for index, pipe in enumerate(self.pipes):
            print(index, end=". ")
            pipe.print()

    def pour(self, src, dst):
        src_pipe = self.pipes[src]
        dst_pipe = self.pipes[dst]
        src_pipe.pour_to(dst_pipe)

    def won(self):
        won = True
        for pipe in self.pipes:
            if not pipe.is_done():
                won = False
                break
        return won

    def get_state(self):  # performance...
        colors = []
        for pipe in self.pipes:
            colors.append(str(pipe.colors))
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
        for src_index, src in enumerate(self.pipes):
            for dst_index, dst in enumerate(self.pipes):
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
        for pipe_data in data['pipes']:
            pipe = Pipe(pipe_data['colors'], pipe_data['capacity'])
            game.add_pipe(pipe)
        return game