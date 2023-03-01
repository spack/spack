from spack.pkg.builtin.darshan_runtime import DarshanRuntime as BuiltinDarshanRuntime


class DarshanRuntime(BuiltinDarshanRuntime):
    __doc__ = BuiltinDarshanRuntime.__doc__

    def setup_run_environment(self, env):
        # The upstream recipe uses the $HOME environment variable, which leads to
        # fixing the BBP CI user home directory in the module specification. With
        # this change, the home directory will be interpreted during module load.
        env.set("DARSHAN_LOG_DIR_PATH", "~")
