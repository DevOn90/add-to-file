# Specification

## CLI
| Argument | Purpose | Required? |
|---|---|---|
| `-p`, `--path` | Path to the JSON file | Yes |
| `-c`, `--create` | Create a key or append a value | One operation required |
| `-r`, `--read` | Read a value or the entire document | One operation required |
| `-u`, `--update` | Replace an existing value | One operation required |
| `-d`, `--delete` | Delete a key or remove a value | One operation required |
| `-t`, `--target` | JSON path to the target | Required for mutations |
| `--data` | Value used by the operation | Depends on the operation |

- Only one operation should be allowed per invocation.
- It is an error to specify more than one operation at a time.
- Both `--target` and `--data` are required for mutating operations (`--create`, `--update`, `--delete`).
- The `--read` operation does not require `--target` or `--data`.
- The `--data` argument is only used by mutating operations.
- The `--target` argument is required for all mutating operations.
- The `--path` argument is required for all operations.
- The `--create`, `--update`, and `--delete` operations are considered mutating operations.
- The `--read` operation is considered a non-mutating operation.
- Both short and long forms of the arguments are supported.

## Data types

The script should preserve JSON data types.

Example:
```
--data '"string"'
--data '123'
--data 'true'
--data 'null'
--data '[1, 2, 3]'
--data '{"key": "value"}'
```

- The quotation marks around strings are required to preserve the JSON data type.
- Unquoted values will result in errors or incorrect data type interpretation.
- `--data null` is a valid JSON value, but the script interprets the resulting Python None as though `--data` wasn't provided. This means you cannot currently create or update a value to JSON `null` as intended.
The fix is to track whether the argument was supplied separately from the parsed value. If no argument was supplied, it should be treated as though `--data` was not provided, even if the parsed value is `None`.

## Define CRUD semantics

Rules:

| Operation | Target exists? | Expected behavior |
|---|---|---|
| Create | No | Create the key |
| Create | Yes | Return an error without changing the file |
| Read | Yes | Return the value |
| Read | No | Return a clear error |
| Update | Yes | Replace the existing value |
| Update | No | Return an error without changing the file |
| Delete | Yes | Delete the target |
| Delete | No | Return a clear error |

For deletion, it is important to check whether the target exists before attempting to delete it. If the target does not exist, a clear error should be returned without modifying the file.

Similarly, for updates, the target must exist; otherwise, an error should be returned without changing the file. For creation, the target must not exist; attempting to create an existing key should result in an error.

- Deletion behaviour (both are valid):
  - Delete entire tag
  ```
  # Delete the entire tags array
  python modify_json.py -p data.json -d -t user.tags
  ```
  - Delete a specified element from the array
  ```
  # Remove the specified value from the array
  python modify_json.py -p data.json -d -t user.tags --data '"admin"'
  ```

## How target path works

```
-t "target" = {"target": ""}
-t "target.path" = {"target": {"path": ""}}
-t "another.target.path" = {"another": {"target": {"path": ""}}}
-t "target.[]" = {"target": ["", "", ""]}
-t "target.[].path" = {"target": [{"path": ""}, {"path": ""}]}
-t "target.[].[]" = {"target": [["", ""], ["", ""]]}
```

Design decisions:
- Existing array indices can be read, updated, or deleted.
- Creation at the next index appends an element.
- Creation at an index beyond the next available position fails.
- Negative indices are not accepted for creation.

## Introduce automated testing

Structure:
```
json-crud/
├── modify_json.py
├── tests/
│   ├── test_create.py
│   ├── test_read.py
│   ├── test_update.py
│   ├── test_delete.py
│   ├── test_data_types.py
│   ├── test_arrays.py
│   └── test_errors.py
├── README.md
└── pyproject.toml
```

The tests should use temporary JSON files so they don't accidentally modify your real data.