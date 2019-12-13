
wires = [
    input().split(","),
    input().split(","),
]

def build_paths(directions):
    pos = (0, 0)
    old_pos = (0, 0)
    current_length = 0
    hor_path = []
    vert_path = []
    for direction in directions:
        cardinal = direction[0]
        distance = int(direction[1:])
        if cardinal == "R" or cardinal == "L":
            if cardinal == "R":
                pos = (pos[0] + distance, pos[1])
            elif cardinal == "L":
                pos = (pos[0] - distance, pos[1])
            hor_path.append((pos[1], (min(pos[0], old_pos[0]), max(pos[0], old_pos[0])), (old_pos[0], current_length)))
        if cardinal == "U" or cardinal == "D":
            if cardinal == "U":
                pos = (pos[0], pos[1] + distance)
            elif cardinal == "D":
                pos = (pos[0], pos[1]  - distance)
            vert_path.append((pos[0], (min(pos[1], old_pos[1]), max(pos[1], old_pos[1])), (old_pos[1],current_length)))
        current_length += distance
        old_pos = pos
    return hor_path, vert_path

def find_intersec(hor_path, vert_path):
    if hor_path[1][0] <= vert_path[0] <= hor_path[1][1] \
        and vert_path[1][0] <= hor_path[0] <= vert_path[1][1]:
        return (vert_path[0], hor_path[0], hor_path[2][1] + vert_path[2][1] + abs(vert_path[0] - hor_path[2][0]) + abs(hor_path[0] - vert_path[2][0]))
    return None

pathes = [build_paths(wire) for wire in wires]
print(pathes)
intersections = []
for hor_path in pathes[0][0]:
    for vert_path in pathes[1][1]:
        intersection = find_intersec(hor_path, vert_path)
        if intersection is not None:
            intersections.append(intersection)

for hor_path in pathes[0][1]:
    for vert_path in pathes[1][0]:
        intersection = find_intersec(hor_path, vert_path)
        if intersection is not None:
            intersections.append(intersection)

print(intersections)
# print(min((abs(x) + abs(y) for x, y in intersections if x != 0 or y != 0)))
print(min((intersec[2] for intersec in intersections if intersec[2] > 0)))