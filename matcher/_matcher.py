from typing import Callable, cast, Generic, Iterable, Type as Typ, TypeVar

__all__ = ['Matcher', 'MatchError']

S = TypeVar('S')
T = TypeVar('T')
U = TypeVar('U')


class MatchError(LookupError):
    """
    An error raised when a match call exhausts all matchers without
    finding a match.
    """
    pass


class _Case(Generic[S, T]):
    def __init__(self,
                 matcher: Callable[[S], bool],
                 actions: Iterable[Callable[[S], T]]) -> None:
        self._matcher = matcher
        self._actions = actions

    def matches(self, value: S) -> bool:
        return self._matcher(value)

    def result(self, value: S) -> T:
        returnValue = None  # type: T
        for action in self._actions:
            returnValue = action(value)
        return returnValue


class Matcher(Generic[S, T]):
    @staticmethod
    def match(value: S, matchers: Iterable[_Case[S, T]]) -> T:
        for matcher in matchers:
            if matcher.matches(value):
                return matcher.result(value)
        raise MatchError("{} doesn't match any of the "
                         "provided clauses".format(value))

    @staticmethod
    def Value(key: S, *actions: Callable[[S], T]) -> _Case[S, T]:
        return _Case(lambda value: value == key, actions)

    @staticmethod
    def Values(keys: Iterable[S], *actions: Callable[[S], T]) -> _Case[S, T]:
        return _Case(lambda value: any(value == key for key in keys), actions)

    @staticmethod
    def Type(typ: Typ[U], *actions: Callable[[U], T]) -> _Case[S, T]:
        def castWrapper(action: Callable[[U], T]) -> Callable[[S], T]:
            return lambda value: action(cast(U, value))

        return _Case(lambda value: isinstance(value, typ),
                    map(castWrapper, actions))

    @staticmethod
    def Else(*actions: Callable[[S], T]) -> _Case[S, T]:
        return _Case(lambda value: True, actions)
