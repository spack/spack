# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import llnl.util.tty as tty

import spack.error
import spack.version
from spack.util.module_cmd import module

from .linux_distro import LinuxDistro

#: Possible locations of the Cray CLE release file,
#: which we look at to get the CNL OS version.
_cle_release_file = "/etc/opt/cray/release/cle-release"
_clerelease_file = "/etc/opt/cray/release/clerelease"


def read_cle_release_file():
    """Read the CLE release file and return a dict with its attributes.

    This file is present on newer versions of Cray.

    The release file looks something like this::

        RELEASE=6.0.UP07
        BUILD=6.0.7424
        ...

    The dictionary we produce looks like this::

        {
          "RELEASE": "6.0.UP07",
          "BUILD": "6.0.7424",
          ...
        }

    Returns:
        dict: dictionary of release attributes
    """
    with open(_cle_release_file) as release_file:
        result = {}
        for line in release_file:
            # use partition instead of split() to ensure we only split on
            # the first '=' in the line.
            key, _, value = line.partition("=")
            result[key] = value.strip()
        return result


def read_clerelease_file():
    """Read the CLE release file and return the Cray OS version.

    This file is present on older versions of Cray.

    The release file looks something like this::

        5.2.UP04

    Returns:
        str: the Cray OS version
    """
    with open(_clerelease_file) as release_file:
        for line in release_file:
            return line.strip()


class CrayBackend(LinuxDistro):
    """Compute Node Linux (CNL) is the operating system used for the Cray XC
    series super computers. It is a very stripped down version of GNU/Linux.
    Any compilers found through this operating system will be used with
    modules. If updated, user must make sure that version and name are
    updated to indicate that OS has been upgraded (or downgraded)
    """

    def __init__(self):
        name = "cnl"
        version = self._detect_crayos_version()
        if version:
            # If we found a CrayOS version, we do not want the information
            # from LinuxDistro. In order to skip the logic from
            # distro.linux_distribution, while still calling __init__
            # methods further up the MRO, we skip LinuxDistro in the MRO and
            # call the OperatingSystem superclass __init__ method
            super(LinuxDistro, self).__init__(name, version)
        else:
            super().__init__()
        self.modulecmd = module

    def __str__(self):
        return self.name + str(self.version)

    @classmethod
    def _detect_crayos_version(cls):
        if os.path.isfile(_cle_release_file):
            release_attrs = read_cle_release_file()
            if "RELEASE" not in release_attrs:
                # This Cray system uses a base OS not CLE/CNL
                return None
            v = spack.version.Version(release_attrs["RELEASE"])
            return v[0]
        elif os.path.isfile(_clerelease_file):
            v = read_clerelease_file()
            return spack.version.Version(v)[0]
        else:
            # Not all Cray systems run CNL on the backend.
            # Systems running in what Cray calls "cluster" mode run other
            # linux OSs under the Cray PE.
            # So if we don't detect any Cray OS version on the system,
            # we return None. We can't ever be sure we will get a Cray OS
            # version.
            # Returning None allows the calling code to test for the value
            # being "True-ish" rather than requiring a try/except block.
            return None

    def arguments_to_detect_version_fn(self, paths):
        import spack.compilers

        command_arguments = []
        for compiler_name in spack.compilers.supported_compilers():
            cmp_cls = spack.compilers.class_for_compiler_name(compiler_name)

            # If the compiler doesn't have a corresponding
            # Programming Environment, skip to the next
            if cmp_cls.PrgEnv is None:
                continue

            if cmp_cls.PrgEnv_compiler is None:
                tty.die("Must supply PrgEnv_compiler with PrgEnv")

            compiler_id = spack.compilers.CompilerID(self, compiler_name, None)
            detect_version_args = spack.compilers.DetectVersionArgs(
                id=compiler_id, variation=(None, None), language="cc", path="cc"
            )
            command_arguments.append(detect_version_args)
        return command_arguments

    def detect_version(self, detect_version_args):
        import spack.compilers

        modulecmd = self.modulecmd
        compiler_name = detect_version_args.id.compiler_name
        compiler_cls = spack.compilers.class_for_compiler_name(compiler_name)
        output = modulecmd("avail", compiler_cls.PrgEnv_compiler)
        version_regex = r"({0})/([\d\.]+[\d]-?[\w]*)".format(compiler_cls.PrgEnv_compiler)
        matches = re.findall(version_regex, output)
        version = tuple(version for _, version in matches if "classic" not in version)
        compiler_id = detect_version_args.id
        value = detect_version_args._replace(id=compiler_id._replace(version=version))
        return value, None

    def make_compilers(self, compiler_id, paths):
        import spack.spec

        name = compiler_id.compiler_name
        cmp_cls = spack.compilers.class_for_compiler_name(name)
        compilers = []
        for v in compiler_id.version:
            comp = cmp_cls(
                spack.spec.CompilerSpec(name + "@=" + v),
                self,
                "any",
                ["cc", "CC", "ftn"],
                [cmp_cls.PrgEnv, name + "/" + v],
            )

            compilers.append(comp)
        return compilers
