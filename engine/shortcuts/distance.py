from typing import Sequence


def calculate_offset(coords1, coords2, speed=1):
    x, y = coords1
    goto_x, goto_y = coords2

    diff_x, diff_y = goto_x - x, goto_y - y
    direction_x, direction_y = 0, 0

    if diff_x != 0:
        direction_x = diff_x // abs(diff_x)
        diff_x = abs(diff_x)

    if diff_y != 0:
        direction_y = diff_y // abs(diff_y)
        diff_y = abs(diff_y)

    distance = int(((x - goto_x) ** 2 + (y - goto_y) ** 2) ** .5)
    
    if not distance:
        return [x, y]
    
    x += distance // (max(diff_x, diff_y) or distance) * speed * direction_x
    y += distance // (max(diff_x, diff_y) or distance) * speed * direction_y

    return [x, y]


def is_nearbly(coords1: Sequence[int], coords2: Sequence[int], distance: int=10):
    return (
        coords1[0] + distance >= coords2[0] and
        coords1[0] - distance <= coords2[0] and
        coords1[1] + distance >= coords2[1] and
        coords1[1] - distance <= coords2[1]
    )
