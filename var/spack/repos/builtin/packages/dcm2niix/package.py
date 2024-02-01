# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Dcm2niix(CMakePackage):
    """DICOM to NIfTI converter"""

    homepage = "https://github.com/rordenlab/dcm2niix"
    url = "https://github.com/rordenlab/dcm2niix/archive/refs/tags/v1.0.20220720.tar.gz"

    version(
        "1.0.20220720", sha256="a095545d6d70c5ce2efd90dcd58aebe536f135410c12165a9f231532ddab8991"
    )
    version(
        "1.0.20210317", sha256="42fb22458ebfe44036c3d6145dacc6c1dc577ebbb067bedc190ed06f546ee05a"
    )
