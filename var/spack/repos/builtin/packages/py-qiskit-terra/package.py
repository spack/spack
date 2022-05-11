# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.util.package import *


class PyQiskitTerra(PythonPackage):
    """Qiskit is an open-source SDK for working with quantum computers
    at the level of extended quantum circuits, operators, and
    algorithms."""

    homepage = "https://github.com/Qiskit/qiskit-terra"
    pypi = "qiskit-terra/qiskit-terra-0.18.3.tar.gz"

    version('0.18.3', sha256='8737c8f1f4c6f29ec2fb02d73023f4854a396c33f78f4629a861a3e48fc789cc')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-cython@0.27.1:', type='build')

    depends_on('py-contextvars@2.4:', when='^python@:3.6', type=('build', 'run'))
    depends_on('py-jsonschema@2.6:', type=('build', 'run'))
    depends_on('py-retworkx@0.9.0:', type=('build', 'run'))
    depends_on('py-numpy@1.17:', type=('build', 'run'))
    depends_on('py-scipy@1.4:', type=('build', 'run'))
    depends_on('py-ply@3.10:', type=('build', 'run'))
    depends_on('py-psutil@5:', type=('build', 'run'))
    depends_on('py-sympy@1.3:', type=('build', 'run'))
    depends_on('py-dill@0.3:', type=('build', 'run'))
    depends_on('py-fastjsonschema@2.10:', type=('build', 'run'))
    depends_on('py-python-constraint@1.4:', type=('build', 'run'))
    depends_on('py-python-dateutil@2.8.0:', type=('build', 'run'))
    depends_on('py-symengine@0.7:', type=('build', 'run'))
    depends_on('py-tweedledum@1.1:1', type=('build', 'run'))
