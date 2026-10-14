# Project Specification

## 1. Problem Definition

A Python script that adds new data and updates existing data in JSON files.
The primary use case is `angular.json`, but the script works with any valid
JSON file and has no Angular-specific logic.

Updating `angular.json` by hand is repetitive and error-prone. The script
automates this, ensuring consistency and reducing manual errors.


## 2. Scope
- Adding new keys/values to a JSON file.
- Updating existing keys/values in a JSON file.

## 3. Out of scope

- Reading or deleting data.
- Validation of Angular-specific structure or semantics.
- Any file format other than JSON.

## 4. Acceptance Criteria
- Adding a key that does not exist creates it with the given value and type.
- Updating an existing key replaces its value, preserving the JSON type given.
- Updating a non-existent key fails with a clear error and leaves the file unchanged.
- Adding a key that already exists fails with a clear error and leaves the file unchanged.
- The script reports an error for a missing or invalid JSON file.
- The file remains valid JSON after every successful operation.
- Passing an object or array as the value fails with a clear error and leaves the file unchanged (stage 1).
- Adding a nested key creates any missing intermediate keys as objects.
- If an intermediate key exists but holds a scalar value, the operation fails with a clear error and leaves the file unchanged.
- Targeting an array element fails with a clear error and leaves the file unchanged (stage 1).
- A successful operation prints its confirmation line (`added`/`updated <target> = <value>`) to stdout and exits with code 0.
- Every error prints a message to stderr, exits with a non-zero code, and leaves the file unchanged.

## 5. Usage

```bash
python src/add_to_json.py add -f <file> -t <target> -d <data>
python src/add_to_json.py update -f <file> -t <target> -d <data>
```

- `<file>`: Path to the JSON file. Required.
- `<target>`: Dot-separated path of keys to add or update. Required.
  - Supports keys nested inside objects at any depth: `key`, `key.to`, `key.to.something`, `key.to.something.else`, etc.
  - When adding, missing intermediate keys are created automatically as objects (like `mkdir -p`).
  - If an intermediate key exists but holds a scalar value, the operation fails with a clear error and leaves the file unchanged.
  - Array elements are not supported in stage 1.
  - Dots are always path separators. Literal keys containing a dot (e.g. `"my.key"`) cannot be addressed (stage-1 limitation).
- `<data>`: The value to set. Required. Must be a scalar JSON value: string, number, `true`, `false`, or `null`.
  - Strings must be passed with quotes so the JSON type is preserved: `-d '"hello"'` sets a string, `-d 123` sets a number.
  - Objects (`{}`) and arrays (`[]`) as values are not supported in stage 1. Passing one is an error and leaves the file unchanged.

## 6. Output and exit codes

- On success, the script prints one confirmation line to stdout and exits with code `0`:
  - `added <target> = <value>` after a successful add
  - `updated <target> = <value>` after a successful update
  - `<value>` is printed in its JSON form (e.g. `true`, `123`, `"hello"`).
- On error, the script prints a message to stderr naming the file, the target, and the reason. The file is left unchanged.
- Exit codes:
  - `0` — success.
  - `1` — operation or file error: missing file, invalid JSON, key already exists on add, key not found on update, non-scalar value, array element as target, intermediate key holding a scalar.
  - `2` — CLI usage error: missing or invalid arguments (argparse default).

