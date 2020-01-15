# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySpdlog(PythonPackage):
    """The py-spdlog package provides a Python wrapper
    to the C++ spdlog library."""

    homepage = 'https://github.com/bodgergely/spdlog-python'
    url = 'https://github.com/bodgergely/spdlog-python/archive/v2.0.0.tar.gz'
    git = 'https://github.com/bodgergely/spdlog-python.git'

    # NOTE: We cannot use the archives of releases because they are missing
    # the content of their spdlog directory, and they are not able to find
    # an existing installation of spdlog. Hence the bellow versions are using
    # the git repository and pulling the spdlog directory using a submodule.

    # NOTE: Righ now py-spdlog works with a git submodule containing a copy
    # of spdlog. Ideally we would want to install spdlog ourselves and make
    # this package depend on it. There is an issue for that on the py-spdlog
    # github repository: https://github.com/bodgergely/spdlog-python/issues/19

    version('master', branch='master', submodules=True)
    version('2.0.0', commit='41a5caa57d27dba01a2015bb90a6174309f50e0e',
            submodules=True)
    version('1.0.5', commit='92ce5f621656aed4daa57902334da68e609b3d42',
            submodules=True)

    depends_on('py-pybind11@2.2:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pytest-runner', type='build')
    depends_on('py-pytest', type='test')
