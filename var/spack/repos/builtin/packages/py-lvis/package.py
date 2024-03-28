# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyLvis(PythonPackage):
    """Python API for LVIS dataset."""

    pypi = "lvis/lvis-0.5.3.tar.gz"

    version(
        "0.5.3",
        sha256="4f07153330df342b3161fafb46641ce7c02864113a8ddf0d6ffab6b02407bef0",
        url="https://pypi.org/packages/72/b6/1992240ab48310b5360bfdd1d53163f43bb97d90dc5dc723c67d41c38e78/lvis-0.5.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-cycler@0.10:", when="@0.5.3:")
        depends_on("py-cython@0.29.12:", when="@0.5.3:")
        depends_on("py-kiwisolver@1.1:", when="@0.5.3:")
        depends_on("py-matplotlib@3.1.1:", when="@0.5.3:")
        depends_on("py-numpy@1.18.2:", when="@0.5.3:")
        depends_on("py-opencv-python@4.1:", when="@0.5.3:")
        depends_on("py-pyparsing@2.4:", when="@0.5.3:")
        depends_on("py-python-dateutil@2.8:", when="@0.5.3:")
        depends_on("py-six@1.12:", when="@0.5.3:")

    # imported at lvis/lvis.py:15

    def patch(self):
        os.rename(
            join_path(self.stage.source_path, "lvis.egg-info", "requires.txt"),
            join_path(self.stage.source_path, "requirements.txt"),
        )
