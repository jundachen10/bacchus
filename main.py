# card_counter/app.py

import curses
import json
from counter import Counter

def save_to_json(hand_history):
    """Saves hand history to a JSON file."""
    with open('hand_history.json', 'w') as f:
        json.dump(hand_history, f, indent=4)  # Write with indentation for readability


def format_message(current_count, total_count):
    """Returns a formatted string with the current and total counts."""
    return f"Current Count: {current_count} | Total Count: {total_count}"


# this will error out when it reaches max terminal screen length cuz .addstr
def display_hand_history(stdscr, hand_history):
    """Displays the result history of each hand along with the running counts."""
    stdscr.addstr(5, 0, "Hand History:")
    for i, hand in enumerate(hand_history, start=1):
        input_sequence = ', '.join(hand['inputs'])  # Join inputs into a string
        stdscr.addstr(
            i + 5,
            0,
            f"Hand {i}: {hand['result']} | Running Count: {hand['running_count']} | Inputs: {input_sequence}"
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

    # Display instructions
    stdscr.addstr(0, 0, "Card Counting App - Press '2' through '9' to count cards")
    stdscr.addstr(1, 0, "Press 'r' to reset current count, 'q' to quit")

    while True:
        # Display the formatted message with the current and total counts
        count_message = format_message(
            counter.get_current_count(), counter.get_total_count()
        )
        stdscr.addstr(3, 0, count_message + "     ")  # Extra spaces to clear old text
        stdscr.refresh()

        # Get user input
        key = stdscr.getch()
        action = None

        # Handle key inputs
        if key in [ord("0"), ord("1")]:
            current_inputs.append(chr(key))
            action = "No Change"
        elif key in [ord("2"), ord("3"), ord("4"), ord("5")]:
            counter.add()
            current_inputs.append(chr(key))
            action = "Add"
        elif key in [ord("6"), ord("7"), ord("8"), ord("9")]:
            counter.subtract()
            current_inputs.append(chr(key))
            action = "Subtract"
            
        # Key inputs for game results    
        elif key == ord("p"):
            hand_history.append(
                {
                    "result": "Player Win",
                    "running_count": counter.get_current_count(),
                    "inputs": current_inputs.copy(),
                }
            )
            display_hand_history(stdscr, hand_history)
            current_inputs = []
        elif key == ord("b"):
            hand_history.append(
                {
                    "result": "Banker Win",
                    "running_count": counter.get_current_count(),
                    "inputs": current_inputs.copy(),
                }
            )
            display_hand_history(stdscr, hand_history)
            current_inputs = []
        elif key == ord("t"):
            hand_history.append(
                {
                    "result": "Tie",
                    "running_count": counter.get_current_count(),
                    "inputs": current_inputs.copy(),
                }
            )
            display_hand_history(stdscr, hand_history)
            current_inputs = []
            
        elif key == ord("s"):  # Save key
            save_to_json(hand_history)
            stdscr.addstr(4, 0, "Hand history saved to 'hand_history.json'     ")  # Feedback message
            stdscr.refresh()
            stdscr.getch()  # Wait for a key press to continue
            
        elif key == ord("q"):
            break


# Run the curses application
if __name__ == "__main__":
    curses.wrapper(main)
