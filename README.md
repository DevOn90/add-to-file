# add-to-file

A small Python command-line tool for adding or updating scalar values in a JSON file.

## Requirements

- Python 3

## Usage

Run the script from the repository root:

```bash
python3 src/add_to_json.py <command> --file <path> --target <key.path> --data <json-value>
```

Commands:

- `add` — add a key that does not already exist.
- `update` — replace the value of an existing key.

Options:

- `-f`, `--file` — path to the JSON file to edit.
- `-t`, `--target` — dot-separated path to the key.
- `-d`, `--data` — a JSON scalar value: a string, number, boolean, or `null`.

## Examples

Add a top-level value:

```bash
python3 src/add_to_json.py add -f settings.json -t theme -d '"dark"'
```

Add a nested value (missing intermediate objects are created):

```bash
python3 src/add_to_json.py add -f settings.json -t editor.fontSize -d 14
```

Update an existing value:

```bash
python3 src/add_to_json.py update -f settings.json -t editor.fontSize -d 16
```

String values must be quoted as JSON strings, so the shell argument includes the quotes, as in `-d '"dark"'`.

## Behavior and limitations

- The target path uses dots to separate object keys. Array indexes are not supported.
- `add` fails if the target key already exists. `update` fails if the target key does not exist.
- `add` creates missing intermediate objects; `update` does not.
- Object and array values are not supported for `--data`.
- The input file must contain valid JSON with an object at its root.
- On success, the file is written with two-space indentation and a trailing newline. A status message is printed.
- Errors are printed to standard error. Operation errors exit with status `1`; command-line usage errors exit with status `2`.

## Tests

Run the test suite from the repository root:

```bash
python3 -m unittest discover -s tests
```