# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.pkgkit import *


class PyTraits(PythonPackage):
    """Explicitly typed attributes for Python."""

    homepage = "https://docs.enthought.com/traits"
    pypi = "traits/traits-6.0.0.tar.gz"

    version('6.3.1', sha256='ebdd9b067a262045840a85e3ff34e1567ce4e9b6548c716cdcc82b5884ed9100')
    version('6.2.0', sha256='16fa1518b0778fd53bf0547e6a562b1787bf68c8f6b7995a13bd1902529fdb0c')
    version('6.0.0', sha256='dbcd70166feca434130a1193284d5819ca72ffbc8dbce8deeecc0cebb41a3bfb')

    depends_on('python@3.6:', type=('build', 'run'), when='@6.2.0:')
    depends_on('python@3.5:', type=('build', 'run'), when='@:6.1')
    depends_on('py-setuptools', type='build')
