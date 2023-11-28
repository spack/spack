# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRarfile(PythonPackage):
    """RAR archive reader for Python."""

    homepage = "https://github.com/markokr/rarfile"
    pypi = "rarfile/rarfile-4.0.tar.gz"

    version("4.1", sha256="db60b3b5bc1c4bdeb941427d50b606d51df677353385255583847639473eda48")
    version("4.0", sha256="67548769229c5bda0827c1663dce3f54644f9dbfba4ae86d4da2b2afd3e602a1")

    depends_on("py-setuptools", type="build")
    depends_on("unrar", type="run")
