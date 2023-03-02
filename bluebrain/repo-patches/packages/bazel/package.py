from spack.package import *
from spack.pkg.builtin.bazel import Bazel as BuiltinBazel


class Bazel(BuiltinBazel):
    __doc__ = BuiltinBazel.__doc__
    patch("bazel-no-worker.patch", when="@5.1.1:")

    # Newer versions of openjdk break this build -
    # newer versions of bazel have not been tested
    # It should require java rather than openjdk, but since we use openjdk
    # and need a specific version...
    depends_on("openjdk@11.0.14.1", when="@5.1.1", type=("build", "run"))
