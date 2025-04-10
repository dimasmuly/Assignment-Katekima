# lfsr_general.py

class GeneralLFSR:
    def __init__(self, size, taps, initial_state):
        self.size = size
        self.taps = taps
        self.state = initial_state

    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state

    def next_bit(self):
        feedback = 0
        for tap in self.taps:
            feedback ^= int(self.state[tap])  # XOR for all tap positions
        self.state = self.state[1:] + str(feedback)  # Shift left and add feedback
        return feedback

def main():
    # Instantiate General LFSR to match Basic LFSR case
    taps = [1, 2]  # Corresponds to R1 and R2
    lfsr = GeneralLFSR(4, taps, "0110")
    
    for _ in range(20):
        current_state = lfsr.get_state()
        next_bit = lfsr.next_bit()
        print(f"State: {current_state}, Next Bit: {next_bit}")

if __name__ == "__main__":
    main()