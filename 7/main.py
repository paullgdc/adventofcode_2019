from intcode_computer import Computer, ComputerSuspension

memory = [code.strip() for code in input().split(",")]

def permutations(elements):
    if len(elements) == 0:
        yield []
        return
    for i, element in enumerate(elements):
        for perm in permutations(elements[: i] + elements[i + 1:]):
            yield [element] + perm

def init_amplifiers(signals, mem):
    computers = [Computer(list(mem)) for _ in signals]
    for signal, computer in zip(signals, computers):
        computer.inputs.append(signal)
        computer.run_until_suspended()
    return computers

def amplifier_loop(first_ampli_input, computers):
    current_output = first_ampli_input
    for computer in computers:
        computer.inputs.append(current_output)
        suspension: ComputerSuspension = computer.run_until_suspended()
        if suspension.kind == ComputerSuspension.OUTPUT:
            current_output = suspension.value
        elif suspension.kind == ComputerSuspension.END:
            return (True, 0)
        else:
            raise Exception("can't wait for input")
    return (False, current_output)

def run_amplifiers(signals, mem):
    computers = init_amplifiers(signals, mem)
    loop_output = 0
    loop_stop = False
    while not loop_stop:
        loop_input = loop_output
        loop_stop,loop_output = amplifier_loop(loop_input, computers)
    return loop_input

for signals in permutations(list(range(5, 10))):
    print(run_amplifiers(signals, memory))

print(max((
    run_amplifiers(signals, memory) for signals in permutations(list(range(5, 10)))
)))
