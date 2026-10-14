"""Add or update key/value pairs in a JSON file. See SPEC.md."""

import argparse
import json
import sys


class OperationError(Exception):
    """A user-facing failure: message goes to stderr, exit code 1."""


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="add_to_json.py",
        description="Add or update a key/value pair in a JSON file.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("add", "update"):
        sub = subparsers.add_parser(command, help=f"{command} a key/value pair")
        sub.add_argument("-f", "--file", required=True, help="path to the JSON file")
        sub.add_argument("-t", "--target", required=True, help="dot-separated key path")
        sub.add_argument("-d", "--data", required=True, help="scalar JSON value to set")
    return parser.parse_args(argv)


def parse_value(raw, target, path):
    try:
        value = json.loads(raw)
    except json.JSONDecodeError:
        raise OperationError(
            f"invalid --data value {raw!r} for {target!r} in {path}: not valid JSON"
        )
    if isinstance(value, (dict, list)):
        raise OperationError(
            f"invalid --data value {raw!r} for {target!r} in {path}: "
            "objects and arrays are not supported in stage 1"
        )
    return value


def load_document(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise OperationError(f"file not found: {path}")
    except json.JSONDecodeError as exc:
        raise OperationError(f"invalid JSON in {path}: {exc}")


def resolve_parent(doc, target, create, path):
    parts = target.split(".")
    if any(part == "" for part in parts):
        raise OperationError(f"invalid target path {target!r} in {path}")
    node = doc
    walked = []
    for part in parts[:-1]:
        if isinstance(node, list):
            raise OperationError(
                f"cannot reach {target!r} in {path}: "
                "array elements are not supported as targets"
            )
        if not isinstance(node, dict):
            raise OperationError(
                f"cannot reach {target!r} in {path}: "
                f"intermediate key {'.'.join(walked)!r} holds a scalar value"
            )
        walked.append(part)
        if part not in node:
            if not create:
                raise OperationError(f"key not found: {target!r} in {path}")
            node[part] = {}
        node = node[part]
    if isinstance(node, list):
        raise OperationError(
            f"cannot reach {target!r} in {path}: "
            "array elements are not supported as targets"
        )
    if not isinstance(node, dict):
        where = ".".join(parts[:-1]) or "<document root>"
        raise OperationError(
            f"cannot reach {target!r} in {path}: {where!r} holds a scalar value"
        )
    return node, parts[-1]


def apply_operation(doc, target, value, command, path):
    parent, key = resolve_parent(doc, target, create=(command == "add"), path=path)
    if command == "add":
        if key in parent:
            raise OperationError(f"cannot add {target!r} in {path}: key already exists")
        parent[key] = value
        return "added"
    if key not in parent:
        raise OperationError(f"cannot update {target!r} in {path}: key not found")
    parent[key] = value
    return "updated"


def main(argv=None):
    args = parse_args(argv)
    try:
        value = parse_value(args.data, args.target, args.file)
        doc = load_document(args.file)
        verb = apply_operation(doc, args.target, value, args.command, args.file)
    except OperationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    with open(args.file, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2)
        fh.write("\n")
    print(f"{verb} {args.target} = {json.dumps(value)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
