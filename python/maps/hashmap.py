from __future__ import annotations
from dataclasses import dataclass
from typing import Generic, Optional, Tuple, TypeVar, Iterator, Iterable

K = TypeVar("K")
V = TypeVar("V")


@dataclass
class _Entry(Generic[K, V]):
    key: K
    value: V
    deleted: bool = False


class HashMap(Generic[K, V]):
    """
    HashMap (open addressing, linear probing).
    Features:
    - put / get / remove / contains
    - resize when load factor exceeded
    """

    def __init__(self, initial_capacity: int = 8, max_load_factor: float = 0.65):
        if initial_capacity < 1:
            raise ValueError("initial_capacity must be >= 1")
        cap = 1
        while cap < initial_capacity:
            cap <<= 1

        self._cap = cap
        self._max_lf = max_load_factor
        self._size = 0          # active entries
        self._used = 0          # active + tombstones
        self._table: list[Optional[_Entry[K, V]]] = [None] * self._cap

    def __len__(self) -> int:
        return self._size

    def _hash(self, key: K) -> int:
        return hash(key) & 0x7FFFFFFF

    def _index(self, key: K) -> int:
        return self._hash(key) & (self._cap - 1)

    def _probe(self, key: K) -> Tuple[int, Optional[int]]:
        """
        Returns: (best_insert_index, found_index_if_exists)
        If key exists -> found_index is not None.
        Else -> found_index is None and best_insert_index is where to insert (prefers first tombstone).
        """
        start = self._index(key)
        first_tombstone = None

        for i in range(self._cap):
            idx = (start + i) & (self._cap - 1)
            e = self._table[idx]

            if e is None:
                return (first_tombstone if first_tombstone is not None else idx), None

            if e.deleted:
                if first_tombstone is None:
                    first_tombstone = idx
                continue

            if e.key == key:
                return idx, idx

        # Should not happen if resize works correctly
        return (first_tombstone if first_tombstone is not None else start), None

    def _maybe_resize(self) -> None:
        if (self._used / self._cap) > self._max_lf:
            self._resize(self._cap * 2)

    def _resize(self, new_cap: int) -> None:
        old = self._table
        self._cap = new_cap
        self._table = [None] * self._cap
        self._size = 0
        self._used = 0

        for e in old:
            if e and not e.deleted:
                self.put(e.key, e.value)

    def put(self, key: K, value: V) -> None:
        self._maybe_resize()
        ins_idx, found_idx = self._probe(key)

        if found_idx is not None:
            self._table[found_idx].value = value  # type: ignore[union-attr]
            return

        existing = self._table[ins_idx]
        if existing is None:
            self._used += 1
        # else: tombstone reuse, _used unchanged

        self._table[ins_idx] = _Entry(key=key, value=value, deleted=False)
        self._size += 1

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        _, found_idx = self._probe(key)
        if found_idx is None:
            return default
        return self._table[found_idx].value  # type: ignore[union-attr]

    def contains(self, key: K) -> bool:
        _, found_idx = self._probe(key)
        return found_idx is not None

    def remove(self, key: K) -> bool:
        _, found_idx = self._probe(key)
        if found_idx is None:
            return False
        e = self._table[found_idx]
        if e and not e.deleted:
            e.deleted = True
            self._size -= 1
            return True
        return False

    def items(self) -> Iterator[Tuple[K, V]]:
        for e in self._table:
            if e and not e.deleted:
                yield e.key, e.value

    def __repr__(self) -> str:
        pairs = ", ".join(f"{k!r}: {v!r}" for k, v in self.items())
        return f"HashMap({{{pairs}}})"


if __name__ == "__main__":
    m = HashMap[str, int]()
    m.put("a", 1)
    m.put("b", 2)
    m.put("a", 10)
    print(m)
    print("a =", m.get("a"))
    print("contains c?", m.contains("c"))
    print("remove b:", m.remove("b"))
    print("items:", list(m.items()))
