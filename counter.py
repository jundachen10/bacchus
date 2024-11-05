
# card_counter/counter.py

class Counter:
    
    
     # Define the original counting system tags
    ORIGINAL_TAGS = {
        '1': 0, '2': 1, '3': 1, '4': 1, '5': 1,
        '6': -1, '7': -1, '8': -1, '9': -1, '0': 0
    }
    
    # Define tags for each card based on Dragon Bonus counting system (Ace, 2, 3, 4, 5, 6, 7, 8, 9, T)
    DRAGON_BONUS_TAGS = {
        '1': 2, '2': 3, '3': 3, '4': 1, '5': 0,
        '6': 0, '7': -1, '8': -2, '9': -2, '0': -1
    }
    
    
    def __init__(self):
        self.original_count = 0
        self.dragon_bonus_count = 0

    def add_card(self, card):
        # Get tags for both systems and update their respective counts
        original_tag = self.ORIGINAL_TAGS.get(card, 0)
        dragon_bonus_tag = self.DRAGON_BONUS_TAGS.get(card, 0)

        self.original_count += original_tag
        self.dragon_bonus_count += dragon_bonus_tag

    def reset(self):
        self.original_count = 0
        self.dragon_bonus_count = 0

    def get_original_count(self):
        return self.original_count

    def get_dragon_bonus_count(self):
        return self.dragon_bonus_count