# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.error


class CompilerAccessError(spack.error.SpackError):
    def __init__(self, compiler, paths):
        msg = f"Compiler '{compiler.spec}' has executables that are missing"
        msg += f" or are not executable: {paths}"
        super().__init__(msg)


class UnsupportedCompilerFlag(spack.error.SpackError):
    def __init__(self, compiler, feature, flag_name, ver_string=None):
        super().__init__(
            f"{compiler.name} ({ver_string if ver_string else compiler.version}) does not support"
            f" {feature} (as compiler.{flag_name}). If you think it should, please edit the "
            f"compiler.{compiler.name} subclass to implement the {flag_name} property and submit "
            f"a pull request or issue."
        )
