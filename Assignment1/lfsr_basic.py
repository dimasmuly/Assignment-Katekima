# lfsr_basic.py

class BasicLFSR:
    def __init__(self, initial_state):
        self.state = initial_state

    def get_state(self):
        return self.state

    def next_bit(self):
        # Feedback function: XOR of specific bits
        feedback = int(self.state[1]) ^ int(self.state[2])  # XOR R1 and R2
        self.state = self.state[1:] + str(feedback)  # Shift left and add feedback
        return feedback

def main():
    lfsr = BasicLFSR("0110")
    for _ in range(20):
        current_state = lfsr.get_state()
        next_bit = lfsr.next_bit()
        print(f"State: {current_state}, Next Bit: {next_bit}")

if __name__ == "__main__":
    main()