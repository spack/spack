# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPyutilib(PythonPackage):
    """The PyUtilib project supports a collection of Python utilities,
    including a well-developed component architecture and extensions to the
    PyUnit testing framework. PyUtilib has been developed to support several
    Python-centric projects, especially Pyomo. PyUtilib is available under the
    BSD License."""

    homepage = "https://github.com/PyUtilib/pyutilib"
    url      = "https://github.com/PyUtilib/pyutilib/archive/5.5.1.tar.gz"

    version('5.6.2', '60c6ea5083e512211984347ffeca19d2')
    version('5.6.1', 'ddc7e896304b6fabe4d21eb5fdec386e')
    version('5.6',   '5bfcdbf118264f1a1b8c6cac9dea8bca')
    version('5.5.1', 'c4990cbced152d879812d109aaa857ff')
    version('5.5',   '7940563bf951332cf836f418d67b2134')
    version('5.4.1', 'b34b5798757e4ab73868b7655c5c8f8a')
    version('5.4',   '9410e5a76885412310b03074d2f97e55')
    version('5.3.5', '85e41e65f24f6711261229bcde6eb825')
    version('5.3.4', '4fe1a8387c027f64b62ca99424275368')
    version('5.3.3', '27a713ca8d49714244646e1ce38778b9')

    depends_on('py-nose', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
