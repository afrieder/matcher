# Stubs for _matcher.py

from typing import Callable, Generic, Iterable, Type as Typ, TypeVar

S = TypeVar('S')
T = TypeVar('T')
U = TypeVar('U')


class MatchError(LookupError): ...


class _Case(Generic[S, T]):
    def __init__(self,
                 matcher: Callable[[S], bool],
                 actions: Iterable[Callable[[S], T]]) -> None: ...
    def matches(self, value: S) -> bool: ...
    def result(self, value: S) -> T: ...


class Matcher(Generic[S, T]):
    @staticmethod
    def match(value: S, matchers: Iterable[_Case[S, T]]) -> T: ...
    @staticmethod
    def Value(key: S, *actions: Callable[[S], T]) -> _Case[S, T]: ...
    @staticmethod
    def Values(keys: Iterable[S], *actions: Callable[[S], T]) -> _Case[S, T]: ...
    @staticmethod
    def Type(typ: Typ[U], *actions: Callable[[U], T]) -> _Case[S, T]: ...
    @staticmethod
    def Else(*actions: Callable[[S], T]) -> _Case[S, T]: ...
