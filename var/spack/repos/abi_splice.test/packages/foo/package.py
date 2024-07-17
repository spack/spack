from spack.package import *


class Foo(Package):
    homepage = "https://www.example.com"
    has_code = False
    variant("compat", default=True)
    version("1.0.0")
    version("1.0.1")
    can_splice("foo@1.0.0 +compat", when="@1.0.1 +compat")
    version("1.0.2")
    can_splice("foo@1.0.0:1.0.1", when="@1.0.2 +compat")
    version("2.0.0")

    def install(self, spec, prefix):
        touch(prefix.foo)
