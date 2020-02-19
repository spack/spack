# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIrpf90(PythonPackage):
    """IRPF90 is a Fortran90 preprocessor written in Python for programming
    using the Implicit Reference to Parameters (IRP) method. It simplifies the
    development of large fortran codes in the field of scientific high
    performance computing."""

    homepage = "http://irpf90.ups-tlse.fr"
    url = "https://files.pythonhosted.org/packages/f7/46/5b41a2a45bf3da8746c864ac60321b92b77dd707ed16264e6f9501cc2bf0/irpf90-1.7.7.tar.gz"

    maintainers = ['scemama']

    version('1.7.7', "b63cf7871580904d54c6ca0fcc2c82c92e674ebf")

    depends_on('python@2.7.0:2.8.999', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
