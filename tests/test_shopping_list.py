import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from src import shopping_list


class AddItemTests(unittest.TestCase):
    """R2: add an item (trimmed, non-empty, case-insensitively unique)."""

    def setUp(self):
        self.items = []

    def test_add_new_item_appends_and_confirms(self):
        message = shopping_list.add_item(self.items, "milk")
        self.assertEqual(self.items, ["milk"])
        self.assertEqual(message, "Added 'milk'.")

    def test_add_trims_surrounding_whitespace(self):
        shopping_list.add_item(self.items, "  milk  ")
        self.assertEqual(self.items, ["milk"])

    def test_add_rejects_empty_name(self):
        message = shopping_list.add_item(self.items, "")
        self.assertEqual(message, "Item name cannot be empty.")
        self.assertEqual(self.items, [])

    def test_add_rejects_whitespace_only_name(self):
        message = shopping_list.add_item(self.items, "   ")
        self.assertEqual(message, "Item name cannot be empty.")
        self.assertEqual(self.items, [])

    def test_add_rejects_exact_duplicate(self):
        shopping_list.add_item(self.items, "milk")
        message = shopping_list.add_item(self.items, "milk")
        self.assertEqual(message, "'milk' is already on the list.")
        self.assertEqual(self.items, ["milk"])

    def test_add_rejects_case_insensitive_duplicate(self):
        shopping_list.add_item(self.items, "milk")
        message = shopping_list.add_item(self.items, "MILK")
        self.assertEqual(message, "'MILK' is already on the list.")
        self.assertEqual(self.items, ["milk"])


class FormatItemsTests(unittest.TestCase):
    """R3: display all items, insertion order, one per line."""

    def test_empty_list_shows_empty_message(self):
        self.assertEqual(
            shopping_list.format_items([]), "The shopping list is empty."
        )

    def test_items_in_insertion_order_one_per_line(self):
        self.assertEqual(
            shopping_list.format_items(["milk", "bread", "eggs"]),
            "milk\nbread\neggs",
        )


class RemoveItemTests(unittest.TestCase):
    """R4: remove an item by name, case-insensitively."""

    def setUp(self):
        self.items = ["milk", "bread"]

    def test_remove_existing_item(self):
        message = shopping_list.remove_item(self.items, "bread")
        self.assertEqual(message, "Removed 'bread'.")
        self.assertEqual(self.items, ["milk"])

    def test_remove_matches_case_insensitively(self):
        message = shopping_list.remove_item(self.items, "MILK")
        self.assertEqual(message, "Removed 'milk'.")
        self.assertEqual(self.items, ["bread"])

    def test_remove_trims_surrounding_whitespace(self):
        shopping_list.remove_item(self.items, "  bread  ")
        self.assertEqual(self.items, ["milk"])

    def test_remove_missing_item_reports_error(self):
        message = shopping_list.remove_item(self.items, "eggs")
        self.assertEqual(message, "'eggs' is not on the list.")
        self.assertEqual(self.items, ["milk", "bread"])


class MainLoopTests(unittest.TestCase):
    """R1 and R5: menu loop, dispatch, and clean program termination."""

    def run_session(self, inputs):
        """Run main() with scripted keyboard input; return printed text."""
        out = io.StringIO()
        with patch("builtins.input", side_effect=inputs), redirect_stdout(out):
            shopping_list.main()
        return out.getvalue()

    def test_menu_is_shown_again_after_each_operation(self):
        output = self.run_session(["add", "milk", "display", "exit"])
        self.assertEqual(output.count(shopping_list.MENU_TEXT), 3)

    def test_each_menu_word_dispatches_to_its_operation(self):
        output = self.run_session(
            ["add", "milk", "display", "remove", "MILK", "display", "exit"]
        )
        self.assertIn("Added 'milk'.", output)
        self.assertIn("\nmilk\n", output)  # displayed, not a message
        self.assertIn("Removed 'milk'.", output)
        self.assertIn("The shopping list is empty.", output)

    def test_unknown_word_shows_error_and_repeats_menu(self):
        output = self.run_session(["bogus", "exit"])
        self.assertIn("Unknown choice.", output)
        self.assertEqual(output.count(shopping_list.MENU_TEXT), 2)

    def test_exit_ends_program_cleanly(self):
        output = self.run_session(["exit"])
        self.assertIn("Goodbye!", output)

    def test_eof_exits_cleanly(self):
        out = io.StringIO()
        with patch("builtins.input", side_effect=EOFError), redirect_stdout(out):
            shopping_list.main()
        self.assertIn("Goodbye!", out.getvalue())

    def test_keyboard_interrupt_exits_cleanly(self):
        out = io.StringIO()
        with patch("builtins.input", side_effect=KeyboardInterrupt), \
                redirect_stdout(out):
            shopping_list.main()
        self.assertIn("Goodbye!", out.getvalue())

    def test_exit_writes_no_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            os.chdir(tmp)
            try:
                self.run_session(["add", "milk", "exit"])
            finally:
                os.chdir(cwd)
            self.assertEqual(os.listdir(tmp), [])


if __name__ == "__main__":
    unittest.main()
