##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""This module contains the following external, potentially separately
licensed, packages that are included in Spack:

argparse
--------

* Homepage: https://pypi.python.org/pypi/argparse
* Usage: We include our own version to be Python 2.6 compatible.
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
* Version: 1.0.4 (last version supporting Python 2.6)

functools
---------

* Homepage: https://github.com/python/cpython/blob/2.7/Lib/functools.py
* Usage: Used for implementation of total_ordering.
* Version: Unversioned
* Note: This is the functools.total_ordering implementation
  from Python 2.7 backported so we can run on Python 2.6.

jinja2
------

* Homepage: https://pypi.python.org/pypi/Jinja2
* Usage: A modern and designer-friendly templating language for Python.
* Version: 2.10

jsonschema
----------

* Homepage: https://pypi.python.org/pypi/jsonschema
* Usage: An implementation of JSON Schema for Python.
* Version: 2.4.0 (last version before functools32 dependency was added)
* Note: functools32 doesn't support Python 2.6 or 3.0, so jsonschema
  cannot be upgraded any further

markupsafe
----------

* Homepage: https://pypi.python.org/pypi/MarkupSafe
* Usage: Implements a XML/HTML/XHTML Markup safe string for Python.
* Version: 1.0

orderddict
----------

* Homepage: https://pypi.org/project/ordereddict/
* Usage: A drop-in substitute for Py2.7's new collections.OrderedDict
  that works in Python 2.4-2.6.
* Version: 1.1

py
--

* Homepage: https://pypi.python.org/pypi/py
* Usage: Needed by pytest. Library with cross-python path,
  ini-parsing, io, code, and log facilities.
* Version: 1.4.34 (last version supporting Python 2.6)

pyqver
------

* Homepage: https://github.com/ghewgill/pyqver
* Usage: External script to query required python version of
  python source code. Used for ensuring 2.6 compatibility.
* Version: Unversioned

pytest
------

* Homepage: https://pypi.python.org/pypi/pytest
* Usage: Testing framework used by Spack.
* Version: 3.2.5 (last version supporting Python 2.6)
* Note: This package has been slightly modified to improve
  Python 2.6 compatibility. See the following commit if the
  vendored copy ever needs to be updated again:
  https://github.com/spack/spack/pull/6801/commits/ff513c39f2c67ff615de5cbc581dd69a8ec96526

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
* Version: 1.11.0
"""
