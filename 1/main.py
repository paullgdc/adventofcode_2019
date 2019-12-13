
def fuel_necessary(weight):
    return (weight // 3) - 2

def total_fuel_necessary(weight):
    total_fuel = 0
    current = fuel_necessary(weight)
    while current > 0:
        total_fuel += current
        current = fuel_necessary(current)
    return total_fuel

with open("input.txt", "r") as f:
    modules = [int(l.strip()) for l in f]

total = sum((fuel_necessary(m) for m in modules))
print("without recursion", total)

total_recurse = sum((total_fuel_necessary(m) for m in modules))
print("with recursion", total_recurse)

