# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re
import subprocess
import sys
from distutils.version import StrictVersion
from typing import Dict, List, Set

import spack.compiler
import spack.operating_systems.windows_os
import spack.platforms
import spack.util.executable
from spack.compiler import Compiler
from spack.error import SpackError
from spack.version import Version

avail_fc_version: Set[str] = set()
fc_path: Dict[str, str] = dict()

fortran_mapping = {
    "2021.3.0": "19.29.30133",
    "2021.2.1": "19.28.29913",
    "2021.2.0": "19.28.29334",
    "2021.1.0": "19.28.29333",
}


def get_valid_fortran_pth(comp_ver):
    cl_ver = str(comp_ver).split("@")[1]
    sort_fn = lambda fc_ver: StrictVersion(fc_ver)
    sort_fc_ver = sorted(list(avail_fc_version), key=sort_fn)
    for ver in sort_fc_ver:
        if ver in fortran_mapping:
            if StrictVersion(cl_ver) <= StrictVersion(fortran_mapping[ver]):
                return fc_path[ver]
    return None


class Msvc(Compiler):
    # Subclasses use possible names of C compiler
    cc_names: List[str] = ["cl"]

    # Subclasses use possible names of C++ compiler
    cxx_names: List[str] = ["cl"]

    # Subclasses use possible names of Fortran 77 compiler
    f77_names: List[str] = ["ifx"]

    # Subclasses use possible names of Fortran 90 compiler
    fc_names: List[str] = ["ifx"]

    # Named wrapper links within build_env_path
    # Due to the challenges of supporting compiler wrappers
    # in Windows, we leave these blank, and dynamically compute
    # based on proper versions of MSVC from there
    # pending acceptance of #28117 for full support using
    # compiler wrappers
    link_paths = {"cc": "", "cxx": "", "f77": "", "fc": ""}

    #: Compiler argument that produces version information
    version_argument = ""

    # For getting ifx's version, call it with version_argument
    # and ignore the error code
    ignore_version_errors = [1]

    #: Regex used to extract version from compiler's output
    version_regex = r"([1-9][0-9]*\.[0-9]*\.[0-9]*)"

    # Initialize, deferring to base class but then adding the vcvarsallfile
    # file based on compiler executable path.

    def __init__(self, *args, **kwargs):
        new_pth = [pth if pth else get_valid_fortran_pth(args[0]) for pth in args[3]]
        args[3][:] = new_pth
        super(Msvc, self).__init__(*args, **kwargs)
        if os.getenv("ONEAPI_ROOT"):
            # If this found, it sets all the vars
            self.setvarsfile = os.path.join(os.getenv("ONEAPI_ROOT"), "setvars.bat")
        else:
            # To use the MSVC compilers, VCVARS must be invoked
            # VCVARS is located at a fixed location, referencable
            # idiomatically by the following relative path from the
            # compiler.
            # Spack first finds the compilers via VSWHERE
            # and stores their path, but their respective VCVARS
            # file must be invoked before useage.
            self.setvarsfile = os.path.abspath(os.path.join(self.cc, "../../../../../../.."))
            self.setvarsfile = os.path.join(self.setvarsfile, "Auxiliary", "Build", "vcvars64.bat")

    @property
    def msvc_version(self):
        """This is the VCToolset version *NOT* the actual version of the cl compiler
        For CL version, query `Msvc.cl_version`"""
        return Version(re.search(Msvc.version_regex, self.cc).group(1))

    @property
    def short_msvc_version(self):
        """
        This is the shorthand VCToolset version of form
        MSVC<short-ver> *NOT* the full version, for that see
        Msvc.msvc_version or MSVC.platform_toolset_ver for the
        raw platform toolset version
        """
        ver = self.platform_toolset_ver
        return "MSVC" + ver

    @property
    def platform_toolset_ver(self):
        """
        This is the platform toolset version of current MSVC compiler
        i.e. 142.
        This is different from the VC toolset version as established
        by `short_msvc_version`
        """
        return self.msvc_version[:2].joined.string[:3]

    @property
    def cl_version(self):
        """Cl toolset version"""
        return spack.compiler.get_compiler_version_output(self.cc)

    def setup_custom_environment(self, pkg, env):
        """Set environment variables for MSVC using the
        Microsoft-provided script."""
        # Set the build environment variables for spack. Just using
        # subprocess.call() doesn't work since that operates in its own
        # environment which is destroyed (along with the adjusted variables)
        # once the process terminates. So go the long way around: examine
        # output, sort into dictionary, use that to make the build
        # environment.

        # get current platform architecture and format for vcvars argument
        arch = spack.platforms.real_host().default.lower()
        arch = arch.replace("-", "_")
        # vcvars can target specific sdk versions, force it to pick up concretized sdk
        # version, if needed by spec
        sdk_ver = "" if "win-sdk" not in pkg.spec else pkg.spec["win-sdk"].version.string + ".0"
        # provide vcvars with msvc version selected by concretization,
        # not whatever it happens to pick up on the system (highest available version)
        out = subprocess.check_output(  # novermin
            'cmd /u /c "{}" {} {} {} && set'.format(
                self.setvarsfile, arch, sdk_ver, "-vcvars_ver=%s" % self.msvc_version
            ),
            stderr=subprocess.STDOUT,
        )
        if sys.version_info[0] >= 3:
            out = out.decode("utf-16le", errors="replace")  # novermin

        int_env = dict(
            (key.lower(), value)
            for key, _, value in (line.partition("=") for line in out.splitlines())
            if key and value
        )

        if "path" in int_env:
            env.set_path("PATH", int_env["path"].split(";"))
        env.set_path("INCLUDE", int_env.get("include", "").split(";"))
        env.set_path("LIB", int_env.get("lib", "").split(";"))

        env.set("CC", self.cc)
        env.set("CXX", self.cxx)
        env.set("FC", self.fc)
        env.set("F77", self.f77)

    @classmethod
    def fc_version(cls, fc):
        # We're using intel for the Fortran compilers, which exist if
        # ONEAPI_ROOT is a meaningful variable
        if not sys.platform == "win32":
            return "unknown"
        fc_ver = cls.default_version(fc)
        avail_fc_version.add(fc_ver)
        fc_path[fc_ver] = fc
        if os.getenv("ONEAPI_ROOT"):
            try:
                sps = spack.operating_systems.windows_os.WindowsOs.compiler_search_paths
            except AttributeError:
                raise SpackError("Windows compiler search paths not established")
            clp = spack.util.executable.which_string("cl", path=sps)
            ver = cls.default_version(clp)
        else:
            ver = fc_ver
        return ver

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)
