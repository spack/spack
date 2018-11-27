# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyproj(PythonPackage):
    """Python interface to the PROJ.4 Library."""

    homepage = "http://jswhit.github.io/pyproj/"
    url      = "https://github.com/jswhit/pyproj/tarball/v1.9.5.1rel"
    git      = "https://www.github.com/jswhit/pyproj.git"

    # This is not a tagged release of pyproj.
    # The changes in this "version" fix some bugs, especially with Python3 use.
    version('1.9.5.1.1', commit='0be612cc9f972e38b50a90c946a9b353e2ab140f')
    version('1.9.5.1', 'a4b80d7170fc82aee363d7f980279835')

    depends_on('py-cython', type='build')
    depends_on('py-setuptools', type='build')

    # NOTE: py-pyproj does NOT depends_on('proj').
    # The py-proj git repo actually includes the correct version of PROJ.4,
    # which is built internally as part of the py-proj build.
    # Adding depends_on('proj') will cause mysterious build errors.
