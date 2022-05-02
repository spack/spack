from spack.pkg.builtin.py_shapely import PyShapely as BuiltinPyShapely


class PyShapely(BuiltinPyShapely):
    __doc__ = BuiltinPyShapely.__doc__

    setup_run_environment = BuiltinPyShapely.setup_build_environment
