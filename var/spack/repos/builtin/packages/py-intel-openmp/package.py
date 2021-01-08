# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIntelOpenmp(Package):
    """Intel OpenMP* Runtime Library x86_64 dynamic libraries
    for macOS*. Intel OpenMP* Runtime Library provides OpenMP
    API specification support in Intel C Compiler, Intel C++
    Compiler and Intel Fortran Compiler. It helps to improve
    performance by creating multithreaded software using shared
    memory and running on multi-core processor systems."""

    homepage = "https://pypi.org/project/intel-openmp/"
    url      = "https://files.pythonhosted.org/packages/e5/15/3a478d0075660e201cc69801b7f6681dff9c9070278c8de4aa388dea24a8/intel_openmp-2021.1.2-py2.py3-none-macosx_10_15_x86_64.whl"

    version('2021.1.2-py2.py3-none-manylinux1_x86_64',
            url='https://files.pythonhosted.org/packages/27/92/68c00e053c0e38fc5e7b0eb1a47a048ce499e12829aede84b400a4c38a96/intel_openmp-2021.1.2-py2.py3-none-manylinux1_x86_64.whl',
            sha256='8796797ecae99f39b27065e4a7f1f435e2ca08afba654ca57a77a2717f864dca',
            expand=False)

    depends_on('py-pip', type='build')

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
