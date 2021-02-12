# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyTraits(PythonPackage):
    """Explicitly typed attributes for Python."""

    homepage = "https://docs.enthought.com/traits"
    pypi = "traits/traits-6.0.0.tar.gz"

    version('6.2.0', sha256='16fa1518b0778fd53bf0547e6a562b1787bf68c8f6b7995a13bd1902529fdb0c')
    version('6.1.1', sha256='807da52ee0d4fc1241c8f8a04d274a28d4b23d3a5f942152497d19405482d04f')
    version('6.1.0', sha256='97fca523374ae85e3d8fd78af9a9f488aee5e88e8b842e1cfd6d637a6f310fac')
    version('6.0.0', sha256='dbcd70166feca434130a1193284d5819ca72ffbc8dbce8deeecc0cebb41a3bfb')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
