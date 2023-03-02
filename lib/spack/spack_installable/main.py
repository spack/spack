import os
import sys
from os.path import dirname as dn


def main(argv=None):
    # Find spack's location and its prefix.
    this_file = os.path.realpath(os.path.expanduser(__file__))
    spack_prefix = dn(dn(dn(dn(this_file))))

    # Allow spack libs to be imported in our scripts
    spack_lib_path = os.path.join(spack_prefix, "lib", "spack")
    sys.path.insert(0, spack_lib_path)

    # Add external libs
    spack_external_libs = os.path.join(spack_lib_path, "external")

    if sys.version_info[:2] <= (2, 7):
        sys.path.insert(0, os.path.join(spack_external_libs, "py2"))

    sys.path.insert(0, spack_external_libs)
    # Here we delete ruamel.yaml in case it has been already imported from site
    # (see #9206 for a broader description of the issue).
    #
    # Briefly: ruamel.yaml produces a .pth file when installed with pip that
    # makes the site installed package the preferred one, even though sys.path
    # is modified to point to another version of ruamel.yaml.
    if "ruamel.yaml" in sys.modules:
        del sys.modules["ruamel.yaml"]

    if "ruamel" in sys.modules:
        del sys.modules["ruamel"]

    # The following code is here to avoid failures when updating
    # the develop version, due to spurious argparse.pyc files remaining
    # in the libs/spack/external directory, see:
    # https://github.com/spack/spack/pull/25376
    # TODO: Remove in v0.18.0 or later
    try:
        import argparse  # noqa: F401
    except ImportError:
        argparse_pyc = os.path.join(spack_external_libs, "argparse.pyc")
        if not os.path.exists(argparse_pyc):
            raise
        try:
            os.remove(argparse_pyc)
            import argparse  # noqa: F401
        except Exception:
            msg = (
                "The file\n\n\t{0}\n\nis corrupted and cannot be deleted by Spack. "
                "Either delete it manually or ask some administrator to "
                "delete it for you."
            )
            print(msg.format(argparse_pyc))
            sys.exit(1)

    import spack.main  # noqa: E402

    sys.exit(spack.main.main(argv))
