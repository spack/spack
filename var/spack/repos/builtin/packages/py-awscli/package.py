##############################################################################
# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAwscli(PythonPackage):
    """This package provides a unified command line interface to
       Amazon Web Services"""

    homepage = "https://pypi.org/project/awscli/"
    url      = "https://pypi.io/packages/source/a/awscli/awscli-1.16.111.tar.gz"

    version('1.16.111', sha256='63c7900e65a76a1574e1d6e3aaa37c98403339a552428b47559d4e05081f8e4b')

    depends_on('py-setuptools')
    depends_on('py-docutils@0.10:')
    depends_on('py-nose', type=('build', 'test'))
    depends_on('py-tox@2.3.1:2.999', type='test')
    depends_on('py-colorama@0.2.5:0.3.9', type=('build', 'run'))
    depends_on('py-mock@1.3.0:', type=('build', 'run'))
    depends_on('py-rsa@3.1.2:3.5.0', type=('build', 'run'))
    depends_on('py-wheel@0.24.0:', type=('build', 'run'))
    depends_on('py-pyyaml@3.10:3.13', type=('build', 'run'))
    depends_on('py-argparse', when='^python@2.6:2.6.99', type=('build', 'run'))
    # I suspect there will need to be some version dependencies for these,
    # too, but they are not explicit. There is an ominous message about tandem
    # development in the requirements.txt
    depends_on('py-jmespath', type=('build', 'run'))
    depends_on('py-s3transfer', type=('build', 'run'))
    depends_on('py-botocore', type=('build', 'run'))
