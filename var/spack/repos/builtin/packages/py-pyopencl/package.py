# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPyopencl(PythonPackage):
    """Python wrapper for OpenCL."""

    homepage = "https://documen.tician.de/pyopencl/"
    url      = "https://files.pythonhosted.org/packages/75/ee/b8c71784fe0eb6997b5daf6065136ea7a8e64118a079917b0eeb70ed0d00/pyopencl-2020.2.2.tar.gz"

    maintainers = ['matthiasdiener']

    version('2020.2.2', sha256='31fcc79fb6862998e98d91a624c0bd4f0ab4c5d418d199912d4d312c64e437ec')

    depends_on('opencl')
    depends_on('ocl-icd')
    depends_on('py-mako')
    depends_on('py-pybind11')
    depends_on('py-numpy')

    @run_before('build')
    def prepare(self):
        cl_prefix = self.spec['ocl-icd'].prefix
        python('configure.py', '--cl-inc-dir=' + cl_prefix.include, '--cl-lib-dir=' + cl_prefix.lib)
	# python('configure.py', '--cl-inc-dir={0}/include'.format(cl_prefix), '--cl-lib-dir={0}/lib'.format(cl_prefix))

