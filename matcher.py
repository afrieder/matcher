from typing import (Callable as _Callable,
                   cast as _cast,
                   Generic as _Generic,
                   Iterable as _Iterable,
                   Type as _Type,
                   TypeVar as _TypeVar)

__all__ = ['Matcher', 'MatchError']

_S = _TypeVar('_S')
_T = _TypeVar('_T')
_U = _TypeVar('_U')


class MatchError(LookupError):
    """
    An error raised when a match call exhausts all matchers without
    finding a match.
    """
    pass


class _Case(_Generic[_S, _T]):
    def __init__(self,
                 matcher: _Callable[[_S], bool],
                 actions: _Iterable[_Callable[[_S], _T]]) -> None:
        self._matcher = matcher
        self._actions = actions

    def matches(self, value: _S) -> bool:
        return self._matcher(value)

    def result(self, value: _S) -> _T:
        returnValue = None  # type: _T
        for action in self._actions:
            returnValue = action(value)
        return returnValue


class Matcher(_Generic[_S, _T]):
    @staticmethod
    def match(value: _S, matchers: _Iterable[_Case[_S, _T]]) -> _T:
        for matcher in matchers:
            if matcher.matches(value):
                return matcher.result(value)
        raise MatchError("{} doesn't match any of the "
                         "provided clauses".format(value))

    @staticmethod
    def Value(key: _S, *actions: _Callable[[_S], _T]) -> _Case[_S, _T]:
        return _Case(lambda value: value == key, actions)

    @staticmethod
    def Values(keys: _Iterable[_S], *actions: _Callable[[_S], _T]) -> _Case[_S, _T]:
        return _Case(lambda value: any(value == key for key in keys), actions)

    @staticmethod
    def Type(typ: _Type[_U], *actions: _Callable[[_U], _T]) -> _Case[_S, _T]:
        def castWrapper(action: _Callable[[_U], _T]) -> _Callable[[_S], _T]:
            return lambda value: action(_cast(_U, value))

        return _Case(lambda value: isinstance(value, typ),
                    map(castWrapper, actions))

    @staticmethod
    def Else(*actions: _Callable[[_S], _T]) -> _Case[_S, _T]:
        return _Case(lambda value: True, actions)
