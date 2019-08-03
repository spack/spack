# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT
#
# ----------------------------------------------------------------------------
#
#     spack install py-compute-job-recorder
#
# You can edit this file again by typing:
#
#     spack edit py-compute-job-recorder
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyComputeJobRecorder(PythonPackage):
    """A tool for recording a compute job progress when undertaking batch processing tasks."""

    homepage = "https://www.remotesensing.info/compute_job_recorder"
    url      = "https://bitbucket.org/petebunting/compute_job_recorder/downloads/ComputeJobRecorder-0.0.1.tar.gz"

    maintainers = ['petebunting']

    version('0.0.1', sha256='0347c8a51829b1f8bae2bcaf370dc4c78dfa2e6340ad2489e9e15aaa3981a165')

    depends_on('sqlite',        type=('build', 'run'))
    depends_on('py-sqlalchemy', type=('build', 'run'))
    

