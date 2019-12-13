
memory = [code.strip() for code in input().split(",")]

from dataclasses import dataclass

@dataclass
class ComputerSuspension:
    END = 0
    WAIT_INPUT = 1
    OUTPUT = 2

    def __init__(self, kind, value=None):
        self.kind = kind
        self.value = value

    @classmethod
    def end(cls):
        return cls(cls.END)

    @classmethod
    def wait_input(cls):
        return cls(cls.WAIT_INPUT)

    @classmethod
    def output(cls, value):
        return cls(cls.OUTPUT, value)

class Computer:
    def __init__(self , mem):
        self.mem = mem
        self.pos = 0
        self.inputs = []

    def run_until_suspended(self):
        external_action = None
        while external_action is None:
            external_action, self.pos = step(self.mem, self.pos, self.inputs)
        return external_action

def get_value(instruction_pos: int, modes, offset: int, memory):
    try:
        mode = modes[-offset]
    except:
        mode = "0"
    parameter_value = int(memory[instruction_pos + offset])
    if mode == "1":
        return parameter_value
    elif mode == "0":
        return int(memory[parameter_value])
    raise NotImplementedError("souldn't have a parameter mode other than O, or 1, got %s" % mode, type(mode))

def set_value(value: int, instruction_pos: int, offset: int, memory):
    position = int(memory[instruction_pos + offset])
    memory[position] = str(value)


def step(mem, start, inputs):
    instruction = mem[start]
    opcode = int(instruction[-2:])
    modes = instruction[:-2]
    if opcode == 99:
        return (ComputerSuspension.end(), 0)
    if opcode == 1: # add
        value = get_value(start, modes, 1, mem) + get_value(start, modes, 2, mem)
        set_value(value, start, 3, mem)
        current_pos = start + 4
    elif opcode == 2: # multiply
        value = get_value(start, modes, 1, mem) * get_value(start, modes, 2, mem)
        set_value(value, start, 3, mem)
        current_pos = start + 4
    elif opcode == 3: # read input
        if len(inputs) == 0:
            return (ComputerSuspension.wait_input(), start)
        value = inputs.pop()
        set_value(value, start, 1, mem)
        current_pos = start + 2
    elif opcode == 4: # write output
        value = get_value(start, modes, 1, mem)
        return (ComputerSuspension.output(value), start + 2)
    elif opcode == 5: # jump if true
        current_pos = start + 3
        value = get_value(start, modes, 1, mem)
        if value != 0: 
            current_pos = get_value(start, modes, 2, mem)
    elif opcode == 6: # jump if false 
        current_pos = start + 3
        value = get_value(start, modes, 1, mem)
        if value == 0:
            current_pos = get_value(start, modes, 2, mem)
    elif opcode == 7: # less than
        value = int(get_value(start, modes, 1, mem) < get_value(start, modes, 2, mem))
        set_value(value, start, 3, mem)
        current_pos = start + 4
    elif opcode == 8: # equals
        value = int(get_value(start, modes, 1, mem) == get_value(start, modes, 2, mem))
        set_value(value, start, 3, mem)
        current_pos = start + 4
    else:
        raise Exception("unexpected opcode %s", opcode)
    return (None, current_pos)

def run_program(memory, inputs):
    outputs = []
    suspension = ComputerSuspension.output(0)
    computer = Computer(memory)
    computer.inputs = inputs
    while suspension.kind != ComputerSuspension.END:
        suspension = computer.run_until_suspended()
        if suspension.kind == ComputerSuspension.OUTPUT:
            outputs.append(suspension.value)
    return outputs


outputs = run_program(memory, [5])
print(outputs)
