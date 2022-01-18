from spack.pkg.builtin.py_rtree import PyRtree as BuiltinPyRtree


class PyRtree(BuiltinPyRtree):
    __doc__ = BuiltinPyRtree.__doc__

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_run_environment(env)
