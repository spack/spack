# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


def _allowed_values(x):
    return x in {"make", "ninja", "other"}


class VariantFunctionValidator(Package):
    """This package has a variant with values defined by a function validator."""

    homepage = "https://www.example.org"
    url = "https://example.org/files/v3.4/cmake-3.4.3.tar.gz"

    version("1.0", md5="4cb3ff35b2472aae70f542116d616e63")

    variant("generator", default="make", values=_allowed_values, description="?")

    # Create a situation where, if the penalty for the variant defined by a function
    # is not taken into account, then we'll select the non-default value
    depends_on("adios2")
    conflicts("adios2+bzip2", when="generator=make")
    conflicts("adios2~bzip2", when="generator=ninja")
