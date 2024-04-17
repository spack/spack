# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPebble(PythonPackage):
    """Threading and multiprocessing eye-candy."""

    homepage = "https://github.com/noxdafox/pebble"
    pypi = "Pebble/Pebble-5.0.3.tar.gz"

    license("LGPL-3.0-only")

    version(
        "5.0.3",
        sha256="8274aa0959f387b368ede47666129cbe5d123f276a1bd9cafe77e020194b2141",
        url="https://pypi.org/packages/3d/e4/51d112fbc10e51a37519635c757a1a6a8a3058ee91bf89632ab720a8cfac/Pebble-5.0.3-py3-none-any.whl",
    )
