import enum
import sys
from dataclasses import dataclass
from typing import Type

import pytest

from class_singledispatch import class_singledispatch, resolve_annotated_type


@dataclass
class Fallback:
    ...


@dataclass
class Special(Fallback):
    ...


@dataclass
class Superspecial(Fallback):
    ...


class ClassSingleDispatchResult(enum.Enum):
    FALLBACK = "fallback instance"
    SPECIAL = "special instance"
    SUPERSPECIAL = "superspecial instance"


if sys.version_info >= (3, 10):

    def test_class_singledispatch_v10() -> None:
        @class_singledispatch
        def on_class(c: type[Fallback], /) -> ClassSingleDispatchResult:
            assert c is Fallback
            return ClassSingleDispatchResult.FALLBACK

        @on_class.register
        def on_special_class(c: type[Special], /) -> ClassSingleDispatchResult:
            assert c is Special
            return ClassSingleDispatchResult.SPECIAL

        @on_class.register(Superspecial)
        def on_superspecial_class(
            c: type[Superspecial],
            /,
        ) -> ClassSingleDispatchResult:
            assert c is Superspecial
            return ClassSingleDispatchResult.SUPERSPECIAL

        assert on_class(Fallback) is ClassSingleDispatchResult.FALLBACK
        assert on_class(Special) is ClassSingleDispatchResult.SPECIAL
        assert on_class(Superspecial) is ClassSingleDispatchResult.SUPERSPECIAL


def test_class_singledispatch_oldstyle() -> None:

    @class_singledispatch
    def on_class(c: Type[Fallback], /) -> ClassSingleDispatchResult:
        assert c is Fallback
        return ClassSingleDispatchResult.FALLBACK

    @on_class.register
    def on_special_class(c: Type[Special], /) -> ClassSingleDispatchResult:
        assert c is Special
        return ClassSingleDispatchResult.SPECIAL

    @on_class.register(Superspecial)
    def on_superspecial_class(c: Type[Superspecial], /) -> ClassSingleDispatchResult:
        assert c is Superspecial
        return ClassSingleDispatchResult.SUPERSPECIAL

    assert on_class(Fallback) is ClassSingleDispatchResult.FALLBACK
    assert on_class(Special) is ClassSingleDispatchResult.SPECIAL
    assert on_class(Superspecial) is ClassSingleDispatchResult.SUPERSPECIAL

    def on_none(c: Type[lambda: None], /) -> None:  # type: ignore[valid-type]
        assert c is None

    with pytest.raises(TypeError):
        on_class.register(on_none)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        resolve_annotated_type(on_none)


def test_registry_available() -> None:
    @class_singledispatch
    def on_class(c: Type[Fallback], /) -> None:
        pass

    assert on_class.registry is on_class._dispatch.registry


def test_invalid_usage() -> None:
    with pytest.raises(TypeError):

        @class_singledispatch
        def on_class(c: Fallback, /) -> None:
            pass

    @class_singledispatch
    def on_class_ok(c: Type[Fallback], /) -> None:
        pass

    with pytest.raises(TypeError):
        on_class_ok.register(object())  # type: ignore[call-overload]

    with pytest.raises(TypeError):
        on_class_ok.register(lambda: None, lambda: None)  # type: ignore[call-overload]
