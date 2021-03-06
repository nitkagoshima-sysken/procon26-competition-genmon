import random
import sys

field_size_max = 32
field_size_min = 20
field_threshold_min = 0.00 #threshold of obstacle
field_threshold_max = 0.25
block_size_max = 8
block_cells_min = 4
blocks_ratio_min = 0.7 #blank cells in field / cells of blocks 
blocks_ratio_max = 1.5
blocks_threshold_min = 0.05 #threshold of making random block
blocks_threshold_max = 0.50
blocks_max = 200

sys.setrecursionlimit(100000)

def rand(threshold=0.5):
    return random.random() < threshold

def draw(problem, true="1", false="0"):
    draw_block(problem[0], true, false)
    print()
    print()
    print(len(problem[1]))
    first = True
    for block in problem[1]:
        if not first:
            print()
            print()
        draw_block(block, true, false)
        first = False

def draw_block(lines, true="1", false="0"):
    first = True
    for line in lines:
        if not first:
            print()
        print("".join([(true if x else false) for x in line]), end="")
        first = False

def create():
    field_width = (int)(random.random() * (field_size_max - field_size_min) + field_size_min)
    field_height = (int)(random.random() * (field_size_max - field_size_min) + field_size_min)
    field_threshold = random.random() * (field_threshold_max - field_threshold_min) + field_threshold_min
    field, blank_blocks = create_panel(field_width, field_height, field_threshold)
    cells_min = (int) (blank_blocks * (random.random() * (blocks_ratio_max - blocks_ratio_min) + blocks_ratio_min))
    cells_sum = 0
    blocks = []
    while True:
        block, cells = create_block(random.random() * (blocks_threshold_max - blocks_threshold_min) + blocks_threshold_min)
        blocks.append(block)
        cells_sum = cells_sum + cells
        if cells_sum >= cells_min or len(blocks) == blocks_max:
            break
    return field, blocks

def create_panel(field_width, field_height, field_threshold):
    field = [[rand(field_threshold) if (i < field_height and j < field_width) else True for j in range(0, field_size_max)] for i in range(0, field_size_max)]
    if len(get_groups(field, False)[0]) > 1:
        return create_panel(field_width, field_height, field_threshold)
    n = 0
    for line in field:
        for item in line:
            if item:
                n = n + 1
    return field, n

def create_block(block_threshold):
    block = [[rand(block_threshold) for j in range(0, block_size_max)] for i in range(0, block_size_max)]
    blocks, count = get_groups(block, True)
    if count < block_cells_min:
        return create_block(block_threshold)
    max = None
    result_number = 0
    for item in blocks:
        item_length = len(item)
        if 4 <= item_length <= 16:
            if max == None or max[1] < item_length:
                max = [[item], item_length]
            elif max[1] == item_length:
                max[0].append(item);
    if max == None:
        return create_block(block_threshold)
    result = cells_to_block(max[0][random.randint(0, len(max[0]) - 1)])
    negative_blocks, count = get_groups(result, False)
    if count > 0:
        if has_hole(negative_blocks, block_size_max, block_size_max):
            return create_block(block_threshold)
    return result, max[1]

def has_hole(blocks, width, height):
    for block in blocks:
        contact_with_edge = False
        for cell in block:
            if cell[0] == 0 or cell[0] == height - 1 or cell[1] == 0 or cell[1] == width - 1:
                contact_with_edge = True
                break
        if not contact_with_edge:
            return True
    return False

def cells_to_block(cells):
    result = [[False for j in range(0, block_size_max)] for i in range(0, block_size_max)]
    for cell in cells:
        result[cell[0]][cell[1]] = True
    return result

def get_groups(block, target=True):
    block_width = len(block[0])
    block_height = len(block)
    used_block = [[False for j in range(0, block_width)] for i in range(0, block_height)]
    blocks = []
    count = 0
    def check(i, j, target=True):
        if 0 <= i < block_height and 0 <= j < block_width and block[i][j] == target and not used_block[i][j]:
            return True
        else:
            return False
    def find(i, j, target=True):
        nonlocal count
        result = []
        if not used_block[i][j]:
            count = count + 1
            used_block[i][j] = True
            result.append((i, j))
            if check(i - 1, j, target):
                result.extend(find(i - 1, j, target))
            if check(i, j - 1, target):
                result.extend(find(i, j - 1, target))
            if check(i + 1, j, target):
                result.extend(find(i + 1, j, target))
            if check(i, j + 1, target):
                result.extend(find(i, j + 1, target))
        return result
    for i in range(0, block_height):
        for j in range(0, block_width):
            if check(i, j, target):
                blocks.append(find(i, j, target))
    return blocks, count

if __name__ == "__main__":
    draw(create())
