# SPDX-License-Identifier: MIT
# (C) 2024-present Bartosz Sławecki (bswck)
"""
`class_singledispatch`.

A [`singledispatch`][functools.singledispatch] for arguments that are classes
annotated as specific types.

https://github.com/python/cpython/issues/100623
"""

from __future__ import annotations

import sys
from contextlib import suppress
from functools import partial, singledispatch
from typing import (
    TYPE_CHECKING,
    Any,
    ForwardRef,
    Generic,
    Type,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from types import MappingProxyType
    from typing import overload


OldFashionGenericAlias: type[object] = type(Type[object])

if sys.version_info < (3, 9):
    GenericAlias = OldFashionGenericAlias
else:
    from types import GenericAlias


if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

with suppress(ImportError):
    from eval_type_backport import ForwardRef  # noqa: F811


__all__ = (
    "class_singledispatch",
    "resolve_annotated_type",
)


_P = ParamSpec("_P")
_R = TypeVar("_R")


def resolve_annotated_type(func: Callable[..., _R]) -> type[Any]:
    """
    Resolve the annotated type of the first argument of `func`.

    This function is used to determine the type of the first argument of `func`
    when the first argument is annotated as a type (e.g. `type[SomeClass]`).
    """
    func_annotations = getattr(func, "__annotations__", {})
    if not func_annotations:
        msg = (
            f"Invalid first argument to `register()`: {func!r}. "
            f"Use either `@register(some_class)` or plain `@register` "
            f"on an annotated function."
        )
        raise TypeError(msg)
    for key, value in func_annotations.items():
        if isinstance(value, str):
            func_annotations[key] = ForwardRef(value)
    argument_name, generic_alias = next(iter(get_type_hints(func).items()))
    if not (
        isinstance(generic_alias, (GenericAlias, OldFashionGenericAlias))
        and ((origin := get_origin(generic_alias)) is Type or isinstance(origin, type))
    ):
        msg = (
            f"Invalid annotation for {argument_name!r}. "
            f"{generic_alias!r} is not an annotation of type (e.g. type[T])."
        )
        raise TypeError(msg)
    cls = next(iter(get_args(generic_alias)), object)
    if not isinstance(cls, type):
        msg = (
            f"Invalid annotation for {argument_name!r}. {cls!r} is not a runtime class."
        )
        raise TypeError(msg)
    return cls


class _ClassSingleDispatchCallable(Generic[_R]):
    def __init__(self, func: Callable[..., _R]) -> None:
        self._dispatch = singledispatch(func)
        # Validate this function.
        resolve_annotated_type(func)

    def dispatch(self, cls: type[Any]) -> Callable[..., _R]:
        return self._dispatch.dispatch(cls)

    @property
    def registry(self) -> MappingProxyType[type[Any], Callable[..., _R]]:
        return self._dispatch.registry

    if TYPE_CHECKING:

        @overload
        def register(
            self,
            cls: type[Any],
            /,
            func: Callable[_P, _R],
        ) -> Callable[_P, _R]: ...

        @overload
        def register(
            self,
            cls: type[Any],
            /,
            func: None = None,
        ) -> partial[Callable[..., _R]]: ...

        @overload
        def register(
            self,
            cls: Callable[..., _R],
            /,
            func: None = None,
        ) -> partial[Callable[..., _R]]: ...

    def register(
        self,
        cls: type[Any] | Callable[..., _R],
        /,
        func: Callable[_P, _R] | None = None,
    ) -> Callable[_P, _R] | partial[Callable[_P, _R]]:
        """
        Register a new function as a dispatcher for `cls`.

        For usage guide, please see the
        [`class_singledispatch`][class_singledispatch.class_singledispatch]
        documentation.
        """
        if isinstance(cls, type):
            if func is None:
                return partial(self.register, cls)
        else:
            if func is not None:
                msg = (
                    f"Invalid first argument to `register()`. "
                    f"{cls!r} is not a runtime class."
                )
                raise TypeError(msg)
            func = cls
            cls = resolve_annotated_type(func)

        self._dispatch.register(cls, func)
        return func

    def _clear_cache(self) -> None:  # pragma: no cover
        self._dispatch._clear_cache()  # noqa: SLF001

    def __call__(self, cls: type[Any], /, *args: Any, **kwargs: Any) -> _R:
        return self.dispatch(cls)(cls, *args, **kwargs)


def class_singledispatch(
    func: Callable[..., _R],
    /,
) -> _ClassSingleDispatchCallable[_R]:
    """
    Use [`functools.singledispatch`][functools.singledispatch] to dispatch
    classes as parameters.

    While `singledispatch` examines the class of the first user argument,
    [`class_singledispatch`][class_singledispatch.class_singledispatch] uses
    the first argument as the class itself and performs the same task with it
    as `singledispatch`.

    ```python
    class T:
        pass

    class OtherT:
        pass

    @class_singledispatch
    def on_class(cls: type[T], /) -> None:
        print("T!")

    @on_class.register
    def on_other_class(cls: type[OtherT], /) -> None:
        print("OtherT!")

    # Useful for <3.10 without eval_type_backport:
    # Pass the class to the decorator not to use the annotation for resolution
    @on_class.register(SomeOtherT)
    def on_some_other_class(cls: type[SomeOtherT], /) -> None:
        print("SomeOtherT!")

    on_class(T)  # T!
    on_class(OtherT)  #  OtherT!
    on_class(SomeOtherT)  #  SomeOtherT!
    ```
    """  # noqa: D205
    return _ClassSingleDispatchCallable(func)
