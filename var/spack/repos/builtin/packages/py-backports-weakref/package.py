# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackportsWeakref(PythonPackage):
    """Backports of new features in Python's weakref module"""

    homepage = "https://github.com/PiDelport/backports.weakref"
    pypi = "backports.weakref/backports.weakref-1.0.post1.tar.gz"

    license("PSF-2.0")

    version(
        "1.0.post1",
        sha256="81bc9b51c0abc58edc76aefbbc68c62a787918ffe943a37947e162c3f8e19e82",
        url="https://pypi.org/packages/88/ec/f598b633c3d5ffe267aaada57d961c94fdfa183c5c3ebda2b6d151943db6/backports.weakref-1.0.post1-py2.py3-none-any.whl",
    )
    version(
        "1.0-rc1",
        sha256="622badff14e0b62703b479244e2ebde2f1c19c266a1edc00608232f4dd3544f4",
        url="https://pypi.org/packages/6a/f7/ae34b6818b603e264f26fe7db2bd07850ce331ce2fde74b266d61f4a2d87/backports.weakref-1.0rc1-py3-none-any.whl",
    )
