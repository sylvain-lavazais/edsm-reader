from threading import Lock
from types import GenericAlias
from typing import Any, Iterable, Iterator


class ThreadSafeList(list):
    _lock: Lock

    def __init__(self):
        super().__init__()
        self._lock = Lock()

    def clear(self) -> None:
        with self._lock:
            super().clear()

    def copy(self) -> list:
        with self._lock:
            return super().copy()

    def append(self, _object: Any) -> None:
        with self._lock:
            super().append(_object)

    def extend(self, _iterable: Iterable[Any]) -> None:
        with self._lock:
            super().extend(_iterable)

    def remove(self, _value: Any) -> None:
        with self._lock:
            super().remove(_value)

    def reverse(self) -> None:
        with self._lock:
            super().reverse()

    def sort(self, **kwargs) -> None:
        with self._lock:
            super().sort(**kwargs)

    def __len__(self) -> int:
        with self._lock:
            return super().__len__()

    def __iter__(self) -> Iterator[Any]:
        with self._lock:
            return super().__iter__()

    def __contains__(self, o: object) -> bool:
        with self._lock:
            return super().__contains__(o)

    def __reversed__(self) -> Iterator[Any]:
        with self._lock:
            return super().__reversed__()

    def __gt__(self, x: list[Any]) -> bool:
        with self._lock:
            return super().__gt__(x)

    def __ge__(self, x: list[Any]) -> bool:
        with self._lock:
            return super().__ge__(x)

    def __lt__(self, x: list[Any]) -> bool:
        with self._lock:
            return super().__lt__(x)

    def __le__(self, x: list[Any]) -> bool:
        with self._lock:
            return super().__le__(x)

    def __class_getitem__(cls, item: Any) -> GenericAlias:
        with cls._lock:
            return super().__class_getitem__(item)
