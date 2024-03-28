# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyH5sh(PythonPackage):
    """Shell-like environment for HDF5."""

    homepage = "https://github.com/sethrj/h5sh"
    pypi = "h5sh/h5sh-0.1.1.tar.gz"

    maintainers("sethrj")

    license("BSD-3-Clause")

    version(
        "0.1.1",
        sha256="5e2d41aca376d34d1fe381e52c37216442334e3d7a0dbc9f591ea07166c8ce84",
        url="https://pypi.org/packages/4f/30/578bce8b4eb4fe48c65c1b2de2860062f9ffadddebb63a1234709799b61d/h5sh-0.1.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-h5py@2.7.1:")
        depends_on("py-numpy@1.15.0:")
        depends_on("py-prompt-toolkit@2:")
        depends_on("py-pygments")
        depends_on("py-six", when="@0.1.1:")
