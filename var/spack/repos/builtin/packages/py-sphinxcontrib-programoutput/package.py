# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySphinxcontribProgramoutput(PythonPackage):
    """A Sphinx extension to literally insert the output of arbitrary commands
    into documents, helping you to keep your command examples up to date."""

    homepage = "https://sphinxcontrib-programoutput.readthedocs.org/"
    url      = "https://pypi.io/packages/source/s/sphinxcontrib-programoutput/sphinxcontrib-programoutput-0.10.tar.gz"

    # FIXME: These import tests don't work for some reason
    # import_modules = ['sphinxcontrib', 'sphinxcontrib.programoutput']

    version('0.10', sha256='fdee94fcebb0d8fddfccac5c4fa560f6177d5340c4349ee447c890bea8857094')

    depends_on('py-setuptools', type='build')
    depends_on('py-sphinx@1.3.5:', type=('build', 'run'))
