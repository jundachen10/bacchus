# card_counter/app.py

import curses
from counter import Counter

def format_message(current_count, total_count):
    """Returns a formatted string with the current and total counts."""
    return f"Current Count: {current_count} | Total Count: {total_count}"

def main(stdscr):
    # Set up curses
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(True)  # Non-blocking input
    stdscr.clear()
    

    # Initialize counter
    counter = Counter()

    # Display instructions
    stdscr.addstr(0, 0, "Card Counting App - Press '+' or '-' to count cards")
    stdscr.addstr(1, 0, "Press 'r' to reset current count, 'q' to quit")

    while True:
        # Display the formatted message with the current and total counts
        count_message = format_message(counter.get_current_count(), counter.get_total_count())
        stdscr.addstr(3, 0, count_message + "     ")  # Extra spaces to clear old text
        stdscr.refresh()

        # Get user input
        key = stdscr.getch()

        # Handle key inputs
        if key == ord('='):
            counter.add()
        elif key == ord('-'):
            counter.subtract()
        elif key == ord('r'):
            counter.reset()
        elif key == ord('q'):
            break

# Run the curses application
if __name__ == "__main__":
    curses.wrapper(main)
