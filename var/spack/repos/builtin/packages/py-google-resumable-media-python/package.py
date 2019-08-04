# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT
#
# ----------------------------------------------------------------------------
#
#     spack install py-google-resumable-media-python
#
# You can edit this file again by typing:
#
#     spack edit py-google-resumable-media-python
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------


from spack import *


class PyGoogleResumableMediaPython(PythonPackage):
    """Utilities for Google Media Downloads and Resumable Uploads."""

    homepage = "https://github.com/GoogleCloudPlatform/google-resumable-media-python"
    url      = "https://github.com/GoogleCloudPlatform/google-resumable-media-python/archive/0.3.1.tar.gz"

    version('0.3.2', 'c5407ab051844272eadaf42ea40516bc')

    # Build dependencies
    depends_on('py-setuptools', type='build')
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))

    


