import random
import sys

field_size_max = 32
field_size_min = 20
field_threshold_min = 0.00 #threshold of obstacle
field_threshold_max = 0.30
block_size_max = 8
blocks_ratio_min = 0.7 #blank cells in field / cells of blocks 
blocks_ratio_max = 1.5
blocks_threshold_min = 0.01 #threshold of making random block
blocks_threshold_max = 0.99

def rand(threshold=0.5):
    return random.random() < threshold

def draw(lines):
    for line in lines:
        print(" ".join([("1" if x else "0") for x in line]))

def create():
    field_width = (int)(random.random() * (field_size_max - field_size_min) + field_size_min)
    field_height = (int)(random.random() * (field_size_max - field_size_min) + field_size_min)
    field_threshold = random.random() * (field_threshold_max - field_threshold_min) + field_threshold_min
    field = create_panel(field_width, field_height, field_threshold)
    draw(field)

def create_panel(field_width, field_height, field_threshold):
    field = [[rand(field_threshold) if (i < field_height and j < field_width) else True for j in range(0, field_size_max)] for i in range(0, field_size_max)]
    n = 0
    for line in field:
        for item in line:
            if item:
                n = n + 1
    return field

if __name__ == "__main__":
    create()
