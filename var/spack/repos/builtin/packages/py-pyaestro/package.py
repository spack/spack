# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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
#     spack install py-pyaestro
#
# You can edit this file again by typing:
#
#     spack edit py-pyaestro
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyPyaestro(PythonPackage):
    """A collection of data classes, data structures, and other utility classes
    that are aimed for use in workflow """

    homepage = "https://github.com/FrankD412/pyaestro"
    pypi = "pyaestro/pyaestro-0.0.1a2.tar.gz"
    git      = "https://github.com/FrankD412/pyaestro"

    maintainers = ['FrankD412']

    # git branches
    version('main',  branch='main')
    version('0.0.1a2', sha256='1f6a5068ff8dd9fe4838aba43850e51a5b622f379819ae62103617bf9c8aaa31', preferred=True)

    depends_on('python@3.6:',    type=('build', 'run'))
    depends_on('py-setuptools',  type='build')
    depends_on('py-coloredlogs', type=('build', 'run'))
    depends_on('py-psutil',      type=('build', 'run'))

