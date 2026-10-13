#!/usr/bin/env python3
"""Perform CRUD operations on any JSON file.

Usage examples:
    modify_json.py -p data.json -c -t user.name --data '"Alice"'
    modify_json.py -p data.json -c -t user.tags --data '["admin", "dev"]'
    modify_json.py -p data.json -c -t user.address --data '{"city": "Oslo"}'
    modify_json.py -p data.json -r -t user.name
    modify_json.py -p data.json -r                      # read whole file
    modify_json.py -p data.json -u -t user.name --data '"Bob"'
    modify_json.py -p data.json -d -t user.address      # delete whole key
    modify_json.py -p data.json -d -t user.tags --data '"admin"'  # remove value from list

Write operations are atomic: the result is written to a temporary file in the
same directory, flushed, and then moved over the original file.
"""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


class JsonCrudError(Exception):
    """User-facing error raised for invalid operations or paths."""


REMOVAL_UNSUPPORTED_MSG = "--data removal is only supported for list or object targets"


def _err_target_not_found(segments: list[str]) -> JsonCrudError:
    return JsonCrudError(f"Target not found: {'.'.join(segments)}")


# ================================================
# Argument parsing
# ================================================
def parse_data(value: str) -> Any:
    """Parse --data as JSON; fall back to a plain string if it is not JSON."""
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Perform CRUD operations on a JSON file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument("-c", "--create", action="store_true",
                           help="Create a new value at the target path.")
    operation.add_argument("-r", "--read", action="store_true",
                           help="Read the value at the target path (or the whole file).")
    operation.add_argument("-u", "--update", action="store_true",
                           help="Update an existing value at the target path.")
    operation.add_argument("-d", "--delete", action="store_true",
                           help="Delete the target, or remove --data value(s) from a list target.")

    parser.add_argument("-p", "--path", type=Path, required=True,
                        help="Path to the JSON file.")
    parser.add_argument("-t", "--target", type=str,
                        help="Dot-separated path where the JSON should change, e.g. 'user.name'. "
                             "Numeric segments index into lists, e.g. 'users.0.name'.")
    parser.add_argument("--data", type=parse_data,
                        help="Value to add/update/remove. Parsed as JSON when possible "
                             "('\"text\"', '[1, 2]', '{\"k\": \"v\"}'), otherwise used as a plain string.")

    return parser.parse_args(argv)


# ================================================
# Target path resolution
# ================================================
def split_target(target: str) -> list[str]:
    segments = [seg for seg in target.split(".") if seg != ""]
    if not segments:
        raise JsonCrudError(f"Invalid target path: {target!r}")
    return segments


def _list_index(segment: str, node: list) -> int:
    try:
        index = int(segment)
    except ValueError:
        raise JsonCrudError(f"Expected a numeric list index, got {segment!r}") from None
    if not -len(node) <= index < len(node):
        raise JsonCrudError(f"List index {index} out of range (length {len(node)})")
    return index


def resolve_parent(root: Any, segments: list[str], create_missing: bool = False) -> tuple[Any, str]:
    """Walk to the container holding the final segment. Returns (parent, last_segment)."""
    node = root
    for segment in segments[:-1]:
        if isinstance(node, list):
            node = node[_list_index(segment, node)]
        elif isinstance(node, dict):
            if segment not in node:
                if not create_missing:
                    raise JsonCrudError(f"Target path not found: missing {segment!r}")
                node[segment] = {}
            node = node[segment]
        else:
            raise JsonCrudError(f"Cannot traverse through {segment!r}: value is not an object or list")
    return node, segments[-1]


# ================================================
# CRUD operations
# ================================================
def op_create(root: Any, segments: list[str], data: Any) -> Any:
    parent, key = resolve_parent(root, segments, create_missing=True)
    if isinstance(parent, list):
        index = int(key) if key.lstrip("-").isdigit() else len(parent)
        if index < len(parent):
            raise JsonCrudError(f"Index {index} already exists; use -u to update it")
        parent.append(data)
    elif isinstance(parent, dict):
        if key in parent:
            raise JsonCrudError(f"Target {key!r} already exists; use -u to update it")
        parent[key] = data
    else:
        raise JsonCrudError("Cannot create a key on a non-object value")
    return root


def _get_existing_child(parent: Any, key: str, segments: list[str]) -> Any:
    if isinstance(parent, list):
        return parent[_list_index(key, parent)]
    if isinstance(parent, dict) and key in parent:
        return parent[key]
    raise _err_target_not_found(segments)


def op_read(root: Any, segments: list[str] | None) -> Any:
    if not segments:
        return root
    parent, key = resolve_parent(root, segments)
    return _get_existing_child(parent, key, segments)


def op_update(root: Any, segments: list[str], data: Any) -> Any:
    parent, key = resolve_parent(root, segments)
    if isinstance(parent, list):
        parent[_list_index(key, parent)] = data
    elif isinstance(parent, dict) and key in parent:
        parent[key] = data
    else:
        raise JsonCrudError(f"Target not found: {'.'.join(segments)}; use -c to create it")
    return root


def _remove_from_list(node: list, data: Any) -> int:
    values = data if isinstance(data, list) else [data]
    removed = 0
    for value in values:
        while value in node:
            node.remove(value)
            removed += 1
    return removed


def _remove_from_dict(node: dict, data: Any) -> int:
    keys = list(data) if isinstance(data, (list, dict)) else [data]
    removed = 0
    for key in keys:
        if isinstance(key, str) and key in node:
            del node[key]
            removed += 1
    return removed


def _remove_matching(node: Any, data: Any) -> int:
    """Remove value(s) described by --data from a list or dict node."""
    if isinstance(node, list):
        return _remove_from_list(node, data)
    if isinstance(node, dict):
        return _remove_from_dict(node, data)
    raise JsonCrudError(REMOVAL_UNSUPPORTED_MSG)


def _delete_value_at(parent: Any, key: str, segments: list[str]) -> None:
    if isinstance(parent, list):
        parent.pop(_list_index(key, parent))
        return
    if isinstance(parent, dict) and key in parent:
        del parent[key]
        return
    raise _err_target_not_found(segments)


def _delete_matching_at(parent: Any, key: str, segments: list[str], data: Any) -> None:
    node = _get_existing_child(parent, key, segments)
    if not isinstance(node, (list, dict)):
        raise JsonCrudError(REMOVAL_UNSUPPORTED_MSG)
    if _remove_matching(node, data) == 0:
        raise JsonCrudError("No matching value found at the target")


def op_delete(root: Any, segments: list[str], data: Any, data_given: bool) -> Any:
    parent, key = resolve_parent(root, segments)
    if data_given:
        _delete_matching_at(parent, key, segments, data)
    else:
        _delete_value_at(parent, key, segments)
    return root


# ================================================
# File I/O (atomic write)
# ================================================
def load_json(path: Path, allow_missing: bool = False) -> Any:
    if not path.exists():
        if allow_missing:
            return {}
        raise JsonCrudError(f"File not found: {path}")
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as exc:
        raise JsonCrudError(f"Invalid JSON in {path}: {exc}") from exc


def atomic_write(path: Path, data: Any) -> None:
    fd, tmp_name = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as tmp_file:
            json.dump(data, tmp_file, indent=2)
            tmp_file.write("\n")
            tmp_file.flush()
            os.fsync(tmp_file.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


# ================================================
# Main
# ================================================
def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    mutating = args.create or args.update or args.delete
    if mutating and not args.target:
        raise JsonCrudError("-t/--target is required for create, update and delete")
    if (args.create or args.update) and args.data is None:
        raise JsonCrudError("--data is required for create and update")

    segments = split_target(args.target) if args.target else None

    root = load_json(args.path, allow_missing=args.create)

    if args.read:
        print(json.dumps(op_read(root, segments), indent=2))
        return 0

    assert segments is not None  # target is required for mutating operations
    if args.create:
        result = op_create(root, segments, args.data)
    elif args.update:
        result = op_update(root, segments, args.data)
    else:
        result = op_delete(root, segments, args.data, args.data is not None)

    atomic_write(args.path, result)
    print(f"Updated {args.path}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except JsonCrudError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
