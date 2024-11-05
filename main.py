# card_counter/app.py

import curses
import json
from counter import Counter


def save_to_json(hand_history):
    """Saves hand history to a JSON file."""
    with open("hand_history.json", "w") as f:
        json.dump(hand_history, f, indent=4)  # Write with indentation for readability


def format_message(original_count, dragon_bonus_count, cards_drawn):
    """Returns a formatted string with the current and total counts."""
    return (
        f"Original Count: {original_count} | Dragon Bonus Count: {dragon_bonus_count} | "
        f"Total Cards Drawn: {cards_drawn}"
    )


def display_hand_history(stdscr, hand_history):
    """Displays the last 10 results of each hand along with the running counts."""
    stdscr.clear()
    stdscr.addstr(5, 0, "Hand History (showing last 10):")

    # Calculate the starting index for the last 10 entries, or start at 0 if fewer than 10
    start_index = max(0, len(hand_history) - 10)

    for i, hand in enumerate(hand_history[start_index:], start=1):
        input_sequence = ", ".join(hand["inputs"])  # Join inputs into a string
        stdscr.addstr(
            i + 5,
            0,
            f"Hand {start_index + i}: {hand['result']} | Original Count: {hand['original_count']} | "
            f"Dragon Bonus Count: {hand['dragon_bonus_count']} | Inputs: {input_sequence}",
        )

    stdscr.refresh()


def main(stdscr):
    # Set up curses
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(True)  # Non-blocking input
    stdscr.clear()

    # Initialize counter
    counter = Counter()
    hand_history = []
    # List to store each hand result and running count as dictionaries
    current_inputs = []  # List to track inputs for the current hand
    cards_drawn = 0  # Counter for total cards drawn

    # Display instructions
    stdscr.addstr(0, 0, "Card Counting App - Press '2' through '9' to count cards")
    stdscr.addstr(1, 0, "Press 'r' to reset current count, 'q' to quit")

    while True:
        # Display the formatted message with the current and total counts
        count_message = format_message(
            counter.get_original_count(), counter.get_dragon_bonus_count(), cards_drawn
        )
        stdscr.addstr(3, 0, count_message + "     ")  # Extra spaces to clear old text
        stdscr.refresh()

        # Get user input
        key = stdscr.getch()
        action = None

        # Handle card inputs (A, 2-9, T for tens and face cards)
        if key in [
            ord("1"),
            ord("2"),
            ord("3"),
            ord("4"),
            ord("5"),
            ord("6"),
            ord("7"),
            ord("8"),
            ord("9"),
            ord("0"),
        ]:
            card = chr(key)
            counter.add_card(card)
            current_inputs.append(card)
            cards_drawn += 1

        # Key inputs for game results
        elif key == ord("p"):
            hand_history.append(
                {
                    "result": "Player Win",
                    "original_count": counter.get_original_count(),
                    "dragon_bonus_count": counter.get_dragon_bonus_count(),
                    "inputs": current_inputs.copy(),
                }
            )
            display_hand_history(stdscr, hand_history)
            current_inputs = []
        elif key == ord("b"):
            hand_history.append(
                {
                    "result": "Banker Win",
                    "original_count": counter.get_original_count(),
                    "dragon_bonus_count": counter.get_dragon_bonus_count(),
                    "inputs": current_inputs.copy(),
                }
            )
            display_hand_history(stdscr, hand_history)
            current_inputs = []
        elif key == ord("t"):
            hand_history.append(
                {
                    "result": "Tie",
                    "original_count": counter.get_original_count(),
                    "dragon_bonus_count": counter.get_dragon_bonus_count(),
                    "inputs": current_inputs.copy(),
                }
            )
            display_hand_history(stdscr, hand_history)
            current_inputs = []

        elif key == ord("s"):  # Save key
            save_to_json(hand_history)
            stdscr.addstr(
                4, 0, "Hand history saved to 'hand_history.json'     "
            )  # Feedback message
            stdscr.refresh()
            stdscr.getch()  # Wait for a key press to continue

        elif key == ord("r"):
            counter.reset()
            current_inputs = []

        elif key == ord("q"):
            break


# Run the curses application
if __name__ == "__main__":
    curses.wrapper(main)
