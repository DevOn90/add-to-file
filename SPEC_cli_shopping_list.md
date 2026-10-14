# SPEC — CLI Shopping List

> Status: **approved** by the developer on 2026-10-14 as the
> requirements for this project. Implemented in `src/shopping_list.py`
> and verified by `tests/test_shopping_list.py` on 2026-10-14; §6
> updated with the concrete function names (AGENTS.md §9).

## 1. Purpose

- **What we are building:** a small command-line shopping list
  application written in Python.
- **Who will use it:** the developer, who is learning programming.
- **What problem it solves:** it keeps track of items to buy through a
  few simple operations, and serves as a learning exercise for
  understanding how a program works — especially how its functions
  relate to each other.

## 2. Scope

**Included:**

- An interactive menu loop: the program starts, shows a menu
  (add / display / remove / exit), and keeps running until the user
  chooses exit.
- Add an item to the shopping list.
- Display all items in the list.
- Remove an item from the list.
- Exit the application.
- Automated tests using Python's built-in `unittest` framework.

**Explicitly excluded (unless the developer later decides otherwise):**

- Item metadata such as quantities, categories, or prices.
- Multiple lists, sharing, or synchronization.
- A graphical or web user interface.
- Packaging or distribution beyond running the program locally.
- Persistence: the list is kept in memory only and resets on every
  start (may be added later).

**Decisions (from developer Q&A, 2026-10-14):**

- Interaction: interactive menu loop (not command-line arguments).
- Storage: in-memory only; the list starts empty on each run.
- Items must be unique: adding a duplicate item is rejected;
  items are identified by name (e.g. when removing).
- Testing: yes, using the standard-library `unittest` module
  (not pytest).
- Error behaviors in §3–§4 (empty-name rejection, invalid menu choice
  handling, remove-missing-item error, no file written on exit):
  **approved** by the developer after review on 2026-10-14
  (initially drafted unlabeled; labeling rule added to AGENTS.md §9).
- **Approved** in the four-pass spec review on 2026-10-14:
  - Menu options are selected by typing a word: `add`, `display`,
    `remove`, `exit`.
  - Display prints items in insertion order, one item per line,
    without numbering.
  - Item names are trimmed of leading/trailing whitespace; a name
    that is empty after trimming is rejected.
  - Uniqueness and removal matching are case-insensitive
    ("Milk" = "milk"); the list displays the name as first typed.
  - Ctrl+C / end-of-input exits the program cleanly, without a
    traceback.
  - Python version: "Python 3", no specific minimum.
  - Design approach: **Option B — plain functions + thin
    controller** (operations never do terminal I/O; `main()` owns all
    input/print and dispatches). Chosen over all-in-one procedural,
    class-based, and global-state alternatives on 2026-10-14.

## 3. Requirements and Acceptance Criteria

**R1 — Interactive menu loop.**
The program displays a menu with four operations, reads the user's
choice as a typed word (`add`, `display`, `remove`, `exit`), performs
it, and shows the menu again until the user types `exit`.
*Satisfied when:* each of the four words triggers the correct
operation, any other input is rejected with a message followed by the
menu again, and the program terminates via `exit`.

**R2 — Add an item.**
The program asks for an item name, trims leading/trailing whitespace,
and adds it to the list. A name that is empty after trimming, or that
matches an existing item case-insensitively, is rejected with a clear
message and the list is left unchanged. The item is stored and
displayed as first typed (after trimming).
*Satisfied when:* a new name appears in the list; adding a duplicate
("Milk" vs "milk"), an empty name, or a whitespace-only name is
rejected with a message.

**R3 — Display all items.**
The program prints every item currently in the list, in insertion
order, one item per line. If the list is empty, it prints a clear
"list is empty" message instead.
*Satisfied when:* the output lists exactly the items added so far,
minus any removals, in the order they were added.

**R4 — Remove an item.**
The program asks for an item name and removes it if present, matching
case-insensitively. If the name is not in the list, it reports a
clear error and leaves the list unchanged.
*Satisfied when:* an existing item no longer appears in Display
(e.g. typing "MILK" removes "milk"); removing a missing item produces
an error message and no change.

**R5 — Exit and interruption.**
Typing `exit` ends the program. Pressing Ctrl+C or signalling
end-of-input (Ctrl+D) also ends the program cleanly, without a
Python traceback. The list is not saved.
*Satisfied when:* the process terminates without an error or
traceback and without writing any file (derived from: in-memory
storage decision).

**R6 — Automated tests.**
A `unittest` test suite covers the behaviors above: normal cases
(add, display, remove, exit), boundary cases (empty list), and error
cases (duplicate add, empty or whitespace-only name, removing a
missing item, invalid menu word).
*Satisfied when:* the suite runs with the standard-library `unittest`
runner and all tests pass.

## 4. Inputs, Outputs, and Errors

**Inputs:**

- A menu choice: one of the words `add`, `display`, `remove`, `exit`.
- An item name entered when adding or removing (a text string;
  leading/trailing whitespace is trimmed before use).
- Ctrl+C or end-of-input (Ctrl+D) at any prompt: the program exits
  cleanly.

**Outputs and side effects:**

- The menu text, the current list contents (insertion order, one item
  per line), and confirmation or error messages, all printed to the
  terminal.
- No files are read or written; the only state is the in-memory list.

**Expected error behavior and edge cases:**

- Invalid menu word (not one of the four): print an error message and
  show the menu again.
- Item name empty after trimming: rejected with a message; the list
  is unchanged.
- Duplicate item name on Add (case-insensitive): rejected with a
  message; the list is unchanged.
- Removing a name that is not in the list (case-insensitive):
  clear error message; the list is unchanged.
- Displaying an empty list: a clear "list is empty" message, not an
  error.
- Ctrl+C / end-of-input: clean exit, no traceback.

## 5. Constraints and Limitations

- Python 3 (no specific minimum version), standard library only;
  no third-party dependencies.
- In-memory storage only: all items are lost when the program exits.
- Single user, single list, local terminal.
- Items are plain text names; no quantities, categories, or prices.
- Uniqueness and removal matching are case-insensitive; the original
  casing (as first typed, after trimming) is preserved for display.

## 6. Program Flow and Component Relationships

**Entry point:** `python src/shopping_list.py` runs the
`if __name__ == "__main__": main()` block, which starts the menu
loop.

**Main execution steps (repeated until Exit):**

1. Show the menu (`add` / `display` / `remove` / `exit`).
2. Read and validate the user's menu word.
3. Dispatch to the chosen operation.
4. The operation reads any further input it needs, updates or reads
   the list, and prints the result.
5. Return to step 1 — unless the choice was `exit`, which ends the
   loop and terminates the program. Ctrl+C / end-of-input at any
   prompt also ends the program cleanly.

**Component responsibilities** (as implemented in
`src/shopping_list.py`):

- **Main loop / controller — `main()`:** owns the menu cycle. Prints
  `MENU_TEXT`, reads and validates the menu word, calls the matching
  operation, and ends the program on `exit`, Ctrl+C, or end-of-input
  (`try/except (EOFError, KeyboardInterrupt)`). This is where invalid
  menu words are handled. `main()` performs all `input()`/`print()`;
  the operations perform none.
- **Add operation — `add_item(items, name) -> str`:** trims the name,
  validates it (non-empty, unique case-insensitively), updates the
  list, and returns the confirmation or rejection message.
- **Display operation — `format_items(items) -> str`:** returns the
  list as text (insertion order, one per line) or the empty-list
  message; `main()` prints the returned text.
- **Remove operation — `remove_item(items, name) -> str`:** removes
  the item if present (trimmed, case-insensitive match) and returns
  the confirmation or error message.
- **List data:** a single in-memory Python list created and owned by
  `main()`; the operations receive it as a parameter and share it
  that way. No global state.

**Data flow:** user input flows into `main()`, which passes control
to one operation; the operation reads or modifies the shared list and
returns a message string, which `main()` prints to the terminal.

**Error handling locations:** menu-word validation and Ctrl+C /
end-of-input handling happen in the controller; item-name validation
(empty after trimming, duplicate, missing) happens inside the
relevant operation.
