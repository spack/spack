# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultiecho(PythonPackage):
    """Combine multi-echoes from a multi-echo fMRI acquisition."""

    homepage = "https://github.com/Donders-Institute/multiecho"
    pypi = "multiecho/multiecho-0.28.tar.gz"

    license("MIT")

    version(
        "0.28",
        sha256="4e8f9507616053133bab97535ea4efa5a9b78e9c046280f684fd50cdd72160bb",
        url="https://pypi.org/packages/10/6e/2d42e6ebc5fcca1a4038342b64836ce22bd8f785a054b8d5365c0d823fb3/multiecho-0.28-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-coloredlogs")
        depends_on("py-nibabel")
        depends_on("py-numpy")
