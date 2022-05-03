from spack import *
from spack.pkg.builtin.mariadb_c_client import MariadbCClient as BuiltinMariadbCClient


class MariadbCClient(BuiltinMariadbCClient):
    __doc__ = BuiltinMariadbCClient.__doc__

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "lib/mariadb"))
