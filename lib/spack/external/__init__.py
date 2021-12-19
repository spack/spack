# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module contains the following external, potentially separately
licensed, packages that are included in Spack:

archspec
--------

* Homepage: https://pypi.python.org/pypi/archspec
* Usage: Labeling, comparison and detection of microarchitectures
* Version: 0.1.2 (commit 85757b6666422fca86aa882a769bf78b0f992f54)

argparse
--------

* Homepage: https://pypi.python.org/pypi/argparse
* Usage: We include our own version to be Python 3.X compatible.
* Version: 1.4.0
* Note: This package has been slightly modified to improve
  error message formatting. See the following commit if the
  vendored copy ever needs to be updated again:
  https://github.com/spack/spack/pull/6786/commits/dfcef577b77249106ea4e4c69a6cd9e64fa6c418

ctest_log_parser
----------------

* Homepage: https://github.com/Kitware/CMake/blob/master/Source/CTest/cmCTestBuildHandler.cxx
* Usage: Functions to parse build logs and extract error messages.
* Version: Unversioned
* Note: This is a homemade port of Kitware's CTest build handler.

distro
------

* Homepage: https://pypi.python.org/pypi/distro
* Usage: Provides a more stable linux distribution detection.
* Version: 1.6.0 (64946a1e2a9ff529047070657728600e006c99ff)
* Note: Last version supporting Python 2.7

functools32
-----------
* Homepage: https://github.com/MiCHiLU/python-functools32
* Usage: Needed by jsonschema when using Python 2.7.
* Version: 3.2.3-2

jinja2
------

* Homepage: https://pypi.python.org/pypi/Jinja2
* Usage: A modern and designer-friendly templating language for Python.
* Version: 2.11.3 (last version supporting Python 2.7)

jsonschema
----------

* Homepage: https://pypi.python.org/pypi/jsonschema
* Usage: An implementation of JSON Schema for Python.
* Version: 2.4.0 (last version before functools32 dependency was added)
* Note: functools32 doesn't support Python 2.6 or 3.0, so jsonschema
  cannot be upgraded any further until we drop 2.6.
  Also, jsonschema/validators.py has been modified NOT to try to import
  requests (see 7a1dd517b8).

markupsafe
----------

* Homepage: https://pypi.python.org/pypi/MarkupSafe
* Usage: Implements a XML/HTML/XHTML Markup safe string for Python.
* Version: 1.1.1 (last version supporting Python 2.7)

py
--

* Homepage: https://pypi.python.org/pypi/py
* Usage: Needed by pytest. Library with cross-python path,
  ini-parsing, io, code, and log facilities.
* Version: 1.4.34 (last version supporting Python 2.6)
* Note: This packages has been modified:
  * https://github.com/pytest-dev/py/pull/186 was backported

pytest
------

* Homepage: https://pypi.python.org/pypi/pytest
* Usage: Testing framework used by Spack.
* Version: 3.2.5 (last version supporting Python 2.6)
* Note: This package has been slightly modified:
  * We improve Python 2.6 compatibility. See:
    https://github.com/spack/spack/pull/6801.
  * We have patched pytest not to depend on setuptools. See:
    https://github.com/spack/spack/pull/15612

ruamel.yaml
------

* Homepage: https://yaml.readthedocs.io/
* Usage: Used for config files. Ruamel is based on PyYAML but is more
  actively maintained and has more features, including round-tripping
  comments read from config files.
* Version: 0.11.15 (last version supporting Python 2.6)
* Note: This package has been slightly modified to improve Python 2.6
  compatibility -- some ``{}`` format strings were replaced, and the
  import for ``OrderedDict`` was tweaked.

six
---

* Homepage: https://pypi.python.org/pypi/six
* Usage: Python 2 and 3 compatibility utilities.
* Version: 1.16.0

macholib
--------

* Homepage: https://macholib.readthedocs.io/en/latest/index.html#
* Usage: Manipulation of Mach-o binaries for relocating macOS buildcaches on Linux
* Version: 1.12

altgraph
--------

* Homepage: https://altgraph.readthedocs.io/en/latest/index.html
* Usage: dependency of macholib
* Version: 0.16.1

"""
