---
title: "Using uv to extend Python with C-code"
weight: 90
date: 2026-01-06T00:00:00Z
description: |
  A walkthrough of a `uv` usage, here to extend Python with two C functions.
  The functionality of the C extension, "hello world", is actually unimportant.
  We use it to show a build system that can drive a C-compiler, and integrate with Python to build a wheel.

---

{{% details title="**Summary**" open=true %}}
A walkthrough of a `uv` usage, here to extend Python with two C functions.
The functionality of the C extension, "hello world", is actually unimportant.
We use it to show a build system that can drive a C-compiler, and integrate with Python to build a wheel.
{{% /details %}}

This walkthrough builds a small C extension to Python, "helloext".
It defines two C functions that are being called from Python.
The goal is not the `helloext` funcitonality.
Instead we use it to demonstrate a different build system, how to build a Wheel with C extensions,
and how to package and install it.

# Create a project

Our project is called `helloext`.
It will use Python 3.12, and we will be using `--managed-python`.
We are using the usual `--package` structure, because what we want to write is a package, just written in C.

```
mkdir helloext
cd helloext
uv init --package --managed-python --python 3.12
```

We get the usual tree:

```
$ tree
.
|-- .gitignore
|-- .python-version
|-- README.md
|-- pyproject.toml
`-- src
    `-- helloext
        `-- __init__.py
```

Our end state will look a bit differently than before:

```
$ tree -a -I .git
.
|-- .gitignore
|-- .python-version
|-- CMakeLists.txt
|-- README.md
|-- pyproject.toml
|-- src
|   `-- helloext
|       |-- __init__.py
|       `-- _hello.c
|-- tests
|   `-- test_hello.py
`-- uv.lock
```

That is, we will have our Python code for the module in `src/helloext/__init__.py`,
the C code in `_hello.c` right next to it.

We will be using a different build system that can handle C code: `scikit-build-core`.
This uses `cmake`, so we need a `CmakeLists.txt` file.

## Tests

We begin with writing tests that define what we want:

```python
# cat tests/test_hello.py
from __future__ import annotations

from helloext import hellop, hellos


def test_hellos():
    assert hellos("Kris") == "Hello, Kris"


def test_hellop(capsys):
    hellop("Kris")
    captured = capsys.readouterr()
    assert captured.out == "Hello, Kris\n"
```

That is, we will be having an extension `helloext` that defines two functions, `hellop()` and `hellos()`.

One will be `hellop(name: str) -> None`.
It will take a string `name`, and print `Hello, {name}\n` with a linefeed at the end.

The other function will be `hellos(name: str) -> str`.
It will take a string `name`, and return a string `Hello, {name}` without a linefeed at the end.

We record these facts as tests, using the name "Kris" for testing.
The `hellos()` assertion is trivial: `assert hellos("Kris") == "Hello, Kris"`.
The `hellop()` uses `capsys` to capture system output, and then can do the same assertion on captured output.

## Writing the Python part of the extension

Our module, `src/helloext` is a module, because the directory contains a file named `__init__.py`.
This file imports what is necessary from other submodules, and collects the symbols we want to export with `helloext`,
in the `__all__` list.

This is how we get an orderly namespace:

```python
from __future__ import annotations

from ._hello import hellop, hellos

__all__ = ["hellop", "hellos"]
```

The module `._hello` is the C code module in the form of a `_hello.so` file in the current directory, `.`.

## The C code for `helloext`

We are not going into the details of how to write Python extensions in C in this class.
But if you ever saw the structure of an extension in PHP, lua or other languages that integrate C modules,
this will look familiar to you:

```c
// cat src/helloext/_hello.c

#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject *hellop(PyObject *self, PyObject *args) {
    const char *name = NULL;

    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }

    PySys_WriteStdout("Hello, %s\n", name);
    Py_RETURN_NONE;
}

static PyObject *hellos(PyObject *self, PyObject *args) {
    const char *name = NULL;

    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }

    return PyUnicode_FromFormat("Hello, %s", name);
}

static PyMethodDef HelloMethods[] = {
    {"hellop", hellop, METH_VARARGS, "Print Hello, {name} to stdout."},
    {"hellos", hellos, METH_VARARGS, "Return Hello, {name} as a string."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef hellomodule = {
    PyModuleDef_HEAD_INIT,
    "_hello",
    "Example CPython extension module.",
    -1,
    HelloMethods
};

PyMODINIT_FUNC PyInit__hello(void) {
    return PyModule_Create(&hellomodule);
}
```

Read bottom to top: A module initializer creates a new module, and points to a module definition, `hellomodule`.
The module definition contains, among other metadata, an array of functions, `HelloMethods`.
This NULL terminated array contains structures that define the functions, and the way they get parameters.

Each function reads Python parameters and converts them into something C can use.
We use the Type "s", which is a Python "utf-8 with surrogates" string.

We then call appropriate Python API functions such as `PySys_WriteStdout()` to print,
or `PyUnicode_FromFormat()` to get a formatted dynamic string from memory that Python owns.

This code now needs to be compiled: `cmake` compiles this, using the `CMakeLists.txt`,
and the `pyproject.toml` tells `uv` how to call `cmake` and set it up.

## The `cmake` definition

We create a file `CMakeLists.txt` in the project root:

```cmake
# cat CMakeLists.txt
cmake_minimum_required(VERSION 3.20)
project(helloext LANGUAGES C)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

Python_add_library(_hello MODULE src/helloext/_hello.c)

set_target_properties(_hello PROPERTIES
  OUTPUT_NAME "_hello"
)

if (WIN32)
  set_target_properties(_hello PROPERTIES SUFFIX ".pyd")
endif()

install(TARGETS _hello LIBRARY DESTINATION helloext)
```

This declares minimum version requirements, names project name and language, and finds the required components,
basically Python and the needed API includes from the SDK.

We create a library, "_hello.so", which we tell `cmake` with `Python_add_library`.

We need to collect the deliverable and install it, that is,
we build a Python Wheel and the compiled artifact needs to be added to the Wheel.
This is what the `install()` line does.

## Our `pyproject.toml`

Our `pyproject.toml` has a few special options:

```toml
# cat pyproject.toml
[project]
name = "helloext"
version = "0.1.0"
description = "Example CPython C extension with uv + scikit-build-core"
readme = "README.md"
authors = [
    { name = "Kristian Koehntopp", email = "kris-git@koehntopp.de" }
]
requires-python = ">=3.12"
dependencies = []

[build-system]
requires = ["scikit-build-core>=0.11", ]
build-backend = "scikit_build_core.build"

[tool.uv]
package = true

[tool.scikit-build]
cmake.version = ">=3.20"
# build.verbose = true
wheel.packages = ["src/helloext"]

[dependency-groups]
dev = [
    "ruff>=0.14.10",
]
test = [
    "pytest>=9.0.2",
]
```

We are defining a non-standard `[build-system]`, `scikit-build-core.build` (with a minimum version requirement).

We also define a toml table `[tool.scikit-build]` to set options:
- `cmake.version>=3.20` sets a minimum version requirement for `cmake`.
  This must match the requirement in the `CMakeLists.txt` itself.
- `wheel.packages` tells the build system where our package to build are.
- optionally we can set `build.verbose` to `true` to get more build debug output.

The other options we should be familiar with by now.

## Building

We can now build:

``` 
$ uv build
Building source distribution...
*** scikit-build-core 0.11.6 (sdist)
Building wheel from source distribution...
*** scikit-build-core 0.11.6 using CMake 4.2.1 (wheel)
*** Configuring CMake...
loading initial cache file /var/folders/dn/vtkw12w17qv7cqw5yj6lmgjh0000gn/T/tmpe31qrwbm/build/CMakeInit.txt
-- The C compiler identification is AppleClang 17.0.0.17000404
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Found Python: /Users/kris/.cache/uv/builds-v0/.tmp8Kf7xj/bin/python (found version "3.12.12") found components: Interpreter Development.Module
-- Configuring done (0.4s)
-- Generating done (0.0s)
-- Build files have been written to: /var/folders/dn/vtkw12w17qv7cqw5yj6lmgjh0000gn/T/tmpe31qrwbm/build
*** Building project with Ninja...
Change Dir: '/var/folders/dn/vtkw12w17qv7cqw5yj6lmgjh0000gn/T/tmpe31qrwbm/build'

Run Build Command(s): /Users/kris/.cache/uv/builds-v0/.tmp8Kf7xj/bin/ninja -v
[1/2] /usr/bin/cc -D_hello_EXPORTS -isystem /Users/kris/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/include/python3.12 -O3 -DNDEBUG -arch arm64 -fPIC -MD -MT CMakeFiles/_hello.dir/src/helloext/_hello.c.o -MF CMakeFiles/_hello.dir/src/helloext/_hello.c.o.d -o CMakeFiles/_hello.dir/src/helloext/_hello.c.o -c /Users/kris/.cache/uv/sdists-v9/.tmpCf0QjY/helloext-0.2.0/src/helloext/_hello.c
[2/2] : && /usr/bin/cc -O3 -DNDEBUG -arch arm64 -bundle -Wl,-headerpad_max_install_names -Xlinker -undefined -Xlinker dynamic_lookup -o _hello.so CMakeFiles/_hello.dir/src/helloext/_hello.c.o   && :

*** Installing project into wheel...
-- Install configuration: "Release"
-- Installing: /var/folders/dn/vtkw12w17qv7cqw5yj6lmgjh0000gn/T/tmpe31qrwbm/wheel/platlib/helloext/_hello.so
*** Making wheel...
*** Created helloext-0.2.0-cp312-cp312-macosx_26_0_arm64.whl
Successfully built dist/helloext-0.2.0.tar.gz
Successfully built dist/helloext-0.2.0-cp312-cp312-macosx_26_0_arm64.whl
```

This creates the `dist/` directory with two files in it:
- The `dist/helloext-0.2.0.tar.gz` with the source distribution for the wheel.
- The `dist/helloext-0.2.0-cp312-cp312-macosx_26_0_arm64.whl`, which is the actual wheel.

```bash
kk:helloext kris$ ls -l dist
total 24
-rw-r--r--  1 kris  staff  3338 Jan  6 10:31 helloext-0.2.0-cp312-cp312-macosx_26_0_arm64.whl
-rw-r--r--  1 kris  staff  5605 Jan  6 10:31 helloext-0.2.0.tar.gz
```

Our wheel contains the usual platform triple: cp312 for Python 3.12, but this time it's not "None-Any",
because the C code is platform specific.
Instead we get the API `cp312` (CPYthon 3.12) in the API field, 
and "macosx_26_0_arm64" for the OS field.
If our deployment needs to cover more or other platforms,
we need to set up a build farm and collect artifacts to spare our users the build.

A wheel is a ZIP file, so we can `unzip -v` this:

```
kk:helloext kris$ unzip -v dist/helloext-0.2.0-cp312-cp312-macosx_26_0_arm64.whl
Archive:  dist/helloext-0.2.0-cp312-cp312-macosx_26_0_arm64.whl
 Length   Method    Size  Cmpr    Date    Time   CRC-32   Name
--------  ------  ------- ---- ---------- ----- --------  ----
     287  Defl:N      132  54% 01-06-2026 09:31 0b99c49a  helloext/__init__.py
     944  Defl:N      434  54% 01-06-2026 09:31 c98a34aa  helloext/_hello.c
   50232  Defl:N     1409  97% 01-06-2026 09:31 bd8c2210  helloext/_hello.so
     239  Defl:N      188  21% 01-06-2026 09:31 4b7d2706  helloext-0.2.0.dist-info/METADATA
     114  Defl:N      107   6% 01-06-2026 09:31 6e776e32  helloext-0.2.0.dist-info/WHEEL
     434  Defl:N      292  33% 01-06-2026 09:31 fe074413  helloext-0.2.0.dist-info/RECORD
--------          -------  ---                            -------
   52250             2562  95%                            6 files
```

The important check here is that our wheel contains the `__init__.py` for the Python part of the module,
and the `_hello.so` for the C/machine level part of the code.

Had we left out the `install()` in the `CMakeLists.txt` file, only the native Python part would be present,
but the `.so` file would be missing.

## Installing and Reinstalling

`uv` does not manage Non-Python parts of our environment.
We need to install a C-compiler, `cmake` or `ninja` (depending on scikit setup),
and the required tools and libraries to compile our C code.

`uv` also does not manage the freshness of the C code.
Because of that we `--reinstall` or `--reinstall-package <packagename>` to force a recompile and reinstall of the Wheel:

``` 
$ uv sync --reinstall --all-groups
Using CPython 3.12.12
Creating virtual environment at: .venv
Resolved 8 packages in 6ms
      Built helloext @ file:///Users/kris/Source/uv-class/examples/helloext
Prepared 7 packages in 1.33s
Installed 7 packages in 12ms
 + helloext==0.2.0 (from file:///Users/kris/Source/uv-class/examples/helloext)
 + iniconfig==2.3.0
 + packaging==25.0
 + pluggy==1.6.0
 + pygments==2.19.2
 + pytest==9.0.2
 + ruff==0.14.10
```

We can inspect the `.venv` to see the extension and its metadata:

``` 
kk:helloext kris$ ls -l .venv/lib/python3.12/site-packages/
total 64
-rw-r--r--   1 kris  staff    58 Jan  6 15:18 _helloext_editable.pth
-rw-r--r--   1 kris  staff  9240 Jan  6 15:18 _helloext_editable.py
drwxr-xr-x  57 kris  staff  1824 Jan  6 15:18 _pytest
-rw-r--r--   1 kris  staff    18 Jan  6 15:16 _virtualenv.pth
-rw-r--r--   1 kris  staff  4342 Jan  6 15:16 _virtualenv.py
drwxr-xr-x   3 kris  staff    96 Jan  6 15:18 helloext
drwxr-xr-x  10 kris  staff   320 Jan  6 15:18 helloext-0.1.0.dist-info
drwxr-xr-x   7 kris  staff   224 Jan  6 15:18 iniconfig
drwxr-xr-x   9 kris  staff   288 Jan  6 15:18 iniconfig-2.3.0.dist-info
drwxr-xr-x  18 kris  staff   576 Jan  6 15:18 packaging
drwxr-xr-x   8 kris  staff   256 Jan  6 15:18 packaging-25.0.dist-info
drwxr-xr-x  11 kris  staff   352 Jan  6 15:18 pluggy
drwxr-xr-x   9 kris  staff   288 Jan  6 15:18 pluggy-1.6.0.dist-info
-rw-r--r--   1 kris  staff   329 Dec 14 10:59 py.py
drwxr-xr-x  22 kris  staff   704 Jan  6 15:18 pygments
drwxr-xr-x   9 kris  staff   288 Jan  6 15:18 pygments-2.19.2.dist-info
drwxr-xr-x   5 kris  staff   160 Jan  6 15:18 pytest
drwxr-xr-x  10 kris  staff   320 Jan  6 15:18 pytest-9.0.2.dist-info
drwxr-xr-x   4 kris  staff   128 Jan  6 15:18 ruff
drwxr-xr-x   8 kris  staff   256 Jan  6 15:18 ruff-0.14.10.dist-info
kk:helloext kris$ ls -l .venv/lib/python3.12/site-packages/helloext
total 104
-rwxr-xr-x  1 kris  staff  50232 Jan  6 15:18 _hello.so
```

The extension is in `.venv/lib/python3.12/site-packages/helloext`, and we see the `_hello.so` file in there.
The metadata is in the `dist-info` directory right next to it, with the usual metadata files.

## Running the tests and using the extension

We then can run out tests as usual, and they will now succeed, using our C code functions instead of native Python:

``` 
$ uv run pytest
============================ test session starts =============================
platform darwin -- Python 3.12.12, pytest-9.0.2, pluggy-1.6.0
rootdir: /Users/kris/Source/uv-class/examples/helloext
configfile: pyproject.toml
collected 2 items

tests/test_hello.py ..                                                 [100%]

============================= 2 passed in 0.01s ==============================
```

We can also test manually:

```
$ uv run python
Python 3.12.12 (main, Dec 17 2025, 21:07:08) [Clang 21.1.4 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from helloext import hellos, hellop
>>> hellop("Kris")
Hello, Kris
>>> a = hellos("Kris")
>>> print(a)
Hello, Kris
```

# What can go wrong

## Successful build, but `No module named 'helloext._hello'`

We see a successful build, and even setting the `verbose` option reveals no errors.
Yet, when we try to import the module, we get the message `No module named 'helloext._hello'`.
This is the name of the `.so` file, `_hello.so`, so we do get the Python part in the init-file, but not the C component.

This is confirmed by listing the contents of the `.whl` file in `dist/` with `unzip -v`:
There is no `_hello.so` packaged.

This happens when we forget the `install()` clause in the `CMakeLists.txt`:

``` 
install(TARGETS _hello LIBRARY DESTINATION helloext)
```

## Editable installs vs. Proper Installs

When we run `uv run something`, we run it directly from the source directory.
The include path that Python uses is expanded, so that modules in `src` can be found and used.
This is called an "editable install".

```
kk:helloext kris$ uv run python
Python 3.12.12 (main, Dec 17 2025, 21:07:08) [Clang 21.1.4 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pprint
>>> import sys
>>> pprint.pprint(sys.path)
['',
 '/Users/kris/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python312.zip',
 '/Users/kris/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12',
 '/Users/kris/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12/lib-dynload',
 '/Users/kris/Source/uv-class/examples/helloext/.venv/lib/python3.12/site-packages',
 '/Users/kris/Source/uv-class/examples/helloext/src']
```

This works with pure python modules, because this will make `import helloext` search `src/helloext`,
the interpreter will find the module and import it.

The C compiler bulld system does the build elsewhere and does not put the module into `src/helloext`.

SciKit works around that by putting hooks into `site-packages`:

``` 
kk:helloext kris$ ls -l .venv/lib/python3.12/site-packages/
total 56
drwxr-xr-x   4 kris  staff   128 Jan  6 16:30 __pycache__
-rw-r--r--   1 kris  staff    58 Jan  6 16:42 _helloext_editable.pth
-rw-r--r--   1 kris  staff  9240 Jan  6 16:42 _helloext_editable.py
-rw-r--r--   1 kris  staff    18 Jan  6 16:30 _virtualenv.pth
-rw-r--r--   1 kris  staff  4342 Jan  6 16:30 _virtualenv.py
drwxr-xr-x   3 kris  staff    96 Jan  6 16:42 helloext
drwxr-xr-x  10 kris  staff   320 Jan  6 16:42 helloext-0.2.0.dist-info
drwxr-xr-x   4 kris  staff   128 Jan  6 16:30 ruff
drwxr-xr-x   8 kris  staff   256 Jan  6 16:30 ruff-0.14.10.dist-info
```

The `.venv/lib/python<versio>/site-packages/_helloext_editable.py` contains Python source that extents the `sys.path`,
but also provides hooks to load `.venv/lib/python<versio>/site-packages/helloext/_hello.so`.

If you check, you will find code that looks similar to this:

```python
import sys

def ScikitBuildRedirectingFinder(): ...

def install(
    known_source_files: dict[str, str],
    known_wheel_files: dict[str, str],
    path: str | None,
    rebuild: bool = False,
    verbose: bool = False,
    build_options: list[str] | None = None,
    install_options: list[str] | None = None,
    install_dir: str = "",
) -> None:
    """
    Install a meta path finder that redirects imports to the source files, and
    optionally rebuilds if path is given.

    :param known_source_files: A mapping of module names to source files
    :param known_wheel_files: A mapping of module names to wheel files
    :param path: The path to the build directory, or None
    :param verbose: Whether to print the cmake commands (also controlled by the
                    SKBUILD_EDITABLE_VERBOSE environment variable)
    :param install_dir: The wheel install directory override, if one was
                        specified
    """
    sys.meta_path.insert(
        0,
        ScikitBuildRedirectingFinder(
            known_source_files,
            known_wheel_files,
            path,
            rebuild,
            verbose,
            build_options or [],
            install_options or [],
            DIR,
            install_dir,
        ),
    )


install({'helloext': '/Users/kris/Source/uv-class/examples/helloext/src/helloext/__init__.py',
'helloext._hello': '/Users/kris/Source/uv-class/examples/helloext/src/helloext/_hello.c'},
{'helloext._hello': 'helloext/_hello.so'}, None, False, True, [], [], '')
```

This will try to wire things together even for editable installs.

Running `uv sync --reinstall-package helloext --no-cache --no-editable` will instead install all files into 
`.venv/lib/python<versio>/site-packages/helloext/` as one expects, and also not put `src` into the search path:

``` 
$ ls -l .venv/lib/python3.12/site-packages/helloext
total 120
-rw-r--r--  1 kris  staff    287 Jan  6 16:46 __init__.py
-rw-r--r--  1 kris  staff    944 Jan  6 16:46 _hello.c
-rwxr-xr-x  1 kris  staff  50232 Jan  6 16:46 _hello.so
kk:helloext kris$ uv run --no-cache --no-editable python
Python 3.12.12 (main, Dec 17 2025, 21:07:08) [Clang 21.1.4 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pprint
>>> import sys
>>> pprint.pprint(sys.path)
['',
 '/Users/kris/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python312.zip',
 '/Users/kris/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12',
 '/Users/kris/.local/share/uv/python/cpython-3.12.12-macos-aarch64-none/lib/python3.12/lib-dynload',
 '/Users/kris/Source/uv-class/examples/helloext/.venv/lib/python3.12/site-packages']
```

So we can see that SciKit goes to considerable lengths to set up the import path and environment for us,
even when we use an editable layout.

But "editable" is a Python thing, and `uv` scope ends at Python boundaries.
We still have to make sure SciKit knows things, and things are being rebuild when we change C sources.

## We fixed a bug, but the module is still broken

When we fix bugs in the C source, it may be that `uv` and Scikit work together to produce a new wheel,
but in testing the old wheel is still being used.

We can work around that by diligently increasing the version number:

``` 
uv version --bump patch
```

to increase the rightmost version number for a versioned compile.

Or we can tell `uv sync`, `uv run` and friends to not use the cache, and force-reinstall

```
uv run --all-groups --reinstall-package helloext ...
```

to force a fresh and uncached install.

# What we get

We get an extension for Python written in C that can be called like a native Python function.

It is delivered as an installable wheel with ABI and OS specific entries in the platform tuple,
so we potentially need a build farm to satisfy our supported platforms.

We can then `import` the C-module and use it.

We have tooling to drive the C build, but this part of the build is not managed by `uv`,
so it is our responsibility to drive the C part of the build.
This includes providing the compiler, the includes and SDKs or other parts of the Non-Python build.

# Exercises

## 1. Extensions
- **Reproduction:** When initializing the `helloext` project, which `uv init` flag is used to establish the `src` layout, and why is this layout preferred for packages?
- **Reproduction:** In the `pyproject.toml` file for a `scikit-build-core` project, what are the two keys required in the `[build-system]` table to define the frontend/backend relationship?
- **Application:** You want to see the detailed output of the C compiler and CMake during the build process. Which option should you add or uncomment in the `[tool.scikit-build]` section of your `pyproject.toml`?
- **Application:** After running `uv build`, you have a `.whl` file in the `dist/` directory. Provide a command-line example of how you can inspect the contents of this wheel to verify that the compiled `_hello.so` file is correctly packaged inside the `helloext` directory.
- **Transfer:** Your team is deciding whether to implement a new high-performance module in C using `scikit-build-core` or in Rust using `maturin`. 
    - Outline how the `[build-system]` configuration in `pyproject.toml` would differ between these two choices.
    - Identify which parts of the build stack `uv` manages (e.g., build isolation, Python dependencies) and which parts remain the developer's responsibility to provide on the host system (e.g., compilers, linker, system SDKs).
    - Discuss how `uv` handles the "freshness" of native code compared to pure Python code, and why commands like `uv sync --reinstall-package` are relevant in this workflow.
