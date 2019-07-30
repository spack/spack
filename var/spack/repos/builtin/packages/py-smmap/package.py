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
#     spack install py-smmap
#
# You can edit this file again by typing:
#
#     spack edit py-smmap
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PySmmap(PythonPackage):
    """smmap is a pure python implementation of a sliding memory map to help unifying memory mapped access on 32 and 64 bit systems and to help managing resources more efficiently.."""

    homepage = "https://smmap.readthedocs.io"
    url      = "https://github.com/gitpython-developers/smmap/archive/v2.0.5.tar.gz"

    version('2.1.1.dev1', sha256='ccf2b2a45831431dd389a0ca2a1861e0daeb676d57af28e19d75489f5bdbb9e6')

    depends_on('py-setuptools', type='build')

