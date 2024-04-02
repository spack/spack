# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeovimRemote(PythonPackage):
    """Remote opening and control for neovim: nvr"""

    homepage = "https://github.com/mhinz/neovim-remote"
    pypi = "neovim-remote/neovim-remote-2.4.0.tar.gz"

    maintainers("trws")

    license("MIT")

    version(
        "2.4.0",
        sha256="4fa2ee4203dea2930ee19042dd22a25a97622cdda7258f99dd87ea0b417dee84",
        url="https://pypi.org/packages/f2/8d/4ad4a14bb226a4121ed0a76bf38959f71c556a81adf378ccfcbc679f8537/neovim_remote-2.4.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-psutil")
        depends_on("py-pynvim", when="@:2.2,2.4:")
        depends_on("py-setuptools")
