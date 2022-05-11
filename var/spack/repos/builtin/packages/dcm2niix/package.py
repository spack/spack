# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Dcm2niix(CMakePackage):
    """DICOM to NIfTI converter"""

    homepage = "https://github.com/rordenlab/dcm2niix"
    url      = "https://github.com/rordenlab/dcm2niix/archive/refs/tags/v1.0.20210317.tar.gz"

    version('1.0.20210317', sha256='42fb22458ebfe44036c3d6145dacc6c1dc577ebbb067bedc190ed06f546ee05a')
