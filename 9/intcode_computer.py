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
        self.relative_base = 0
        self.inputs = []

    def step(self):
        instruction = self.mem[self.pos]
        opcode = int(instruction[-2:])
        modes = instruction[:-2]
        if opcode == 99:
            return (ComputerSuspension.end(), 0)
        if opcode == 1: # add
            value = self.get_value(modes, 1) + self.get_value(modes, 2)
            self.set_value(value, modes, 3)
            current_pos = self.pos + 4
        elif opcode == 2: # multiply
            value = self.get_value(modes, 1) * self.get_value(modes, 2)
            self.set_value(value, modes, 3)
            current_pos = self.pos + 4
        elif opcode == 3: # read input
            if len(self.inputs) == 0:
                return (ComputerSuspension.wait_input(), self.pos)
            value = self.inputs.pop()
            self.set_value(value, modes, 1)
            current_pos = self.pos + 2
        elif opcode == 4: # write output
            value = self.get_value(modes, 1)
            return (ComputerSuspension.output(value), self.pos + 2)
        elif opcode == 5: # jump if true
            current_pos = self.pos + 3
            value = self.get_value(modes, 1)
            if value != 0: 
                current_pos = self.get_value(modes, 2)
        elif opcode == 6: # jump if false 
            current_pos = self.pos + 3
            value = self.get_value(modes, 1)
            if value == 0:
                current_pos = self.get_value(modes, 2)
        elif opcode == 7: # less than
            value = int(self.get_value(modes, 1) < self.get_value(modes, 2))
            self.set_value(value, modes, 3)
            current_pos = self.pos + 4
        elif opcode == 8: # equals
            value = int(self.get_value(modes, 1) == self.get_value(modes, 2))
            self.set_value(value, modes, 3)
            current_pos = self.pos + 4
        elif opcode == 9: # set relative base
            value = int(self.get_value(modes, 1))
            self.relative_base += value
            current_pos = self.pos + 2
        else:
            raise Exception("unexpected opcode %s" % opcode)
        return (None, current_pos)

    def run_until_suspended(self):
        external_action = None
        while external_action is None:
            external_action, self.pos = self.step()
        return external_action

    def get_value(self, modes, offset):
        try:
            mode = modes[-offset]
        except:
            mode = "0"
        parameter_value = int(self.mem[self.pos + offset])
        if mode == "0":
            return int(self.mem[parameter_value])
        elif mode == "1":
            return parameter_value
        elif mode == "2":
            return int(self.mem[parameter_value + self.relative_base])
        raise NotImplementedError("souldn't have a parameter mode other than O, or 1, got %s" % mode, type(mode))

    def set_value(self, value: int, modes, offset: int):
        try:
            mode = modes[-offset]
        except:
            mode = "0"
        if mode == "0":
            position = int(self.mem[self.pos + offset])
        elif mode == "1":
            raise Exception("set parameters shouldn't be in mode 1")
        elif mode == "2":
            position = int(self.mem[self.pos + offset]) + self.relative_base
        self.mem[position] = str(value)


def run_program(memory, inputs):
    outputs = []
    suspension = ComputerSuspension.output(0)
    computer = Computer(memory)
    computer.inputs = inputs
    while suspension.kind != ComputerSuspension.END:
        suspension = computer.run_until_suspended()
        if suspension.kind == ComputerSuspension.OUTPUT:
            outputs.append(suspension.value)
        elif suspension.kind == ComputerSuspension.WAIT_INPUT:
            raise Exception("unsuficient inputs provided")
    return outputs
