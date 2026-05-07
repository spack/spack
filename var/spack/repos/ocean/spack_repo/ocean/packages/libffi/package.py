from spack_repo.builtin.packages.libffi.package import Libffi as BuiltinLibffi


class Libffi(BuiltinLibffi):
    """Ocean override for Darwin x86_64 builds on Apple Silicon."""

    def configure_args(self):
        args = super().configure_args()
        if self.spec.satisfies("platform=darwin target=x86_64:"):
            args.extend(["--build=x86_64-apple-darwin", "--host=x86_64-apple-darwin"])
        return args
