from spack.package import *
from spack.pkg.builtin.py_sentry_sdk import PySentrySdk as BuiltinPySentrySdk


class PySentrySdk(BuiltinPySentrySdk):
    __doc__ = BuiltinPySentrySdk.__doc__

    version("1.15.0", sha256="69ecbb2e1ff4db02a06c4f20f6f69cb5dfe3ebfbc06d023e40d77cf78e9c37e7")
