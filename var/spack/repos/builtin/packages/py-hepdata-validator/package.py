# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHepdataValidator(PythonPackage):
    """Validation schema and code for HEPdata submissions."""

    homepage = "https://github.com/hepdata/hepdata-validator"
    url = "https://pypi.io/packages/source/h/hepdata_validator/hepdata_validator-0.1.16.tar.gz"

    version('0.1.16', '62e80db7425a4a48050af29e05295e0d')
    version('0.1.15', 'e29aa75780b9963997e79f572ca0209f')
    version('0.1.14', '386a2440f23fda7d877764d120bf61fb')
    version('0.1.8', '5bf388a507a857afbe0deba0857125c7')

    depends_on('py-setuptools', type='build')
    depends_on('py-jsonschema', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
