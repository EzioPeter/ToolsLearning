"""
Iterator examples

- Stateful iterator implementing __iter__ and __next__
- Iterable that returns a fresh iterator each time (reusable)
- Demonstrates exhaustion and manual `next()` usage
"""
from typing import Iterator

class CountUpIterator:
    """A simple stateful iterator that counts from 1..max_inclusive."""
    def __init__(self, max_inclusive: int):
        self.max = max_inclusive
        self.current = 0

    def __iter__(self) -> "CountUpIterator":
        return self

    def __next__(self) -> int:
        if self.current >= self.max:
            raise StopIteration
        self.current += 1
        return self.current


class CountUpIterable:
    """An iterable that returns a fresh CountUpIterator on each __iter__ call."""
    def __init__(self, max_inclusive: int):
        self.max = max_inclusive

    def __iter__(self) -> Iterator[int]:
        return CountUpIterator(self.max)


def demo_stateful_iterator():
    print("-- demo_stateful_iterator --")
    it = CountUpIterator(3)
    print("manual next():", next(it))   # 1
    print("manual next():", next(it))   # 2
    print("for-loop resumes from current state:")
    for v in it:
        print("  ", v)                 # prints 3
    try:
        print("after exhaustion next():", next(it))
    except StopIteration:
        print("  -> StopIteration (iterator exhausted)")
    print()


def demo_reusable_iterable():
    print("-- demo_reusable_iterable --")
    iterable = CountUpIterable(3)
    print("first pass:", list(iterable))   # [1,2,3]
    print("second pass:", list(iterable))  # again [1,2,3]
    print()


if __name__ == '__main__':
    demo_stateful_iterator()
    demo_reusable_iterable()
