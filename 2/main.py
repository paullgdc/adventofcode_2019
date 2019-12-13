
memory = [int(code.strip()) for code in input().split(",")]

def setup_input(memory, noun, verb):
    memory[1] = noun
    memory[2] = verb

def step(memory, start):
    opcode = memory[start]
    if opcode == 99:
        return False
    if opcode == 1:
        memory[memory[start + 3]] = memory[memory[start + 1]] + memory[memory[start + 2]]
    elif opcode == 2:
        memory[memory[start + 3]] = memory[memory[start + 1]] * memory[memory[start + 2]]
    else:
        raise Exception("unexpected opcode")
    return True

def run_program(memory, noun, verb):
    setup_input(memory, noun, verb)
    current_pos = 0
    while step(memory, current_pos):
        current_pos += 4
    return memory[0]

output = 0
for i in range(100):
    for j in range(100):
        memory_copy = list(memory)
        output = run_program(memory_copy, i, j)
        if output == 19690720:
            break
    else:
        continue
    break

print(100 * i + j)
