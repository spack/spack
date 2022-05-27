from spack import *
from spack.pkg.builtin.arm_forge import ArmForge as BuiltinArmForge


class ArmForge(BuiltinArmForge):
    __doc__ = BuiltinArmForge.__doc__

    version(
        "22.0.1-Linux-x86_64",
        sha256="8f8a61c159665d3de3bc5334ed97bdb4966bfbdb91b65d32d162d489eb2219ac",
        url="https://content.allinea.com/downloads/arm-forge-22.0.1-linux-x86_64.tar",
    )

    def setup_run_environment(self, env):
        # ENV variables required to avoid licensing and SLURM issues on BB5
        env.unset('HTTP_PROXY')
        env.unset('HTTPS_PROXY')
        env.unset('http_proxy')
        env.unset('https_proxy')
        env.set('ALLINEA_USE_SSH_STARTUP', "1")
