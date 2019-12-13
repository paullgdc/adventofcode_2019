from intcode_computer import run_program

memory = [code.strip() for code in input().split(",")]
memory.extend(("0" for _ in range(1 << 16)))

# Part 1
# outputs = run_program(memory, [1])
# print(outputs)

# Part 2
outputs = run_program(memory, [2])
print(outputs)
