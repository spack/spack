# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyAzureMultiapiStorage(PythonPackage):
    """Microsoft Azure Storage Client Library for Python with multi API
    version support."""

    homepage = "https://github.com/Azure/azure-multiapi-storage-python"
    pypi = "azure-multiapi-storage/azure-multiapi-storage-0.3.5.tar.gz"

    version('0.5.2', sha256='ee9d7589bb61388b550766cf13571829af9ee86ebb75b068232fcec36a39c027')
    version('0.5.1', sha256='31c791b53a3ce179eed19d6a139738df2b1492fb1af5b94a6e9c140b9e8546d7')
    version('0.5.0', sha256='75e0048b3656917b746c66b42ea408983002ed74ddd112681cffdf522a8b70cc')
    version('0.4.1', sha256='a33bc313d67ce1bd67a2f59a333bd4e6d599caeddc2ef9714f7250cfb1faeb40')
    version('0.3.7', sha256='de137ed313673014e8f740e99a9865ffccc5d2ad74e2f8c152428c73b4684411')
    version('0.3.6', sha256='e2e0c365d425b4eb075e19d03bba21398b40820c202ae223210bf331cd92fc3f')
    version('0.3.5', sha256='71c238c785786a159b3ffd587a5e7fa1d9a517b66b592ae277fed73a9fbfa2b0')

    depends_on('py-setuptools', type='build')
    depends_on('py-azure-common', type=('build', 'run'))
    depends_on('py-cryptography', type=('build', 'run'))
    depends_on('py-python-dateutil', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-azure-core', type=('build', 'run'))
    depends_on('py-futures', when='^python@:2', type=('build', 'run'))
    depends_on('py-azure-nspkg', when='^python@:2', type=('build', 'run'))
