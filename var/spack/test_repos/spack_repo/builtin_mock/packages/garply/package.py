# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import sys

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class Garply(Package):
    """Toy package for testing dependencies"""

    homepage = "https://www.example.com"
    has_code = False
    version("3.0.0")

    def install(self, spec, prefix):
        garply_h = """#ifndef GARPLY_H_

class Garply
{
private:
    static const int version_major;
    static const int version_minor;

public:
    Garply();
    int get_version() const;
    int garplinate() const;
};

#endif // GARPLY_H_
"""
        garply_cc = """#include "garply.h"
#include "garply_version.h"
#include <iostream>

const int Garply::version_major = garply_version_major;
const int Garply::version_minor = garply_version_minor;

Garply::Garply() {}

int
Garply::get_version() const
{
    return 10 * version_major + version_minor;
}

int
Garply::garplinate() const
{
    std::cout << "Garply::garplinate version " << get_version()
              << " invoked" << std::endl;
    std::cout << "Garply config dir = %s" << std::endl;
    return get_version();
}
"""
        garplinator_cc = """#include "garply.h"
#include <iostream>

int
main()
{
    Garply garply;
    garply.garplinate();

    return 0;
}
"""
        garply_version_h = """const int garply_version_major = %s;
const int garply_version_minor = %s;
"""
        mkdirp(f"{prefix.include}/garply")
        mkdirp(f"{self.stage.source_path}/garply")
        with open(f"{self.stage.source_path}/garply_version.h", "w", encoding="utf-8") as f:
            f.write(garply_version_h % (self.version[0], self.version[1:]))
        with open(f"{self.stage.source_path}/garply/garply.h", "w", encoding="utf-8") as f:
            f.write(garply_h)
        with open(f"{self.stage.source_path}/garply/garply.cc", "w", encoding="utf-8") as f:
            f.write(garply_cc % prefix.config)
        with open(f"{self.stage.source_path}/garply/garplinator.cc", "w", encoding="utf-8") as f:
            f.write(garplinator_cc)
        gpp = which(
            "g++",
            path=":".join(
                [s for s in os.environ["PATH"].split(os.pathsep) if "lib/spack/env" not in s]
            ),
        )
        if sys.platform == "darwin":
            gpp = which("/usr/bin/clang++")
        gpp(
            "-Dgarply_EXPORTS",
            f"-I{self.stage.source_path}",
            "-O2",
            "-g",
            "-DNDEBUG",
            "-fPIC",
            "-o",
            "garply.cc.o",
            "-c",
            f"{self.stage.source_path}/garply/garply.cc",
        )
        gpp(
            "-Dgarply_EXPORTS",
            f"-I{self.stage.source_path}",
            "-O2",
            "-g",
            "-DNDEBUG",
            "-fPIC",
            "-o",
            "garplinator.cc.o",
            "-c",
            f"{self.stage.source_path}/garply/garplinator.cc",
        )
        if sys.platform == "darwin":
            gpp(
                "-fPIC",
                "-O2",
                "-g",
                "-DNDEBUG",
                "-dynamiclib",
                "-Wl,-headerpad_max_install_names",
                "-o",
                "libgarply.dylib",
                "-install_name",
                "@rpath/libgarply.dylib",
                "garply.cc.o",
            )
            gpp(
                "-O2",
                "-g",
                "-DNDEBUG",
                "-Wl,-search_paths_first",
                "-Wl,-headerpad_max_install_names",
                "garplinator.cc.o",
                "-o",
                "garplinator",
                f"-Wl,-rpath,{prefix.lib64}",
                "libgarply.dylib",
            )
            mkdirp(prefix.lib64)
            copy("libgarply.dylib", f"{prefix.lib64}/libgarply.dylib")
            os.link(f"{prefix.lib64}/libgarply.dylib", f"{prefix.lib64}/libgarply.dylib.3.0")
        else:
            gpp(
                "-fPIC",
                "-O2",
                "-g",
                "-DNDEBUG",
                "-shared",
                "-Wl,-soname,libgarply.so",
                "-o",
                "libgarply.so",
                "garply.cc.o",
            )
            gpp(
                "-O2",
                "-g",
                "-DNDEBUG",
                "-rdynamic",
                "garplinator.cc.o",
                "-o",
                "garplinator",
                f"-Wl,-rpath,{prefix.lib64}",
                "libgarply.so",
            )
            mkdirp(prefix.lib64)
            copy("libgarply.so", f"{prefix.lib64}/libgarply.so")
            os.link(f"{prefix.lib64}/libgarply.so", f"{prefix.lib64}/libgarply.so.3.0")
        copy("garplinator", f"{prefix.lib64}/garplinator")
        copy(f"{self.stage.source_path}/garply/garply.h", f"{prefix.include}/garply/garply.h")
        mkdirp(prefix.bin)
        copy("garply_version.h", f"{prefix.bin}/garply_version.h")
        os.symlink(f"{prefix.lib64}/garplinator", f"{prefix.bin}/garplinator")
