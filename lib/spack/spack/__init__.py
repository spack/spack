# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#: PEP440 canonical <major>.<minor>.<micro>.<devN> string

import sys

__version__ = "0.22.0.dev0"
spack_version = __version__


def __try_int(v):
    try:
        return int(v)
    except ValueError:
        return v


#: (major, minor, micro, dev release) tuple
spack_version_info = tuple([__try_int(v) for v in __version__.split(".")])


#: Package modules are imported as spack.pkg.<repo-namespace>.<pkg-name>
#: This is a special namespace because it's generated dynamically from package repos.
ROOT_PYTHON_NAMESPACE = "spack.pkg"


# To import `spack.pkg`, `spack.repo` *must* be imported first. This class lazily
# imports `spack.repo` (in case it hasn't been imported already) when `spack.pkg` is
# imported, allowing `import spack.pkg...` to be the first thing you import.
class LazyRepoImporter:
    """Fake loader for ``sys.meta_path``.

    Ensures ``spack.repo`` is always imported before ``spack.pkg``.

    """

    def find_spec(self, fullname, python_path, target=None):
        if fullname.startswith(ROOT_PYTHON_NAMESPACE):
            sys.meta_path.remove(self)  # remove so we don't do this twice
            import spack.repo  # noqa: F401
        return None

    def compute_loader(self, fullname):
        return None


# ensure our LazyRepoImporter is the first thing on the PATH. We could just import
# `spack.repo` here, but this allows us to only load it when needed.
sys.meta_path.insert(0, LazyRepoImporter())


__all__ = ["spack_version_info", "spack_version"]
