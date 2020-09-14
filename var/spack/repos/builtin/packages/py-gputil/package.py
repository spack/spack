# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGputil(PythonPackage):
    """GPUtil is a Python module for getting the GPU status from NVIDA GPUs
    using nvidia-smi."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/anderskm/gputil"
    url      = "https://github.com/anderskm/gputil/archive/v1.4.0.zip"

    version('1.4.0', sha256='6c157fba2ab6bfbf9ce7e8eedb4c38685ef01a1b484043320a2861822e905a37')
    version('1.3.0', sha256='098be020168d677c27f9c9c31585e0f5081584514915b6bb5861843c51acc48c')
    version('1.2.3', sha256='93db313dcbcd9c989874ad9191848e63295f3b159cf90a5d5abcd86b965a326e')
    version('1.2.2', sha256='43badf6018bbdc4d849233b4c9fa8bd1c518a549eea4af2db29eeea0aee645aa')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
