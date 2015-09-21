from spack import *

class PyPythonDaemon(Package):
    """Library to implement a well-behaved Unix daemon process.

       This library implements the well-behaved daemon specification of
       PEP Standard daemon process.

       A well-behaved Unix daemon process is tricky to get right, but the
       required steps are much the same for every daemon program. A
       DaemonContext instance holds the behaviour and configured process
       environment for the program; use the instance as a context manager
       to enter a daemon state.
    """
    homepage = "https://pypi.python.org/pypi/python-daemon/"
    url      = "https://pypi.python.org/packages/source/p/python-daemon/python-daemon-2.0.5.tar.gz"

    version('2.0.5', '73e7f49f525c51fa4a995aea4d80de41')

    extends("python")
    depends_on("py-setuptools")
    depends_on("py-lockfile")

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)

