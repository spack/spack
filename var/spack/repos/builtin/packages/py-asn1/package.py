# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-asn1
#
# You can edit this file again by typing:
#
#     spack edit py-asn1
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyAsn1(PythonPackage):
    """Python-ASN1 is a simple ASN.1 encoder and decoder for Python 2.6+
    and 3.3+.
    """

    homepage = "https://github.com/andrivet/python-asn1"
    url      = "https://pypi.io/packages/source/a/asn1/asn1-2.2.0.tar.gz"

    version('2.2.0', sha256='5a0cc798ae21313260a53fda7d76b45a86d72a93c58eb218b2713765ce8bf3c7')

    depends_on('py-setuptools', type='build')
    depends_on('py-future@0.17.1', type=('build', 'run'))
    depends_on('py-enum34@1.1.6', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
