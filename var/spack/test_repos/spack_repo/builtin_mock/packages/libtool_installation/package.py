# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *
from ..libtool_deletion.package import AutotoolsBuilder as BuilderBase
from ..libtool_deletion.package import LibtoolDeletion


class LibtoolInstallation(LibtoolDeletion, AutotoolsPackage):
    """Mock AutotoolsPackage to check proper installation of libtool archives."""


class AutotoolsBuilder(BuilderBase):
    install_libtool_archives = True
