from spack_repo.builtin_mock.build_systems.makefile import MakefilePackage

from spack.package import *


class DummyMakefileBuildTestLog(MakefilePackage):
    """Mock Makefile-based package that simulates test and installcheck."""

    homepage = "http://example.com"
    url = "http://example.com/dummy-makefile-test-1.0.tar.gz"

    version("1.0", sha256="0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef")

    def build(self, spec, prefix):
        # Simulate build step (no-op)
        pass

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        touch(join_path(prefix.bin, "dummy"))

    def check(self):
        # Simulate `make test`
        print("=== DUMMY MAKE TEST ===")

    def installcheck(self):
        # Simulate `make installcheck`
        print("=== DUMMY INSTALLCHECK ===")
