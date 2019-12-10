from collections import Counter

from typing import List


def read_file(filename="input.txt") -> str:
    with open(filename) as f:
        return f.readline().strip()


class Layer():
    def __init__(self, width: int, pixel_vals: str):
        self.pixel_vals = pixel_vals
        self.layer = [[int(pixel_vals[i]) for i in range(x, x + width)]
                      for x in range(0, (len(pixel_vals)-width) + 1, width)]


class Image():
    def __init__(self, width: int, height: int, encoding: str):
        self.height = height
        self.width = width
        self.encoding = encoding
        self.num_pixels = len(self.encoding)
        self.layer_size = height * width
        self.num_layers = len(self.encoding) // self.layer_size

        self.layers = [Layer(width, self.encoding[x: x + self.layer_size])
                       for x in range(0, (len(self.encoding) - self.layer_size) + 1, self.layer_size)]

    def least_zeroes(self) -> Layer:
        min_zeroes = float('inf')
        idx = 0
        for curr_idx, layer in enumerate(self.layers):
            count = Counter([pixel for row in layer.layer for pixel in row])
            if count[0] <= min_zeroes:
                min_zeroes = count[0]
                idx = curr_idx
        return self.layers[idx]

    def ones_times_twos(self, layer: Layer) -> int:
        count = Counter([pixel for row in layer.layer for pixel in row])
        print(count)
        return count[1] * count[2]

    def decode(self) -> str:
        output = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                for layer in range(len(self.layers)):
                    color = self.layers[layer].layer[i][j]
                    if color == 0:
                        output[i][j] = ' '
                        break
                    elif color == 1:
                        output[i][j] = '*'
                        break

        for row in output:
            print(''.join(row))


# width, height, file = 2, 2, '0222112222120000'
# image = Image(width, height, file)
# print(image.decode())

image = Image(25, 6, read_file())
image.decode()
