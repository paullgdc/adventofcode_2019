from functools import reduce

WIDTH = 25
HEIGHT = 6

image = input()

def split_image(image, dim):
    return [image[i * dim: (i + 1) * dim] for i in range(len(image) // dim)]

def count_digit(layer, digit):
    return sum((elem == digit for elem in layer))

def merge_layers(layer_top, layer_bot):
    return "".join([
        pixel_bot if pixel_top == "2" else pixel_top
        for pixel_top, pixel_bot in zip (layer_top, layer_bot)
    ])

def format_image(layer, width):
    return "\n".join(split_image("".join([ "*" if px == "1" else " " for px in layer]), width))

layers = split_image(image, WIDTH * HEIGHT)
# Part 1

# min_layer = min((
#     (count_digit(layer, "0"), layer) for layer in layers
# ))[1]
# print(count_digit(min_layer, "1") * count_digit(min_layer, "2"))

# Part 2

merged = reduce(merge_layers, layers)
print(format_image(merged, WIDTH))
