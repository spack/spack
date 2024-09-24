import spack.package as sp


def load():

    #
    # ----- Compilers ---------
    #
    with sp.when("%gcc"):
        with sp.when("%gcc@4.4.7"):
            # https://svn.boost.org/trac/boost/ticket/11856
            sp.patch("patches/boost_11856.patch", when="@1.60.0")

        with sp.when("%gcc@5.0:"):
            # https://svn.boost.org/trac/boost/ticket/10125
            sp.patch("patches/call_once_variadic.patch", when="@1.54.0:1.55")

        with sp.when("%gcc@8.3"):
            # Workaround gcc-8.3 compiler issue https://github.com/boostorg/mpl/issues/44
            sp.patch("patches/boost_gcc83_cpp17_fix.patch", when="@1.69:")

    with sp.when("%fj"):
        # Change the method for version analysis when using Fujitsu compiler.
        sp.patch("patches/fujitsu_version_analysis.patch", when="@1.67.0:1.76.0")
        sp.patch("patches/fujitsu_version_analysis-1.77.patch", when="@1.77.0:")

    with sp.when("%xl"):
        # IBM XL C
        sp.patch("patches/xl_1_62_0_le.patch", when="@1.62.0")

    with sp.when("%xl_r"):
        # IBM XL C++
        sp.patch("patches/xl_1_62_0_le.patch", when="@1.62.0")

    with sp.when("%pgi"):
        sp.patch("patches/boost_1.67.0_pgi.patch", when="@1.67.0:1.68")
        sp.patch("patches/boost_1.63.0_pgi.patch", when="@1.63.0")

        with sp.when("%pgi@17.4"):
            sp.patch("patches/boost_1.63.0_pgi_17.4_workaround.patch", when="@1.63.0")

    with sp.when("%nvhpc"):
        # Override the PGI toolset when using the NVIDIA compilers
        sp.patch("patches/nvhpc-1.74.patch", when="@1.74.0:1.75")
        sp.patch("patches/nvhpc-1.76.patch", when="@1.76.0:1.76")

        # Workaround compiler bug
        sp.patch("patches/nvhpc-find_address.patch", when="@1.75.0:1.76")

    with sp.when("%cce"):
        with sp.when("%cce@:1.76"):
            # Fix float128 support when building with CUDA and Cray compiler
            sp.patch(
                "patches/config_PR378.patch",
                sha256="666eec8cfb0f71a87443ab27d179a9771bda32bcb8ff5e16afa3767f7b7f1e70",
                level=2,
            )

    with sp.when("%oneapi"):
        # https://www.intel.com/content/www/us/en/developer/articles/technical/building-boost-with-oneapi.html
        sp.patch("patches/intel-oneapi-linux-jam.patch", when="@1.76:")

    #
    # ----- Platform-specific ---------
    #
    with sp.when("platform=darwin"):
        # Fix for version comparison on newer Clang on darwin
        # See: https://github.com/boostorg/build/issues/440
        # See: https://github.com/macports/macports-ports/pull/6726
        sp.patch("patches/darwin_clang_version.patch", level=0, when="@1.56.0:1.72.0")

        # Allow building context asm sources with GCC on Darwin
        # See https://github.com/spack/spack/pull/24889
        # and https://github.com/boostorg/context/issues/177
        sp.patch("patches/context-macho-gcc.patch", when="@1.65:1.76 +context %gcc")

    with sp.when("platform=windows"):
        # https://github.com/boostorg/filesystem/issues/284
        sp.patch(
            "patches/filesystem_PR284.patch",
            when="@1.82.0",
            sha256="738ba8e0d7b5cdcf5fae4998f9450b51577bbde1bb0d220a0721551609714ca4",
        )

    #
    # ----- Python ---------
    #
    with sp.when("^python@3:"):
        # Patch fix from https://svn.boost.org/trac/boost/ticket/11120
        sp.patch("patches/python_jam-1_77.patch", when="@1.77:")
        sp.patch("patches/python_jam.patch", when="@1.56:1.76")
        sp.patch("patches/python_jam_pre156.patch", when="@:1.55.0")

    #
    # ----- Generic Fixes ---------
    #

    # Fix missing declaration of uintptr_t with glibc>=2.17 - https://bugs.gentoo.org/482372
    sp.patch(
        "patches/glibc_gentoo_v1.53.0.patch",
        when="@1.53.0:1.54",
        sha256="b6f6ce68282159d46c716a1e6c819c815914bdb096cddc516fa48134209659f2",
    )

    # Add option to C/C++ compile commands in clang-linux.jam
    sp.patch("patches/clang-linux_add_option.patch", when="@1.56.0:1.63.0")
    sp.patch("patches/clang-linux_add_option2.patch", when="@1.47.0:1.55.0")

    # Support bzip2 and gzip in other directory
    # See https://github.com/boostorg/build/pull/154
    sp.patch("patches/build_PR154.patch", when="@1.56.0:1.63")

    # Backport Python3 import problem
    # See https://github.com/boostorg/python/pull/218
    sp.patch("patches/python_PR218.patch", when="@1.63.0:1.67")

    # Fix: "Unable to compile code using boost/process.hpp"
    # See: https://github.com/boostorg/process/issues/116
    sp.patch("patches/process_PR116.patch", level=2, when="@1.72.0")

    # Patch fix for warnings from commits 2d37749, af1dc84, c705bab, and
    # 0134441 on https://github.com/boostorg/system.
    sp.patch("patches/system-non-virtual-dtor-include.patch", when="@1.69.0", level=2)
    sp.patch(
        "patches/system-non-virtual-dtor-test.patch",
        when="@1.69.0",
        working_dir="libs/system",
        level=1,
    )

    # Fix issues with PTHREAD_STACK_MIN not being a DEFINED constant in newer glibc
    # See https://github.com/spack/spack/issues/28273
    sp.patch("patches/pthread-stack-min-fix.patch", when="@1.69.0:1.72.0")

    # C++20 concepts fix for Beast
    # See https://github.com/boostorg/beast/pull/1927 for details
    sp.patch(
        "patches/beast_PR1927.patch",
        sha256="4dd507e1f5a29e3b87b15321a4d8c74afdc8331433edabf7aeab89b3c405d556",
        when="@1.73.0",
    )

    # Cloning a status_code with indirecting_domain leads to segmentation fault
    # See https://github.com/ned14/outcome/issues/223 for details
    sp.patch(
        "patches/outcome_PR223.patch",
        sha256="246508e052c44b6f4e8c2542a71c06cacaa72cd1447ab8d2a542b987bc35ace9",
        when="@1.73.0",
    )

    # Fix B2 bootstrap toolset during installation
    # See https://github.com/spack/spack/issues/20757
    # and https://github.com/spack/spack/pull/21408
    sp.patch("patches/bootstrap-toolset.patch", when="@1.75")

    # Fix compiler used for building bjam during bootstrap
    sp.patch("patches/bootstrap-compiler.patch", when="@1.76:")

    # Fix building with Intel compilers
    sp.patch(
        "patches/b2_PR79.patch",
        sha256="4849671f9df4b8f3c962130d7f6d44eba3b20d113e84f9faade75e6469e90310",
        when="@1.77.0",
        working_dir="tools/build",
    )

    with sp.when("@1.78.0"):
        # https://github.com/bfgroup/b2/pull/113
        sp.patch(
            "patches/build_PR113.patch",
            sha256="0e1b19e91e0fef2906b3e1bed1ba06b277ff84942bb8ac9e645dd93ad3532b4e",
        )

        # UWP support for atomic
        sp.patch(
            "patches/atomic_PR54.patch",
            when="+atomic",
            sha256="1be9f01f238d54ce311c2a8a5ddbdd3f97268c0c011460e41033443d70280a18",
        )

    # https://github.com/boostorg/json/issues/692
    sp.patch(
        "patches/json_PR695.patch",
        when="@1.79.0 +json",
        sha256="0edcb348b9c6f6ab8c67735881dccd9759af852830ffe651ae51248e24ff11ac",
    )

    # https://github.com/boostorg/phoenix/issues/111
    sp.patch("patches/phoenix_PR111.patch", level=2, when="@1.81.0:1.83.0")
