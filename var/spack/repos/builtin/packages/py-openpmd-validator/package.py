# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenpmdValidator(PythonPackage):
    """Validator and Example Scripts for the openPMD markup.

    openPMD is an open standard for particle-mesh data files."""

    homepage = "https://www.openPMD.org"
    git = "https://github.com/openPMD/openPMD-validator.git"
    pypi = "openPMD-validator/openPMD-validator-1.1.0.3.tar.gz"

    maintainers("ax3l")

    license("ISC")

    version(
        "1.1.0.3",
        sha256="8f55d04acd135d0afa67b4224912b2a009e660c8bbc9e94c49b79554fd3e6192",
        url="https://pypi.org/packages/68/b0/7aa658cc495b058f49af93afe2db01170e3e4a80c3a3404bcbae4b63633a/openPMD_validator-1.1.0.3-py3-none-any.whl",
    )
    version(
        "1.1.0.2",
        sha256="754c0a8c3ae1a13079e5c535d50ab1074537fd2a29814193298c1c3c8cf2129c",
        url="https://pypi.org/packages/81/86/c939f7bd14de85a97ee658def8491e2430be366d49ec601ec0b7a30f3d72/openPMD_validator-1.1.0.2-py3-none-any.whl",
    )
    version(
        "1.1.0.1",
        sha256="473a9d61bdc919ca970cbf347dbbafe54f50c5da9e5d17b86fa31b5c1d4925dd",
        url="https://pypi.org/packages/08/28/9d63b538af46fb87772388828d4233a3461a458cd9e8e4feee0bb589d0b6/openPMD_validator-1.1.0.1-py3-none-any.whl",
    )
    version(
        "1.0.0.2",
        sha256="47098ed5b9ca6b9d54225f6af100f1386dec9c1b7ca3157dbd6a269124feed9c",
        url="https://pypi.org/packages/b6/d3/33607035ee595c2ed3341350b3c706734d8748d7a9f73f25f7607eba6d50/openPMD_validator-1.0.0.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-h5py")
        depends_on("py-numpy@1.6.1:")
        depends_on("py-python-dateutil@2.3:")
