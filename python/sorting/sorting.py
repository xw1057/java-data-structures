from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence, TypeVar

T = TypeVar("T")


def bubble_sort(arr: List[T], key: Optional[Callable[[T], object]] = None, reverse: bool = False) -> List[T]:
    """
    In-place bubble sort with last-swap optimization.
    Returns the same list for convenience.
    """
    if key is None:
        key = lambda x: x  # type: ignore[return-value]

    n = len(arr)
    if n <= 1:
        return arr

    end = n - 1
    while end > 0:
        last_swap = -1
        for i in range(end):
            a = key(arr[i])
            b = key(arr[i + 1])
            should_swap = a > b if not reverse else a < b
            if should_swap:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                last_swap = i
        if last_swap == -1:
            break
        end = last_swap
    return arr


def merge_sort(arr: Sequence[T], key: Optional[Callable[[T], object]] = None, reverse: bool = False) -> List[T]:
    """
    Out-of-place stable merge sort.
    Returns a new list.
    """
    if key is None:
        key = lambda x: x  # type: ignore[return-value]

    a = list(arr)
    n = len(a)
    if n <= 1:
        return a

    mid = n // 2
    left = merge_sort(a[:mid], key=key, reverse=reverse)
    right = merge_sort(a[mid:], key=key, reverse=reverse)

    merged: List[T] = []
    i = j = 0
    while i < len(left) and j < len(right):
        lv = key(left[i])
        rv = key(right[j])

        if not reverse:
            # stable: when equal, take from left first
            if lv <= rv:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        else:
            if lv >= rv:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

    if i < len(left):
        merged.extend(left[i:])
    if j < len(right):
        merged.extend(right[j:])
    return merged


def quick_sort(arr: List[T], key: Optional[Callable[[T], object]] = None, reverse: bool = False) -> List[T]:
    """
    In-place quick sort (not stable).
    Returns the same list for convenience.
    """
    if key is None:
        key = lambda x: x  # type: ignore[return-value]

    def lt(a: object, b: object) -> bool:
        return a < b if not reverse else a > b

    def gt(a: object, b: object) -> bool:
        return a > b if not reverse else a < b

    def partition(lo: int, hi: int) -> int:
        pivot = arr[(lo + hi) // 2]
        pv = key(pivot)

        i, j = lo, hi
        while i <= j:
            while lt(key(arr[i]), pv):
                i += 1
            while gt(key(arr[j]), pv):
                j -= 1
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1
        return i

    def qs(lo: int, hi: int) -> None:
        if lo >= hi:
            return
        idx = partition(lo, hi)
        qs(lo, idx - 1)
        qs(idx, hi)

    if len(arr) <= 1:
        return arr
    qs(0, len(arr) - 1)
    return arr


def heap_sort(arr: List[T], key: Optional[Callable[[T], object]] = None, reverse: bool = False) -> List[T]:
    """
    In-place heap sort (not stable).
    Returns the same list for convenience.
    """
    if key is None:
        key = lambda x: x  # type: ignore[return-value]

    def better(a: object, b: object) -> bool:
        # for a max-heap when reverse=False, "better" means larger
        # when reverse=True, we want a min-heap behavior so "better" means smaller
        return a > b if not reverse else a < b

    n = len(arr)
    if n <= 1:
        return arr

    def sift_down(i: int, size: int) -> None:
        while True:
            left = 2 * i + 1
            right = left + 1
            best = i

            if left < size and better(key(arr[left]), key(arr[best])):
                best = left
            if right < size and better(key(arr[right]), key(arr[best])):
                best = right

            if best == i:
                return
            arr[i], arr[best] = arr[best], arr[i]
            i = best

    # build heap
    for i in range((n // 2) - 1, -1, -1):
        sift_down(i, n)

    # extract
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        sift_down(0, end)

    # if reverse=True, heap logic already produced reverse order via min-heap behavior
    return arr


if __name__ == "__main__":
    data = [5, 1, 4, 2, 8, 0, 2]
    print("bubble:", bubble_sort(data.copy()))
    print("merge :", merge_sort(data))
    print("quick :", quick_sort(data.copy()))
    print("heap  :", heap_sort(data.copy()))
    print("desc  :", merge_sort(data, reverse=True))
