# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyResultsfile(PythonPackage):
    """Python module to read output files of quantum chemistry programs"""

    homepage = "https://gitlab.com/scemama/resultsFile"
    url      = "https://gitlab.com/scemama/resultsFile/-/archive/v1.0/resultsFile-v1.0.tar.gz"

    maintainers = ['scemama']

    version('1.0', sha256='e029054b2727131da9684fa2ec9fb8b6a3225dc7f648216a9390267b2d5d60c3')

    depends_on('python@2.7:2.8.999', type=('build','run'))

    # It depends on py-setuptools only at build time, but I get the following error:
    #   error: option --single-version-externally-managed not recognized
    # So I fixed it by setting the type to 'run' here, which is a bit dirty.
    depends_on('py-setuptools', type='run')
