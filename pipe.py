from typing import List

class Pipe:
    def __init__(self, colors: List[str], capacity: int):
        self.colors = colors
        self.capacity = capacity

    @property
    def remaining_capacity(self):
        return self.capacity - len(self.colors)

    @property
    def is_empty(self):
        return len(self.colors) == 0

    @property
    def top_color(self):
        if len(self.colors) > 0:
            return self.colors[-1]

    @property
    def top_color_len(self):
        if len(self.colors) == 0:
            return 0
        count = 0
        colors_reversed = list(reversed(self.colors))
        while count < len(colors_reversed) and colors_reversed[count] == self.top_color:
            count += 1
        return count

    def add_color(self, color: str, length: int):
        if (len(self.colors) != 0) and (self.top_color != color or self.remaining_capacity < length):
            raise Exception("Add color called with invalid values!")
        self.colors.extend([color] * length)

    def can_pour_to(self, other_pipe: 'Pipe'):
        return ((len(self.colors) != 0) and
                other_pipe.remaining_capacity != 0 and
                (other_pipe.is_empty or other_pipe.top_color == self.top_color))

    def good_to_pour_to(self, other_pipe: 'Pipe'):  # heuristic...
        return other_pipe.remaining_capacity >= self.top_color_len

    def pour_to(self, other_pipe: 'Pipe'):
        if not self.can_pour_to(other_pipe):
            raise Exception("Cannot Pour!")
        other_capacity = other_pipe.remaining_capacity
        pour_len = min(other_capacity, self.top_color_len)
        other_pipe.add_color(self.top_color, pour_len)
        self.colors = self.colors[:-pour_len]

    def print(self):
        print("[ ", end="")
        for i in range(self.capacity):
            if len(self.colors) > i:
                print(self.colors[i], end=" ")
            else:
                print("_", end=" ")
        print("]")

    def is_done(self):
        if self.is_empty:
            return True
        has_only_one_color = True
        for color in self.colors:
            if color != self.top_color:
                has_only_one_color = False
                break
        return has_only_one_color and len(self.colors) == self.capacity