from spack import *
from spack.pkg.builtin.arm_forge import ArmForge as BuiltinArmForge


class ArmForge(BuiltinArmForge):
    __doc__ = BuiltinArmForge.__doc__

    version(
        "21.1.2-Linux-x86_64",
        sha256="ebc99fa3461d2cd968e4d304c11b70cc8d9c5a2acd68681cec2067c128255cd5",
        url="https://content.allinea.com/downloads/arm-forge-21.1.2-linux-x86_64.tar",
    )

    version(
        "20.2.0-Redhat-7.0-x86_64",
        sha256="26592a77c42f970f724f15b70cc5ce6af1078fd0ef9243a37c3215916cfa7cf4",
        url="https://content.allinea.com/downloads/arm-forge-20.2-Redhat-7.0-x86_64.tar",
    )
