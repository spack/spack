from pathlib import Path


def b2_name(spec):
    # 'b2' was named 'bjam' before 1.47
    if spec.satisfies("platform=windows"):
        if spec.satisfies("@1.47:"):
            return "b2.exe"
        return "bjam.exe"

    if spec.satisfies("@1.47:"):
        return "./b2"
    return "./bjam"


def write_user_jam_file(filename, spec, cxx, toolset):
    with open(filename, "w") as f:
        # Boost may end up using gcc even though clang+gfortran is set in
        # compilers.yaml. Make sure this does not happen.
        # Skip this on Windows since we don't have a cl.exe wrapper in spack
        if not spec.satisfies("platform=windows"):
            f.write(f"using {toolset} : : {cxx} ;\n")

        if spec.satisfies("+mpi"):
            # Use the correct mpi compiler.  If the compiler options are
            # empty or undefined, Boost will attempt to figure out the
            # correct options by running "${mpicxx} -show" or something
            # similar, but that doesn't work with the Cray compiler
            # wrappers.  Since Boost doesn't use the MPI C++ bindings,
            # that can be used as a compiler option instead.
            mpi_line = "using mpi : %s" % Path(spec["mpi"].mpicxx).as_posix()
            f.write(mpi_line + " ;\n")

        if spec.satisfies("+python"):
            f.write(_python_line(spec))


def threading_options(spec):
    opts = list()

    if spec.satisfies("+multithreaded"):
        opts.append("multi")

    if spec.satisfies("+singlethreaded"):
        opts.append("single")

    if not opts:
        raise RuntimeError("At least one of {singlethreaded, multithreaded} must be enabled")

    return opts


def b2_options(spec):
    opts = list()

    if spec.satisfies("+debug"):
        opts.append("variant=debug")
    else:
        opts.append("variant=release")

    if spec.satisfies("+icu"):
        opts.extend(["-s", "ICU_PATH=%s" % spec["icu4c"].prefix])
    else:
        opts.append("--disable-icu")

    if spec.satisfies("+iostreams"):
        opts.extend(
            [
                "-s",
                "BZIP2_INCLUDE=%s" % spec["bzip2"].prefix.include,
                "-s",
                "BZIP2_LIBPATH=%s" % spec["bzip2"].prefix.lib,
                "-s",
                "ZLIB_INCLUDE=%s" % spec["zlib-api"].prefix.include,
                "-s",
                "ZLIB_LIBPATH=%s" % spec["zlib-api"].prefix.lib,
                "-s",
                "LZMA_INCLUDE=%s" % spec["xz"].prefix.include,
                "-s",
                "LZMA_LIBPATH=%s" % spec["xz"].prefix.lib,
                "-s",
                "ZSTD_INCLUDE=%s" % spec["zstd"].prefix.include,
                "-s",
                "ZSTD_LIBPATH=%s" % spec["zstd"].prefix.lib,
            ]
        )

        # At least with older Xcode, _lzma_cputhreads is missing (#33998)
        if spec.satisfies("platform=darwin"):
            opts.extend(["-s", "NO_LZMA=1"])

    link_types = ["static"]
    if spec.satisfies("+shared"):
        link_types.append("shared")
    opts.append("link={0}".format(",".join(link_types)))

    # If we are building context, tell b2 which backend to use
    if spec.satisfies("+context") and "context-impl" in spec.variants:
        opts.extend(["context-impl=%s" % spec.variants["context-impl"].value])

    layout = _layout(spec)
    opts.append(f"--layout={layout}")

    if layout == "system" and len(threading_options(spec)) > 1:
        raise RuntimeError(
            "Cannot build both single and multi-threaded targets with system layout"
        )

    opts.extend(_cxx_flags(spec))

    # clang is not officially supported for pre-compiled headers
    # and at least in clang 3.9 still fails to build
    #   https://www.boost.org/build/doc/html/bbv2/reference/precompiled_headers.html
    if spec.satisfies("%apple-clang") or spec.satisfies("%clang") or spec.satisfies("%fj"):
        opts.append("pch=off")

    # Visibility was added in 1.69.0.
    if spec.satisfies("@1.69.0:"):
        opts.append("visibility=%s" % spec.variants["visibility"].value)

    return opts


def _cxx_flags(spec):
    all_opts = list()
    cxx_build_flags = list()
    cxx_link_flags = list()

    if spec.satisfies("@1.66:"):
        # `cxxstd` is a separate flag since 1.66.0
        all_opts.append("cxxstd={0}".format(spec.variants["cxxstd"].value))
    else:
        # Add to cxx_build_flags for older Boost
        cxxstd = spec.variants["cxxstd"].value
        flag = getattr(spec.package.compiler, "cxx{0}_flag".format(cxxstd))
        if flag:
            cxx_build_flags.append(flag)

    if spec.satisfies("+pic"):
        cxx_build_flags.append(spec.package.compiler.cxx_pic_flag)

    if spec.satisfies("%xl") or spec.satisfies("%xl_r"):
        # see also: https://lists.boost.org/boost-users/2019/09/89953.php
        # the cxxstd setting via spack is not sufficient to drive the
        # change into boost compilation
        if spec.variants["cxxstd"].value == "11":
            cxx_build_flags.append("-std=c++11")

    if spec.satisfies("+clanglibcpp"):
        cxx_build_flags.append("-stdlib=libc++")
        cxx_link_flags.append("-stdlib=libc++")

    all_opts.append("cxxflags={0:s}".format(" ".join(cxx_build_flags)))
    all_opts.append("linkflags={0:s}".format(" ".join(cxx_link_flags)))

    return all_opts


def _python_line(spec):
    # avoid "ambiguous key" error
    if spec.satisfies("@:1.58"):
        return ""

    return "using python : {0} : {1} : {2} : {3} ;\n".format(
        spec["python"].version.up_to(2),
        Path(spec["python"].command.path).as_posix(),
        Path(spec["python"].headers.directories[0]).as_posix(),
        Path(spec["python"].libs[0]).parent.as_posix(),
    )


def _layout(spec):
    if spec.satisfies("+taggedlayout"):
        return "tagged"

    if spec.satisfies("+versionedlayout"):
        return "versioned"

    return "system"
