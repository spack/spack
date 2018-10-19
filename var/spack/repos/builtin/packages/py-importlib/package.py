# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyImportlib(PythonPackage):
    """Packaging for importlib from Python 2.7"""

    homepage = "https://github.com/brettcannon/importlib"
    url      = "https://pypi.io/packages/source/i/importlib/importlib-1.0.4.zip"

    version('1.0.4', '5f9a0803bca7ba95f670d1464984296f')
