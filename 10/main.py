from sys import stdin
from itertools import takewhile
from operator import itemgetter 
from fractions import Fraction
from math import atan2

def has_view(a1, a2, asteroids_set):
    if a1 == a2:
        return True
    if a1[0] == a2[0]:
        direction = (2 * int(a1[1] < a2[1])) - 1
        for j in range(1, abs(int(a2[1] - a1[1]))):
            if (a1[0], a1[1] + direction * Fraction(j)) in asteroids_set:
                return False

    # a1, a2 = (a1 if a1[0] < a2[0] else a2, a1 if a1[0] > a2[0] else a2)
    direction = (2 * int(a1[0] < a2[0])) - 1
    for i in range(1, abs(int(a2[0] - a1[0]))):
        if (a1[0] + direction * Fraction(i), a1[1] + direction * Fraction(i) * (a2[1] - a1[1]) /( a2[0] - a1[0])) in asteroids_set:
            return False
    return True
    
    

asteroid_map = [[c == "#" for c in l.strip()] for l in stdin]

asteroids = [(Fraction(i), Fraction(j)) for i, row in enumerate(asteroid_map) for j, is_asteroid in enumerate(row) if is_asteroid]

asteroid_set = set(asteroids) 

asteroid_viewed = dict(((a, 0) for a in asteroids))

# for i in range(len(asteroids)):
#     for j in range(i + 1, len(asteroids)):
#         print(i, j)
#         a1 = asteroids[i]
#         a2 = asteroids[j]
#         # print(a1, a2, has_view(a1, a2, asteroid_set))
#         if has_view(a1, a2, asteroid_set):
#             asteroid_viewed[a1] += 1
#             asteroid_viewed[a2] += 1

# # print(*((a, c) for a, c in asteroid_viewed.items()), sep="\n")
# print("best", max(asteroid_viewed.items(), key=itemgetter(1)))

best_asteroid = (Fraction(20, 1), Fraction(23, 1))
viewable_asteroids = [a for a in asteroids if a!= best_asteroid and has_view(best_asteroid, a, asteroid_set)]
angles = [(-atan2((a[1] - best_asteroid[1]), (a[0] - best_asteroid[0])), a) for a in viewable_asteroids]
print(sorted(angles)[199])

map_asteroids = [[" " for _ in asteroid_map[0]] for _ in asteroid_map]
for i, (an, a) in enumerate(angles):
    map_asteroids[int(a[0])][int(a[1])] = "{:10.2f}".format(an)
map_asteroids[int(best_asteroid[0])][int(best_asteroid[1])] = "o"
print("\n".join(("".join(row) for row in map_asteroids)))