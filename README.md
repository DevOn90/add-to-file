# My application

## Purpose

CLI Shopping List — a small command-line shopping list written in
Python, built as a learning exercise. See [SPEC.md](SPEC.md) for the
full specification.

## Requirements

- Python 3 (standard library only; no packages to install).

## Installation

None. Clone the repository and run the script.

## Usage

```
python src/shopping_list.py
```

The program shows a menu and accepts four commands, typed as words:
`add`, `display`, `remove`, `exit`.

## Examples

```
Shopping list.
Menu: add | display | remove | exit
> add
Item name: milk
Added 'milk'.
Menu: add | display | remove | exit
> display
milk
```

## Testing

```
python -m unittest discover tests
```

## Limitations

- The list is kept in memory only; it resets on every start.
- Single list, item names only (no quantities or categories).