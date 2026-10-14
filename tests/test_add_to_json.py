import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from src import add_to_json


class AddToJsonTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.file = Path(self.tmp.name) / "data.json"

    def write_json(self, content):
        self.file.write_text(content, encoding="utf-8")

    def run_cli(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            try:
                code = add_to_json.main(argv)
            except SystemExit as exc:  # argparse usage errors
                code = exc.code
        return code, out.getvalue(), err.getvalue()

    def assert_error(self, argv, before, expect=()):
        code, out, err = self.run_cli(argv)
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertNotEqual(err.strip(), "")
        for fragment in expect:
            self.assertIn(fragment, err)
        if before is None:
            self.assertFalse(self.file.exists())
        else:
            self.assertEqual(self.file.read_bytes(), before)

    def add_argv(self, target, data, command="add"):
        return [command, "-f", str(self.file), "-t", target, "-d", data]

    def test_add_creates_key(self):
        self.write_json('{"a": 1}')
        code, out, _ = self.run_cli(self.add_argv("b", "2"))
        self.assertEqual(code, 0)
        self.assertEqual(out, "added b = 2\n")
        self.assertEqual(json.loads(self.file.read_text()), {"a": 1, "b": 2})

    def test_add_nested_creates_intermediate_keys(self):
        self.write_json('{"a": {"b": 1}}')
        code, out, _ = self.run_cli(self.add_argv("a.c.d", '"x"'))
        self.assertEqual(code, 0)
        self.assertEqual(out, 'added a.c.d = "x"\n')
        result = json.loads(self.file.read_text())
        self.assertEqual(result, {"a": {"b": 1, "c": {"d": "x"}}})

    def test_add_existing_key_fails(self):
        before = '{"a": 1}'
        self.write_json(before)
        self.assert_error(
            self.add_argv("a", "2"),
            before.encode(),
            expect=(str(self.file), "'a'", "key already exists"),
        )

    def test_update_replaces_value(self):
        self.write_json('{"a": {"b": 1}}')
        code, out, _ = self.run_cli(self.add_argv("a.b", '"new"', command="update"))
        self.assertEqual(code, 0)
        self.assertEqual(out, 'updated a.b = "new"\n')
        self.assertEqual(json.loads(self.file.read_text()), {"a": {"b": "new"}})

    def test_update_missing_key_fails(self):
        before = '{"a": 1}'
        self.write_json(before)
        self.assert_error(
            self.add_argv("missing", "2", command="update"),
            before.encode(),
            expect=(str(self.file), "'missing'", "key not found"),
        )
        before_nested = '{"a": {}}'
        self.write_json(before_nested)
        self.assert_error(
            self.add_argv("a.b", "2", command="update"),
            before_nested.encode(),
            expect=(str(self.file), "'a.b'", "key not found"),
        )

    def test_missing_file_fails(self):
        self.assert_error(
            self.add_argv("a", "1"),
            before=None,
            expect=(str(self.file), "file not found"),
        )

    def test_invalid_json_file_fails(self):
        before = "{not valid json"
        self.write_json(before)
        self.assert_error(
            self.add_argv("a", "1"),
            before.encode(),
            expect=(str(self.file), "invalid JSON"),
        )

    def test_object_value_rejected(self):
        before = '{"a": 1}'
        self.write_json(before)
        self.assert_error(
            self.add_argv("b", '{"x": 1}'),
            before.encode(),
            expect=(str(self.file), "'b'", "objects and arrays"),
        )

    def test_array_value_rejected(self):
        before = '{"a": 1}'
        self.write_json(before)
        self.assert_error(
            self.add_argv("b", "[1, 2]"),
            before.encode(),
            expect=(str(self.file), "'b'", "objects and arrays"),
        )

    def test_scalar_intermediate_key_fails(self):
        before = '{"a": "hello"}'
        self.write_json(before)
        self.assert_error(
            self.add_argv("a.b", "1"),
            before.encode(),
            expect=(str(self.file), "'a.b'", "scalar"),
        )
        self.assert_error(
            self.add_argv("a.b", "1", command="update"),
            before.encode(),
            expect=(str(self.file), "'a.b'", "scalar"),
        )

    def test_array_target_fails(self):
        before = '{"a": [1, 2]}'
        self.write_json(before)
        self.assert_error(
            self.add_argv("a.0", "5"),
            before.encode(),
            expect=(str(self.file), "'a.0'", "array"),
        )
        self.assert_error(
            self.add_argv("a.0", "5", command="update"),
            before.encode(),
            expect=(str(self.file), "'a.0'", "array"),
        )

    def test_usage_error_exits_with_code_2(self):
        self.write_json('{"a": 1}')
        code, out, err = self.run_cli(["add", "-f", str(self.file), "-t", "a"])
        self.assertEqual(code, 2)
        self.assertNotEqual(err.strip(), "")

    def test_data_types_preserved(self):
        cases = [('"text"', "text"), ("123", 123), ("true", True), ("null", None)]
        for raw, expected in cases:
            for command, initial in (("add", "{}"), ("update", '{"key": "old"}')):
                with self.subTest(raw=raw, command=command):
                    self.write_json(initial)
                    code, out, _ = self.run_cli(self.add_argv("key", raw, command=command))
                    self.assertEqual(code, 0)
                    verb = "added" if command == "add" else "updated"
                    self.assertEqual(out, f"{verb} key = {raw}\n")
                    result = json.loads(self.file.read_text())["key"]
                    self.assertEqual(result, expected)
                    self.assertIs(type(result), type(expected))


if __name__ == "__main__":
    unittest.main()
