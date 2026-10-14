"""Command-line shopping list (see SPEC.md).

The item operations in this module never read from the keyboard or
print to the terminal. They receive the shopping list as a parameter
and return a message string. main() owns all input/output and calls
these operations.
"""


def add_item(items, name):
    """Add name to items, or reject it. Return the message to show.

    The name is trimmed of surrounding whitespace. A name that is
    empty after trimming, or already on the list (compared
    case-insensitively), is rejected and the list is left unchanged.
    """
    name = name.strip()
    if not name:
        return "Item name cannot be empty."
    if name.lower() in (item.lower() for item in items):
        return f"'{name}' is already on the list."
    items.append(name)
    return f"Added '{name}'."


def format_items(items):
    """Return the list as text: insertion order, one item per line."""
    if not items:
        return "The shopping list is empty."
    return "\n".join(items)


def remove_item(items, name):
    """Remove name from items (case-insensitive). Return the message.

    The name is trimmed before matching. If no item matches, the list
    is left unchanged.
    """
    name = name.strip()
    for item in items:
        if item.lower() == name.lower():
            items.remove(item)
            return f"Removed '{item}'."
    return f"'{name}' is not on the list."


MENU_TEXT = "Menu: add | display | remove | exit"


def main():
    """Run the menu loop until the user exits (R1, R5).

    Owns all keyboard input and terminal output. One shared list is
    passed to the item operations. `exit`, Ctrl+C, or end-of-input
    (Ctrl+D) end the program cleanly, without a traceback.
    """
    items = []
    print("Shopping list.")
    while True:
        try:
            print(MENU_TEXT)
            choice = input("> ").strip().lower()
            if choice == "add":
                print(add_item(items, input("Item name: ")))
            elif choice == "display":
                print(format_items(items))
            elif choice == "remove":
                print(remove_item(items, input("Item name: ")))
            elif choice == "exit":
                print("Goodbye!")
                break
            else:
                print("Unknown choice.")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
