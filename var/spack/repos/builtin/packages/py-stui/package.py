# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStui(PythonPackage):
    """A Slurm dashboard for the terminal."""

    homepage = "https://github.com/mi-lad/stui"
    pypi = "stui/stui-0.3.6.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version(
        "0.3.6",
        sha256="441a3e7c8e9b9991c833f8c2a278009fadb97adee49cdeaa581355575fb7a418",
        url="https://pypi.org/packages/8e/47/02763888893798f4c5be9adae4b5f56f6e921238370c5739c08241d6886e/stui-0.3.6-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-fabric@2.5:", when="@0.2:")
        depends_on("py-urwid")
