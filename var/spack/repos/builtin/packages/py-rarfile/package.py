# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRarfile(PythonPackage):
    """RAR archive reader for Python."""

    homepage = "https://github.com/markokr/rarfile"
    pypi = "rarfile/rarfile-4.0.tar.gz"

    license("ISC")

    version(
        "4.1",
        sha256="17d7554c93c776ceae677e9d927051267d4c5eba38bf64b9cc89a415d9a5f901",
        url="https://pypi.org/packages/75/34/f06b7de74bcea328d8d7a950aad099c1100578cc3960ffc5a00d30ab511c/rarfile-4.1-py3-none-any.whl",
    )
    version(
        "4.0",
        sha256="1094869119012f95c31a6f22cc3a9edbdca61861b805241116adbe2d737b68f8",
        url="https://pypi.org/packages/95/f4/c92fab227c7457e3b76a4096ccb655ded9deac869849cb03afbe55dfdc1e/rarfile-4.0-py3-none-any.whl",
    )
