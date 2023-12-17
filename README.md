
# class_singledispatch [![Package version](https://img.shields.io/pypi/v/class-singledispatch?label=PyPI)](https://pypi.org/project/class-singledispatch/) [![Supported Python versions](https://img.shields.io/pypi/pyversions/class-singledispatch.svg?logo=python&label=Python)](https://pypi.org/project/class-singledispatch/)
[![Tests](https://github.com/bswck/class_singledispatch/actions/workflows/test.yml/badge.svg)](https://github.com/bswck/class_singledispatch/actions/workflows/test.yml)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/bswck/class_singledispatch.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/bswck/class_singledispatch)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg?label=Code%20style)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/bswck/class_singledispatch.svg?label=License)](https://github.com/bswck/class_singledispatch/blob/HEAD/LICENSE)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

A ``singledispatch()`` for arguments that are classes annotated as specific types.

Inspired by https://github.com/python/cpython/issues/100623.

# A simple example
Use `functools.singledispatch` to singledispatch classes as parameters.

While `functools.singledispatch` examines the class of the first user argument,
`class_singledispatch` uses the first argument as the class itself and performs
the same task with it as `functools.singledispatch`.

```python
from class_singledispatch import class_singledispatch


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


# Useful for <=3.10 as soon as `@class_singledispatch` allows specifying
# similarly to `.register`:
# Pass the class to the decorator not to use the annotation for resolution
@on_class.register(SomeOtherT)
def on_some_other_class(cls: type[SomeOtherT], /) -> None:
    print("SomeOtherT!")


on_class(T)  # T!
on_class(OtherT)  #  OtherT!
on_class(SomeOtherT)  #  SomeOtherT!
```


# Installation
If you want to…



## …use this tool in your project 💻
You might simply install it with pip:

```shell
pip install class-singledispatch
```

If you use [Poetry](https://python-poetry.org/), then run:

```shell
poetry add class-singledispatch
```

## …contribute to [class_singledispatch](https://github.com/bswck/class_singledispatch) 🚀

<!--
This section was generated from bswck/skeleton@6253cb7.
Instead of changing this particular file, you might want to alter the template:
https://github.com/bswck/skeleton/tree/6253cb7/fragments/guide.md
-->

> [!Note]
> If you use Windows, it is highly recommended to complete the installation in the way presented below through [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).



1.  Fork the [class_singledispatch repository](https://github.com/bswck/class_singledispatch) on GitHub.

1.  [Install Poetry](https://python-poetry.org/docs/#installation).<br/>
    Poetry is an amazing tool for managing dependencies & virtual environments, building packages and publishing them.
    You might use [pipx](https://github.com/pypa/pipx#readme) to install it globally (recommended):

    ```shell
    pipx install poetry
    ```

    <sub>If you encounter any problems, refer to [the official documentation](https://python-poetry.org/docs/#installation) for the most up-to-date installation instructions.</sub>

    Be sure to have Python 3.8 installed—if you use [pyenv](https://github.com/pyenv/pyenv#readme), simply run:

    ```shell
    pyenv install 3.8
    ```

1.  Clone your fork locally and install dependencies.

    ```shell
    git clone https://github.com/your-username/class_singledispatch path/to/class_singledispatch
    cd path/to/class_singledispatch
    poetry env use $(cat .python-version)
    poetry install
    ```

    Next up, simply activate the virtual environment and install pre-commit hooks:

    ```shell
    poetry shell
    pre-commit install --hook-type pre-commit --hook-type pre-push
    ```

For more information on how to contribute, check out [CONTRIBUTING.md](https://github.com/bswck/class_singledispatch/blob/HEAD/CONTRIBUTING.md).<br/>
Always happy to accept contributions! ❤️


# Legal info
© Copyright by Bartosz Sławecki ([@bswck](https://github.com/bswck)).
<br />This software is licensed under the terms of [MIT License](https://github.com/bswck/class_singledispatch/blob/HEAD/LICENSE).
