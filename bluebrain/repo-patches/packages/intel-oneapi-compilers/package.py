from spack.package import *
from spack.pkg.builtin.intel_oneapi_compilers import (
    IntelOneapiCompilers as BuiltinIntelOneapiCompilers,
)


class IntelOneapiCompilers(BuiltinIntelOneapiCompilers):
    __doc__ = BuiltinIntelOneapiCompilers.__doc__
    # Otherwise module load intel-oneapi-compilers leaves us with a prehistoric binutils
    depends_on("binutils", type="run")
