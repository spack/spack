from spack.package import *
from spack.pkg.builtin.arm_forge import ArmForge as BuiltinArmForge


class ArmForge(BuiltinArmForge):
    __doc__ = BuiltinArmForge.__doc__

    def setup_run_environment(self, env):
        # ENV variables required to avoid licensing and SLURM issues on BB5
        env.unset("HTTP_PROXY")
        env.unset("HTTPS_PROXY")
        env.unset("http_proxy")
        env.unset("https_proxy")
        env.set("ALLINEA_USE_SSH_STARTUP", "1")
