# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyCarputils(PythonPackage):
    """The carputils framework for running simulations with the openCARP software."""

    homepage = "https://www.opencarp.org"
    git      = "https://git.opencarp.org/openCARP/carputils.git"

    maintainers = ['MarieHouillon']

    version('master', branch='master')
    # Version to use with openCARP releases
    version('oc8.1', commit='a4210fcb0fe17226a1744ee9629f85b629decba3')
    version('oc7.0', commit='4c04db61744f2fb7665594d7c810699c5c55c77c')

    depends_on('git')

    depends_on('python@:3.8', type=('build', 'run'))
    depends_on('py-pip', type='build')
    depends_on('py-numpy@1.14.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-python-dateutil', type='run')
    depends_on('py-scipy@:1.5.4', type='run')
    depends_on('py-matplotlib@:3.3.3', type='run')
    depends_on('py-pandas@:1.1.4', type='run')
    depends_on('py-tables@3.6.1', type='run')
    depends_on('py-six@:1.14.0', type='run')
    depends_on('py-ruamel-yaml', type='run')
