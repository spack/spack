# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""This module contains the following external, potentially separately
licensed, packages that are included in Spack:

altgraph
--------

* Homepage: https://altgraph.readthedocs.io/en/latest/index.html
* Usage: dependency of macholib
* Version: 0.17.3
* License: MIT

archspec
--------

* Homepage: https://pypi.python.org/pypi/archspec
* Usage: Labeling, comparison and detection of microarchitectures
* Version: 0.2.5 (commit 38ce485258ffc4fc6dd6688f8dc90cb269478c47)
* License: Apache-2.0 or MIT

astunparse
----------------

* Homepage: https://github.com/simonpercivall/astunparse
* Usage: Unparsing Python ASTs for package hashes in Spack
* Version: 1.6.3 (plus modifications)
* License: PSF-2.0
* Note: This is in ``spack.util.unparse`` because it's very heavily
  modified, and we want to track coverage for it.
  Specifically, we have modified this library to generate consistent unparsed ASTs
  regardless of the Python version. It is based on:
    1. The original ``astunparse`` library;
    2. Modifications for consistency;
    3. Backports from the ``ast.unparse`` function in Python 3.9 and later
  The unparsing is now mostly consistent with upstream ``ast.unparse``, so if
  we ever require Python 3.9 or higher, we can drop this external package.

attrs
----------------

* Homepage: https://github.com/python-attrs/attrs
* Usage: Needed by jsonschema.
* Version: 22.1.0
* License: MIT

ctest_log_parser
----------------

* Homepage: https://github.com/Kitware/CMake/blob/master/Source/CTest/cmCTestBuildHandler.cxx
* Usage: Functions to parse build logs and extract error messages.
* Version: Unversioned
* License: BSD-3-Clause
* Note: This is a homemade port of Kitware's CTest build handler.

distro
------

* Homepage: https://pypi.python.org/pypi/distro
* Usage: Provides a more stable linux distribution detection.
* Version: 1.8.0
* License: Apache-2.0

jinja2
------

* Homepage: https://pypi.python.org/pypi/Jinja2
* Usage: A modern and designer-friendly templating language for Python.
* Version: 3.0.3 (last version supporting Python 3.6)
* License: BSD-3-Clause

jsonschema
----------

* Homepage: https://pypi.python.org/pypi/jsonschema
* Usage: An implementation of JSON Schema for Python.
* Version: 3.2.0 (last version before 2.7 and 3.6 support was dropped)
* License: MIT
* Note: We don't include tests or benchmarks; just what Spack needs.

macholib
--------

* Homepage: https://macholib.readthedocs.io/en/latest/index.html#
* Usage: Manipulation of Mach-o binaries for relocating macOS buildcaches on Linux
* Version: 1.16.2
* License: MIT

markupsafe
----------

* Homepage: https://pypi.python.org/pypi/MarkupSafe
* Usage: Implements a XML/HTML/XHTML Markup safe string for Python.
* Version: 2.0.1 (last version supporting Python 3.6)
* License: BSD-3-Clause

pyrsistent
----------

* Homepage: http://github.com/tobgu/pyrsistent/
* Usage: Needed by `jsonschema`
* Version: 0.18.0
* License: MIT

ruamel.yaml
------

* Homepage: https://yaml.readthedocs.io/
* Usage: Used for config files. Ruamel is based on PyYAML but is more
  actively maintained and has more features, including round-tripping
  comments read from config files.
* Version: 0.17.21
* License: MIT

six
---

* Homepage: https://pypi.python.org/pypi/six
* Usage: Python 2 and 3 compatibility utilities.
* Version: 1.16.0
* License: MIT

"""
