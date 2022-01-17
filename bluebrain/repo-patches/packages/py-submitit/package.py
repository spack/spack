from spack import *
from spack.pkg.builtin.py_submitit import PySubmitit as BuiltinPySubmitit


class PySubmitit(BuiltinPySubmitit):
    __doc__ = BuiltinPySubmitit.__doc__

    git      = "https://github.com/facebookincubator/submitit.git"

    # specify the commit because submitit-1.4.0.tar.gz is broken on pypi
    version('1.4.0', commit='d85b7abf73d094dd11c4a89343afa88f8908b316')
