"""File management."""


import shelve
from pathlib import Path


def save_memory(local_path: Path, positions: list[int]) -> None:
    """Save object to memory."""
    with shelve.open(local_path) as db:
        db['save'] = positions


def get_memory(local_path: Path) -> list[int]:
    """Get object from memory."""
    if not local_path.exists():
        default = [3, 3]
        save_memory(local_path, default)
        return default
    with shelve.open(local_path) as db:
        return db.get('save', [])


def first_save_memory(local_path: Path) -> None:
    """Save the first object to memory."""
    with shelve.open(local_path) as db:
        if not bool(db.get('save')):
            db['save'] = [3, 3]
