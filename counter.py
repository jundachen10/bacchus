
# card_counter/counter.py

class Counter:
    def __init__(self):
        self.current_count = 0
        self.total_count = 0

    def add(self):
        self.current_count += 1
        self.total_count += 1

    def subtract(self):
        self.current_count -= 1
        self.total_count -= 1

    def reset(self):
        self.current_count = 0

    def get_current_count(self):
        return self.current_count

    def get_total_count(self):
        return self.total_count
