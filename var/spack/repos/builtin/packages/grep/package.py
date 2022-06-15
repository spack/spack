# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Grep(AutotoolsPackage):
    """Grep searches one or more input files for lines containing a match to
    a specified pattern"""

    homepage = "https://www.gnu.org/software/grep/"
    url      = "https://ftp.gnu.org/gnu/grep/grep-3.3.tar.xz"

    version('3.7', sha256='5c10da312460aec721984d5d83246d24520ec438dd48d7ab5a05dbc0d6d6823c')
    version('3.3', sha256='b960541c499619efd6afe1fa795402e4733c8e11ebf9fafccc0bb4bccdc5b514')

    build_directory = 'spack-build'
