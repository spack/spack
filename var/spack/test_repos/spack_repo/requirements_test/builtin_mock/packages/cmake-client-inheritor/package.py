# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *  # noqa: F401

from ..cmake_client.package import CmakeClient


class CmakeClientInheritor(CmakeClient):
    """A dumy package that inherits from one using cmake."""
