# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re
from typing import Optional, Tuple

import llnl.util.filesystem as fs
import llnl.util.lang as lang
import llnl.util.tty as tty
import spack.deptypes as dt
from llnl.util.filesystem import mkdirp

from spack.dependency import Dependency
from spack.directives import extends
from spack.spec import Spec

from .generic import GenericBuilder, Package


class RBuilder(GenericBuilder):
    """The R builder provides a single phase that can be overridden:

        1. :py:meth:`~.RBuilder.install`

    It has sensible defaults, and for many packages the only thing
    necessary will be to add dependencies.
    """

    #: Names associated with package methods in the old build-system format
    legacy_methods: Tuple[str, ...] = (
        "configure_args",
        "configure_vars",
    ) + GenericBuilder.legacy_methods

    def configure_args(self):
        """Arguments to pass to install via ``--configure-args``."""
        return []

    def configure_vars(self):
        """Arguments to pass to install via ``--configure-vars``."""
        return []

    def install(self, pkg, spec, prefix):
        """Installs an R package."""
        mkdirp(pkg.module.r_lib_dir)

        try:
            # TODO: use a more sustainable dcf parser
            import pycran

            # Read DESCRIPTION file with dependency information
            # https://r-pkgs.org/description.html
            r_deps = []
            with open(fs.join_path(self.stage.source_path, 'DESCRIPTION')) as file:
                for desc in pycran.parse(file.read()):
                    if "Imports" in desc:
                        r_deps.extend([d.strip() for d in desc["Imports"].split(",")])
                    if "Depends" in desc:
                        r_deps.extend([d.strip() for d in desc["Depends"].split(",")])

            # Convert to spack dependencies format for comparison
            deps = {}
            for r_dep in r_deps:
                p = re.search(r"^[\w_-]+", r_dep)  # first word, incl. underscore or dash
                v = re.search("(?<=[(]).*(?=[)])", r_dep)  # everything between parentheses
                # require valid package
                assert p, f"Unable to find package name in {r_dep}"
                r_spec = f"r-{p[0].strip().lower()}" if p[0].lower() != "r" else "r"
                # allow minimum or pinned versions
                if v:
                    v = re.sub(r">=\s([\d.-]+)", r"@\1:", v[0])  # >=
                    v = re.sub(r"==\s([\d.-]+)", r"@\1", v)  # ==
                    deps[r_spec] = Dependency(pkg, Spec(r_spec + v), dt.BUILD | dt.RUN)
                else:
                    deps[r_spec] = Dependency(pkg, Spec(r_spec), dt.BUILD | dt.RUN)

            # Retrieve dependencies for current spack package and version
            spack_dependencies = []
            for when, dep in pkg.dependencies.items():
                if spec.satisfies(when):
                    spack_dependencies.append(dep)
            merged_dependencies = {}
            for dep in spack_dependencies:
                for n, d in dep.items():
                    if d in merged_dependencies:
                        merged_dependencies[n].merge(d)
                    else:
                        merged_dependencies[n] = d

            # For each R dependency, ensure Spack dependency is at least as strong
            for dep in sorted(deps.keys()):
                if dep in merged_dependencies:
                    if not merged_dependencies[dep].spec.satisfies(deps[dep].spec):
                        tty.debug(f'    depends_on("{deps[dep].spec}", when="@{pkg.version}:", type=("build", "run"))')
                else:
                    tty.debug(f'    depends_on("{deps[dep].spec}", when="@{pkg.version}:", type=("build", "run"))')

        except ImportError:
            tty.debug("R package dependency verification requires pycran")
            pass

        config_args = self.configure_args()
        config_vars = self.configure_vars()

        args = ["--vanilla", "CMD", "INSTALL"]

        if config_args:
            args.append(f"--configure-args={' '.join(config_args)}")

        if config_vars:
            args.append(f"--configure-vars={' '.join(config_vars)}")

        args.extend([f"--library={pkg.module.r_lib_dir}", self.stage.source_path])

        pkg.module.R(*args)


class RPackage(Package):
    """Specialized class for packages that are built using R.

    For more information on the R build system, see:
    https://stat.ethz.ch/R-manual/R-devel/library/utils/html/INSTALL.html
    """

    # package attributes that can be expanded to set the homepage, url,
    # list_url, and git values
    # For CRAN packages
    cran: Optional[str] = None

    # For Bioconductor packages
    bioc: Optional[str] = None

    GenericBuilder = RBuilder

    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = "RPackage"

    extends("r")

    @lang.classproperty
    def homepage(cls):
        if cls.cran:
            return f"https://cloud.r-project.org/package={cls.cran}"
        elif cls.bioc:
            return f"https://bioconductor.org/packages/{cls.bioc}"

    @lang.classproperty
    def url(cls):
        if cls.cran:
            return f"https://cloud.r-project.org/src/contrib/{cls.cran}_{str(list(cls.versions)[0])}.tar.gz"

    @lang.classproperty
    def list_url(cls):
        if cls.cran:
            return f"https://cloud.r-project.org/src/contrib/Archive/{cls.cran}/"

    @property
    def git(self):
        if self.bioc:
            return f"https://git.bioconductor.org/packages/{self.bioc}"
