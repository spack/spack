# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# Package automatically generated using 'pip2spack' converter


class PyLhsmdu(PythonPackage):
    """Latin Hypercube Sampling with Multi-Dimensional Uniformity (LHS-MDU)
    from Deutsch and Deutsch, Latin hypercube sampling with multidimensional
    uniformity."""

    homepage = "http://github.com/sahilm89/lhsmdu"
    url      = "https://pypi.io/packages/source/l/lhsmdu/lhsmdu-1.1.tar.gz"

    version('1.1', sha256='4bc1df6b9cdd27bae0bff75cf1693f455ba32e4fa87ca9a932f60696607fe712')
    version('0.1', sha256='ef462054b354cd20b10c6d80876c8fdb552a8d2e23eaf74179dc91956d68d32a')

    # depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
