from spack import *
from spack.pkg.builtin.py_python_daemon import PyPythonDaemon as BuiltinPyPythonDaemon


class PyPythonDaemon(BuiltinPyPythonDaemon):
    __doc__ = BuiltinPyPythonDaemon.__doc__

    depends_on("py-docutils", type=('build', 'run'))
