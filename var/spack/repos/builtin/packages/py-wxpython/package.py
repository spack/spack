# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWxpython(PythonPackage):
    """Cross platform GUI toolkit for Python."""

    homepage = "https://www.wxpython.org/"
    pypi = "wxPython/wxPython-4.0.6.tar.gz"

    version('4.1.1', sha256='00e5e3180ac7f2852f342ad341d57c44e7e4326de0b550b9a5c4a8361b6c3528')
    version('4.1.0', sha256='2e2475cb755ac8d93d2f9335c39c060b4d17ecb5d4e0e86626d1e2834b64a48b')
    version('4.0.7', sha256='3be608bfdede3063678cc703453850ab0a018b82bafd5ee057302250b18f0233')
    version('4.0.6', sha256='35cc8ae9dd5246e2c9861bb796026bbcb9fb083e4d49650f776622171ecdab37')

    depends_on('wxwidgets')

    # Needed for the build.py script
    depends_on('py-setuptools', type='build')
    depends_on('py-pathlib2', type='build')

    # Needed at runtime
    depends_on('py-numpy', type='run')
    depends_on('pil', type='run')
    depends_on('py-six', type='run')
