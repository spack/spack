# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Test detection of compiler version"""
import pytest

import spack.compilers.aocc
import spack.compilers.arm
import spack.compilers.cce
import spack.compilers.clang
import spack.compilers.fj
import spack.compilers.gcc
import spack.compilers.intel
import spack.compilers.nag
import spack.compilers.nvhpc
import spack.compilers.oneapi
import spack.compilers.pgi
import spack.compilers.xl
import spack.compilers.xl_r
import spack.util.module_cmd


@pytest.mark.parametrize(
    "version_str,expected_version",
    [
        (
            "Arm C/C++/Fortran Compiler version 19.0 (build number 73) (based on LLVM 7.0.2)\n"
            "Target: aarch64--linux-gnu\n"
            "Thread model: posix\n"
            "InstalledDir:\n"
            "/opt/arm/arm-hpc-compiler-19.0_Generic-AArch64_RHEL-7_aarch64-linux/bin\n",
            "19.0",
        ),
        (
            "Arm C/C++/Fortran Compiler version 19.3.1 (build number 75) (based on LLVM 7.0.2)\n"
            "Target: aarch64--linux-gnu\n"
            "Thread model: posix\n"
            "InstalledDir:\n"
            "/opt/arm/arm-hpc-compiler-19.0_Generic-AArch64_RHEL-7_aarch64-linux/bin\n",
            "19.3.1",
        ),
    ],
)
def test_arm_version_detection(version_str, expected_version):
    version = spack.compilers.arm.Arm.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize(
    "version_str,expected_version",
    [
        ("Cray C : Version 8.4.6  Mon Apr 15, 2019  12:13:39\n", "8.4.6"),
        ("Cray C++ : Version 8.4.6  Mon Apr 15, 2019  12:13:45\n", "8.4.6"),
        ("Cray clang Version 8.4.6  Mon Apr 15, 2019  12:13:45\n", "8.4.6"),
        ("Cray Fortran : Version 8.4.6  Mon Apr 15, 2019  12:13:55\n", "8.4.6"),
    ],
)
def test_cce_version_detection(version_str, expected_version):
    version = spack.compilers.cce.Cce.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.regression("10191")
@pytest.mark.parametrize(
    "version_str,expected_version",
    [
        # macOS clang
        (
            "Apple clang version 11.0.0 (clang-1100.0.33.8)\n"
            "Target: x86_64-apple-darwin18.7.0\n"
            "Thread model: posix\n"
            "InstalledDir: "
            "/Applications/Xcode.app/Contents/Developer/Toolchains/"
            "XcodeDefault.xctoolchain/usr/bin\n",
            "11.0.0",
        ),
        (
            "Apple LLVM version 7.0.2 (clang-700.1.81)\n"
            "Target: x86_64-apple-darwin15.2.0\n"
            "Thread model: posix\n",
            "7.0.2",
        ),
    ],
)
def test_apple_clang_version_detection(version_str, expected_version):
    cls = spack.compilers.class_for_compiler_name("apple-clang")
    version = cls.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.regression("10191")
@pytest.mark.parametrize(
    "version_str,expected_version",
    [
        # LLVM Clang
        (
            "clang version 6.0.1-svn334776-1~exp1~20181018152737.116 (branches/release_60)\n"
            "Target: x86_64-pc-linux-gnu\n"
            "Thread model: posix\n"
            "InstalledDir: /usr/bin\n",
            "6.0.1",
        ),
        (
            "clang version 3.1 (trunk 149096)\n"
            "Target: x86_64-unknown-linux-gnu\n"
            "Thread model: posix\n",
            "3.1",
        ),
        (
            "clang version 8.0.0-3~ubuntu18.04.1 (tags/RELEASE_800/final)\n"
            "Target: x86_64-pc-linux-gnu\n"
            "Thread model: posix\n"
            "InstalledDir: /usr/bin\n",
            "8.0.0",
        ),
        (
            "clang version 9.0.1-+201911131414230800840845a1eea-1~exp1~20191113231141.78\n"
            "Target: x86_64-pc-linux-gnu\n"
            "Thread model: posix\n"
            "InstalledDir: /usr/bin\n",
            "9.0.1",
        ),
        (
            "clang version 8.0.0-3 (tags/RELEASE_800/final)\n"
            "Target: aarch64-unknown-linux-gnu\n"
            "Thread model: posix\n"
            "InstalledDir: /usr/bin\n",
            "8.0.0",
        ),
        (
            "clang version 11.0.0\n"
            "Target: aarch64-unknown-linux-gnu\n"
            "Thread model: posix\n"
            "InstalledDir: /usr/bin\n",
            "11.0.0",
        ),
    ],
)
def test_clang_version_detection(version_str, expected_version):
    version = spack.compilers.clang.Clang.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize(
    "version_str,expected_version",
    [
        # C compiler
        (
            "fcc (FCC) 4.0.0a 20190314\n"
            "simulating gcc version 6.1\n"
            "Copyright FUJITSU LIMITED 2019",
            "4.0.0a",
        ),
        # C++ compiler
        (
            "FCC (FCC) 4.0.0a 20190314\n"
            "simulating gcc version 6.1\n"
            "Copyright FUJITSU LIMITED 2019",
            "4.0.0a",
        ),
        # Fortran compiler
        ("frt (FRT) 4.0.0a 20190314\n" "Copyright FUJITSU LIMITED 2019", "4.0.0a"),
    ],
)
def test_fj_version_detection(version_str, expected_version):
    version = spack.compilers.fj.Fj.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize(
    "version_str,expected_version",
    [
        # Output of -dumpversion changed to return only major from GCC 7
        ("4.4.7\n", "4.4.7"),
        ("7\n", "7"),
    ],
)
def test_gcc_version_detection(version_str, expected_version):
    version = spack.compilers.gcc.Gcc.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize(
    "version_str,expected_version",
    [
        (
            "icpc (ICC) 12.1.5 20120612\n"
            "Copyright (C) 1985-2012 Intel Corporation.  All rights reserved.\n",
            "12.1.5",
        ),
        (
            "ifort (IFORT) 12.1.5 20120612\n"
            "Copyright (C) 1985-2012 Intel Corporation.  All rights reserved.\n",
            "12.1.5",
        ),
    ],
)
def test_intel_version_detection(version_str, expected_version):
    version = spack.compilers.intel.Intel.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize(
    "version_str,expected_version",
    [
        (  # ICX/ICPX
            "Intel(R) oneAPI DPC++ Compiler 2021.1.2 (2020.10.0.1214)\n"
            "Target: x86_64-unknown-linux-gnu\n"
            "Thread model: posix\n"
            "InstalledDir: /made/up/path",
            "2021.1.2",
        ),
        (  # ICX/ICPX
            "Intel(R) oneAPI DPC++ Compiler 2021.2.0 (2021.2.0.20210317)\n"
            "Target: x86_64-unknown-linux-gnu\n"
            "Thread model: posix\n"
            "InstalledDir: /made/up/path",
            "2021.2.0",
        ),
        (  # ICX/ICPX
            "Intel(R) oneAPI DPC++/C++ Compiler 2021.3.0 (2021.3.0.20210619)\n"
            "Target: x86_64-unknown-linux-gnu\n"
            "Thread model: posix\n"
            "InstalledDir: /made/up/path",
            "2021.3.0",
        ),
        (  # ICX/ICPX
            "Intel(R) oneAPI DPC++/C++ Compiler 2021.4.0 (2021.4.0.20210924)\n"
            "Target: x86_64-unknown-linux-gnu\n"
            "Thread model: posix\n"
            "InstalledDir: /made/up/path",
            "2021.4.0",
        ),
        (  # IFX
            "ifx (IFORT) 2021.1.2 Beta 20201214\n"
            "Copyright (C) 1985-2020 Intel Corporation. All rights reserved.",
            "2021.1.2",
        ),
        (  # IFX
            "ifx (IFORT) 2021.2.0 Beta 20210317\n"
            "Copyright (C) 1985-2020 Intel Corporation. All rights reserved.",
            "2021.2.0",
        ),
        (  # IFX
            "ifx (IFORT) 2021.3.0 Beta 20210619\n"
            "Copyright (C) 1985-2020 Intel Corporation. All rights reserved.",
            "2021.3.0",
        ),
        (  # IFX
            "ifx (IFORT) 2021.4.0 Beta 20210924\n"
            "Copyright (C) 1985-2021 Intel Corporation. All rights reserved.",
            "2021.4.0",
        ),
        (  # IFX
            "ifx (IFORT) 2022.0.0 20211123\n"
            "Copyright (C) 1985-2021 Intel Corporation. All rights reserved.",
            "2022.0.0",
        ),
        (  # IFX
            "ifx (IFX) 2023.1.0 20230320\n"
            "Copyright (C) 1985-2023 Intel Corporation. All rights reserved.",
            "2023.1.0",
        ),
    ],
)
def test_oneapi_version_detection(version_str, expected_version):
    version = spack.compilers.oneapi.Oneapi.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize(
    "version_str,expected_version",
    [
        (
            "NAG Fortran Compiler Release 6.0(Hibiya) Build 1037\n"
            "Product NPL6A60NA for x86-64 Linux\n",
            "6.0.1037",
        )
    ],
)
def test_nag_version_detection(version_str, expected_version):
    version = spack.compilers.nag.Nag.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize(
    "version_str,expected_version",
    [
        # C compiler on x86-64
        (
            "nvc 20.9-0 LLVM 64-bit target on x86-64 Linux -tp haswell\n"
            "NVIDIA Compilers and Tools\n"
            "Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.",
            "20.9",
        ),
        # C++ compiler on x86-64
        (
            "nvc++ 20.9-0 LLVM 64-bit target on x86-64 Linux -tp haswell\n"
            "NVIDIA Compilers and Tools\n"
            "Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.",
            "20.9",
        ),
        # Fortran compiler on x86-64
        (
            "nvfortran 20.9-0 LLVM 64-bit target on x86-64 Linux -tp haswell\n"
            "NVIDIA Compilers and Tools\n"
            "Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.",
            "20.9",
        ),
        # C compiler on Power
        (
            "nvc 20.9-0 linuxpower target on Linuxpower\n"
            "NVIDIA Compilers and Tools\n"
            "Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.",
            "20.9",
        ),
        # C++ compiler on Power
        (
            "nvc++ 20.9-0 linuxpower target on Linuxpower\n"
            "NVIDIA Compilers and Tools\n"
            "Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.",
            "20.9",
        ),
        # Fortran compiler on Power
        (
            "nvfortran 20.9-0 linuxpower target on Linuxpower\n"
            "NVIDIA Compilers and Tools\n"
            "Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.",
            "20.9",
        ),
        # C compiler on Arm
        (
            "nvc 20.9-0 linuxarm64 target on aarch64 Linux\n"
            "NVIDIA Compilers and Tools\n"
            "Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.",
            "20.9",
        ),
        # C++ compiler on Arm
        (
            "nvc++ 20.9-0 linuxarm64 target on aarch64 Linux\n"
            "NVIDIA Compilers and Tools\n"
            "Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.",
            "20.9",
        ),
        # Fortran compiler on Arm
        (
            "nvfortran 20.9-0 linuxarm64 target on aarch64 Linux\n"
            "NVIDIA Compilers and Tools\n"
            "Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.",
            "20.9",
        ),
    ],
)
def test_nvhpc_version_detection(version_str, expected_version):
    version = spack.compilers.nvhpc.Nvhpc.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize(
    "version_str,expected_version",
    [
        # Output on x86-64
        (
            "pgcc 15.10-0 64-bit target on x86-64 Linux -tp sandybridge\n"
            "The Portland Group - PGI Compilers and Tools\n"
            "Copyright (c) 2015, NVIDIA CORPORATION.  All rights reserved.\n",
            "15.10",
        ),
        # Output on PowerPC
        (
            "pgcc 17.4-0 linuxpower target on Linuxpower\n"
            "PGI Compilers and Tools\n"
            "Copyright (c) 2017, NVIDIA CORPORATION.  All rights reserved.\n",
            "17.4",
        ),
        # Output when LLVM-enabled
        (
            "pgcc-llvm 18.4-0 LLVM 64-bit target on x86-64 Linux -tp haswell\n"
            "PGI Compilers and Tools\n"
            "Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.\n",
            "18.4",
        ),
    ],
)
def test_pgi_version_detection(version_str, expected_version):
    version = spack.compilers.pgi.Pgi.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize(
    "version_str,expected_version",
    [
        ("IBM XL C/C++ for Linux, V11.1 (5724-X14)\n" "Version: 11.01.0000.0000\n", "11.1"),
        ("IBM XL Fortran for Linux, V13.1 (5724-X16)\n" "Version: 13.01.0000.0000\n", "13.1"),
        ("IBM XL C/C++ for AIX, V11.1 (5724-X13)\n" "Version: 11.01.0000.0009\n", "11.1"),
        (
            "IBM XL C/C++ Advanced Edition for Blue Gene/P, V9.0\n" "Version: 09.00.0000.0017\n",
            "9.0",
        ),
    ],
)
def test_xl_version_detection(version_str, expected_version):
    version = spack.compilers.xl.Xl.extract_version_from_output(version_str)
    assert version == expected_version

    version = spack.compilers.xl_r.XlR.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize(
    "version_str,expected_version",
    [
        # This applies to C,C++ and FORTRAN compiler
        (
            "AMD clang version 12.0.0 (CLANG: AOCC_3_1_0-Build#126 2021_06_07)"
            "(based on LLVM Mirror.Version.12.0.0)\n"
            "Target: x86_64-unknown-linux-gnu\n"
            "Thread model: posix\n",
            "3.1.0",
        ),
        (
            "AMD clang version 12.0.0 (CLANG: AOCC_3.0.0-Build#78 2020_12_10)"
            "(based on LLVM Mirror.Version.12.0.0)\n"
            "Target: x86_64-unknown-linux-gnu\n"
            "Thread model: posix\n",
            "3.0.0",
        ),
        (
            "AMD clang version 11.0.0 (CLANG: AOCC_2.3.0-Build#85 2020_11_10)"
            "(based on LLVM Mirror.Version.11.0.0)\n"
            "Target: x86_64-unknown-linux-gnu\n"
            "Thread model: posix\n",
            "2.3.0",
        ),
        (
            "AMD clang version 10.0.0 (CLANG: AOCC_2.2.0-Build#93 2020_06_25)"
            "(based on LLVM Mirror.Version.10.0.0)\n"
            "Target: x86_64-unknown-linux-gnu\n"
            "Thread model: posix\n",
            "2.2.0",
        ),
    ],
)
def test_aocc_version_detection(version_str, expected_version):
    version = spack.compilers.aocc.Aocc.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.regression("33901")
@pytest.mark.parametrize(
    "version_str",
    [
        (
            "Apple clang version 11.0.0 (clang-1100.0.33.8)\n"
            "Target: x86_64-apple-darwin18.7.0\n"
            "Thread model: posix\n"
            "InstalledDir: "
            "/Applications/Xcode.app/Contents/Developer/Toolchains/"
            "XcodeDefault.xctoolchain/usr/bin\n"
        ),
        (
            "Apple LLVM version 7.0.2 (clang-700.1.81)\n"
            "Target: x86_64-apple-darwin15.2.0\n"
            "Thread model: posix\n"
        ),
    ],
)
def test_apple_clang_not_detected_as_cce(version_str):
    version = spack.compilers.cce.Cce.extract_version_from_output(version_str)
    assert version == "unknown"
