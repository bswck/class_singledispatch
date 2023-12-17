import enum
import sys
from dataclasses import dataclass

from class_singledispatch import class_singledispatch


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
            assert c == Fallback
            return ClassSingleDispatchResult.FALLBACK

        @on_class.register
        def on_special_class(c: type[Special], /) -> ClassSingleDispatchResult:
            assert c == Special
            return ClassSingleDispatchResult.SPECIAL

        @on_class.register(Superspecial)
        def on_superspecial_class(
            c: type[Superspecial],
            /,
        ) -> ClassSingleDispatchResult:
            assert c == Superspecial
            return ClassSingleDispatchResult.SUPERSPECIAL

        assert on_class(Fallback) is ClassSingleDispatchResult.FALLBACK
        assert on_class(Special) is ClassSingleDispatchResult.SPECIAL
        assert on_class(Superspecial) is ClassSingleDispatchResult.SUPERSPECIAL

else:

    def test_class_singledispatch_oldstyle() -> None:
        from typing import Type

        @class_singledispatch
        def on_class(c: Type[Fallback], /) -> ClassSingleDispatchResult:
            assert c == Fallback
            return ClassSingleDispatchResult.FALLBACK

        @on_class.register
        def on_special_class(c: Type[Special], /) -> ClassSingleDispatchResult:
            assert c == Special
            return ClassSingleDispatchResult.SPECIAL

        @on_class.register(Superspecial)
        def on_superspecial_class(
            c: Type[Superspecial], /
        ) -> ClassSingleDispatchResult:
            assert c == Superspecial
            return ClassSingleDispatchResult.SUPERSPECIAL

        assert on_class(Fallback) is ClassSingleDispatchResult.FALLBACK
        assert on_class(Special) is ClassSingleDispatchResult.SPECIAL
        assert on_class(Superspecial) is ClassSingleDispatchResult.SUPERSPECIAL
