from __future__ import annotations

import enum
import sys
from contextlib import suppress
from dataclasses import dataclass
from typing import ForwardRef, Type

import pytest

from class_singledispatch import class_singledispatch, resolve_annotated_type

with suppress(ImportError):
    from eval_type_backport import ForwardRef


@dataclass
class Spam:
    ...


@dataclass
class Eggs(Spam):
    ...


@dataclass
class Ham(Spam):
    ...


class ClassSingleDispatchResult(enum.Enum):
    SPAM = "spam"
    EGGS = "eggs"
    HAM = "ham"


if (
    ForwardRef.__module__.startswith("eval_type_backport")
    or sys.version_info >= (3, 10)
):

    def test_class_singledispatch_v10() -> None:
        @class_singledispatch
        def on_class(c: type[Spam], /) -> ClassSingleDispatchResult:
            assert c is Spam
            return ClassSingleDispatchResult.SPAM

        @on_class.register
        def on_eggs_class(c: type[Eggs], /) -> ClassSingleDispatchResult:
            assert c is Eggs
            return ClassSingleDispatchResult.EGGS

        @on_class.register(Ham)
        def on_ham_class(
            c: type[Ham],
            /,
        ) -> ClassSingleDispatchResult:
            assert c is Ham
            return ClassSingleDispatchResult.HAM

        assert on_class(Spam) is ClassSingleDispatchResult.SPAM
        assert on_class(Eggs) is ClassSingleDispatchResult.EGGS
        assert on_class(Ham) is ClassSingleDispatchResult.HAM


def test_class_singledispatch_oldstyle() -> None:

    @class_singledispatch
    def on_class(c: Type[Spam], /) -> ClassSingleDispatchResult:
        assert c is Spam
        return ClassSingleDispatchResult.SPAM

    @on_class.register
    def on_eggs_class(c: Type[Eggs], /) -> ClassSingleDispatchResult:
        assert c is Eggs
        return ClassSingleDispatchResult.EGGS

    @on_class.register(Ham)
    def on_ham_class(c: Type[Ham], /) -> ClassSingleDispatchResult:
        assert c is Ham
        return ClassSingleDispatchResult.HAM

    assert on_class(Spam) is ClassSingleDispatchResult.SPAM
    assert on_class(Eggs) is ClassSingleDispatchResult.EGGS
    assert on_class(Ham) is ClassSingleDispatchResult.HAM

    def on_none(c: Type[lambda: None], /) -> None:  # type: ignore[valid-type]
        assert c is None

    with pytest.raises(TypeError):
        on_class.register(on_none)  # type: ignore[arg-type]

    with pytest.raises(TypeError):
        resolve_annotated_type(on_none)


def test_registry_available() -> None:
    @class_singledispatch
    def on_class(c: Type[Spam], /) -> None:
        pass

    assert on_class.registry is on_class._dispatch.registry


def test_invalid_usage() -> None:
    with pytest.raises(TypeError):

        @class_singledispatch
        def on_class(c: Spam, /) -> None:
            pass

    @class_singledispatch
    def on_class_ok(c: Type[Spam], /) -> None:
        pass

    with pytest.raises(TypeError):
        on_class_ok.register(object())  # type: ignore[call-overload]

    with pytest.raises(TypeError):
        on_class_ok.register(lambda: None, lambda: None)  # type: ignore[call-overload]
