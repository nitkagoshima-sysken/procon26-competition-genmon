import random
import sys

field_size_max = 32
field_size_min = 20
field_threshold_min = 0.00 #threshold of obstacle
field_threshold_max = 0.30
block_size_max = 8
block_cells_min = 4
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
    for i in range(0, 20):
        print("")
        draw(create_block(random.random() * (blocks_threshold_max - blocks_threshold_min) + blocks_threshold_min))

def create_panel(field_width, field_height, field_threshold):
    field = [[rand(field_threshold) if (i < field_height and j < field_width) else True for j in range(0, field_size_max)] for i in range(0, field_size_max)]
    n = 0
    for line in field:
        for item in line:
            if item:
                n = n + 1
    return field

def create_block(block_threshold):
    block = [[rand(block_threshold) for j in range(0, block_size_max)] for i in range(0, block_size_max)]
    blocks, count = get_groups(block, True)
    if count < block_cells_min:
        return create_block(block_threshold)
    max = None
    result_number = 0
    for item in blocks:
        item_length = len(item)
        if max == None or max[1] < item_length:
            max = [[item], item_length]
        elif max[1] == item_length:
            max[0].append(item);
    result = cells_to_block(max[0])
    negative_blocks, count = get_groups(result, False)
    if count > 0:
        for negative_block in negative_blocks:
            contact_with_edge = False
            for cell in negative_block:
                if cell[0] == 0 or cell[0] == block_size_max - 1 or cell[1] == 0 or cell[1] == block_size_max - 1:
                    contact_with_edge = True
                    break;
            if not contact_with_edge:
                return create_block(block_threshold)
    return result

def cells_to_block(cells):
    result = [[False for j in range(0, block_size_max)] for i in range(0, block_size_max)]
    for cell in cells[random.randint(0, len(cells) - 1)]:
        result[cell[0]][cell[1]] = True
    return result

def get_groups(block, target=True):
    used_block = [[False for j in range(0, block_size_max)] for i in range(0, block_size_max)]
    blocks = []
    count = 0
    def check(i, j, target=True):
        if 0 <= i < block_size_max and 0 <= j < block_size_max and block[i][j] == target and not used_block[i][j]:
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
    for i in range(0, block_size_max):
        for j in range(0, block_size_max):
            if check(i, j, target):
                blocks.append(find(i, j, target))
    return blocks, count

if __name__ == "__main__":
    create()
