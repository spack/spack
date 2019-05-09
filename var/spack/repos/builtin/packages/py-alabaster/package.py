# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAlabaster(PythonPackage):
    """Alabaster is a visually (c)lean, responsive, configurable theme
    for the Sphinx documentation system."""

    homepage = "https://alabaster.readthedocs.io/"
    url      = "https://pypi.io/packages/source/a/alabaster/alabaster-0.7.10.tar.gz"

    import_modules = ['alabaster']

    version('0.7.12', sha256='a661d72d58e6ea8a57f7a86e37d86716863ee5e92788398526d58b26a4e4dc02')
    version('0.7.10', '7934dccf38801faa105f6e7b4784f493')
    version('0.7.9',  'b29646a8bbe7aa52830375b7d17b5d7a')

    depends_on('py-setuptools', type='build')
