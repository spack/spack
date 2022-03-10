# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import shutil
import sys

import pytest

import llnl.util.filesystem

import spack.compilers
import spack.main
import spack.version

compiler = spack.main.SpackCommand('compiler')


@pytest.fixture
def mock_compiler_version():
    return '4.5.3'


@pytest.fixture()
def mock_compiler_dir(tmpdir, mock_compiler_version):
    """Return a directory containing a fake, but detectable compiler."""

    tmpdir.ensure('bin', dir=True)
    bin_dir = tmpdir.join('bin')

    gcc_path = bin_dir.join('gcc')
    gxx_path = bin_dir.join('g++')
    gfortran_path = bin_dir.join('gfortran')

    gcc_path.write("""\
#!/bin/sh

for arg in "$@"; do
    if [ "$arg" = -dumpversion ]; then
        echo '%s'
    fi
done
""" % mock_compiler_version)

    # Create some mock compilers in the temporary directory
    llnl.util.filesystem.set_executable(str(gcc_path))
    gcc_path.copy(gxx_path, mode=True)
    gcc_path.copy(gfortran_path, mode=True)

    return str(tmpdir)


@pytest.mark.regression('11678,13138')
def test_compiler_find_without_paths(no_compilers_yaml, working_env, tmpdir):
    with tmpdir.as_cwd():
        with open('gcc', 'w') as f:
            f.write("""\
#!/bin/sh
echo "0.0.0"
""")
        os.chmod('gcc', 0o700)

    os.environ['PATH'] = str(tmpdir)
    output = compiler('find', '--scope=site')

    assert 'gcc' in output


@pytest.mark.regression('17589')
def test_compiler_find_no_apple_gcc(no_compilers_yaml, working_env, tmpdir):
    with tmpdir.as_cwd():
        # make a script to emulate apple gcc's version args
        with open('gcc', 'w') as f:
            f.write("""\
#!/bin/sh
if [ "$1" = "-dumpversion" ]; then
    echo "4.2.1"
elif [ "$1" = "--version" ]; then
    echo "Configured with: --prefix=/dummy"
    echo "Apple clang version 11.0.0 (clang-1100.0.33.16)"
    echo "Target: x86_64-apple-darwin18.7.0"
    echo "Thread model: posix"
    echo "InstalledDir: /dummy"
else
    echo "clang: error: no input files"
fi
""")
        os.chmod('gcc', 0o700)

    os.environ['PATH'] = str(tmpdir)
    output = compiler('find', '--scope=site')

    assert 'gcc' not in output


def test_compiler_remove(mutable_config, mock_packages):
    args = spack.util.pattern.Bunch(
        all=True, compiler_spec='gcc@4.5.0', add_paths=[], scope=None
    )
    spack.cmd.compiler.compiler_remove(args)
    compilers = spack.compilers.all_compiler_specs()
    assert spack.spec.CompilerSpec("gcc@4.5.0") not in compilers


def test_compiler_add(
        mutable_config, mock_packages, mock_compiler_dir, mock_compiler_version
):
    # Compilers available by default.
    old_compilers = set(spack.compilers.all_compiler_specs())

    args = spack.util.pattern.Bunch(
        all=None,
        compiler_spec=None,
        add_paths=[mock_compiler_dir],
        scope=None
    )
    spack.cmd.compiler.compiler_find(args)

    # Ensure new compiler is in there
    new_compilers = set(spack.compilers.all_compiler_specs())
    new_compiler = new_compilers - old_compilers
    assert any(c.version == spack.version.Version(mock_compiler_version)
               for c in new_compiler)


@pytest.fixture
def clangdir(tmpdir):
    """Create a directory with some dummy compiler scripts in it.

    Scripts are:
      - clang
      - clang++
      - gcc
      - g++
      - gfortran-8

    """
    with tmpdir.as_cwd():
        with open('clang', 'w') as f:
            f.write("""\
#!/bin/sh
if [ "$1" = "--version" ]; then
    echo "clang version 11.0.0 (clang-1100.0.33.16)"
    echo "Target: x86_64-apple-darwin18.7.0"
    echo "Thread model: posix"
    echo "InstalledDir: /dummy"
else
    echo "clang: error: no input files"
    exit 1
fi
""")
        shutil.copy('clang', 'clang++')

        gcc_script = """\
#!/bin/sh
if [ "$1" = "-dumpversion" ]; then
    echo "8"
elif [ "$1" = "-dumpfullversion" ]; then
    echo "8.4.0"
elif [ "$1" = "--version" ]; then
    echo "{0} (GCC) 8.4.0 20120313 (Red Hat 8.4.0-1)"
    echo "Copyright (C) 2010 Free Software Foundation, Inc."
else
    echo "{1}: fatal error: no input files"
    echo "compilation terminated."
    exit 1
fi
"""
        with open('gcc-8', 'w') as f:
            f.write(gcc_script.format('gcc', 'gcc-8'))
        with open('g++-8', 'w') as f:
            f.write(gcc_script.format('g++', 'g++-8'))
        with open('gfortran-8', 'w') as f:
            f.write(gcc_script.format('GNU Fortran', 'gfortran-8'))
        os.chmod('clang', 0o700)
        os.chmod('clang++', 0o700)
        os.chmod('gcc-8', 0o700)
        os.chmod('g++-8', 0o700)
        os.chmod('gfortran-8', 0o700)

    yield tmpdir


@pytest.mark.regression('17590')
def test_compiler_find_mixed_suffixes(
        no_compilers_yaml, working_env, clangdir):
    """Ensure that we'll mix compilers with different suffixes when necessary.
    """
    os.environ['PATH'] = str(clangdir)
    output = compiler('find', '--scope=site')

    assert 'clang@11.0.0' in output
    assert 'gcc@8.4.0' in output

    config = spack.compilers.get_compiler_config('site', False)
    clang = next(c['compiler'] for c in config
                 if c['compiler']['spec'] == 'clang@11.0.0')
    gcc = next(c['compiler'] for c in config
               if c['compiler']['spec'] == 'gcc@8.4.0')

    gfortran_path = str(clangdir.join('gfortran-8'))

    assert clang['paths'] == {
        'cc': str(clangdir.join('clang')),
        'cxx': str(clangdir.join('clang++')),
        # we only auto-detect mixed clang on macos
        'f77': gfortran_path if sys.platform == 'darwin' else None,
        'fc': gfortran_path if sys.platform == 'darwin' else None,
    }

    assert gcc['paths'] == {
        'cc': str(clangdir.join('gcc-8')),
        'cxx': str(clangdir.join('g++-8')),
        'f77': gfortran_path,
        'fc': gfortran_path,
    }


@pytest.mark.regression('17590')
def test_compiler_find_prefer_no_suffix(
        no_compilers_yaml, working_env, clangdir):
    """Ensure that we'll pick 'clang' over 'clang-gpu' when there is a choice.
    """
    with clangdir.as_cwd():
        shutil.copy('clang', 'clang-gpu')
        shutil.copy('clang++', 'clang++-gpu')
        os.chmod('clang-gpu', 0o700)
        os.chmod('clang++-gpu', 0o700)

    os.environ['PATH'] = str(clangdir)
    output = compiler('find', '--scope=site')

    assert 'clang@11.0.0' in output
    assert 'gcc@8.4.0' in output

    config = spack.compilers.get_compiler_config('site', False)
    clang = next(c['compiler'] for c in config
                 if c['compiler']['spec'] == 'clang@11.0.0')

    assert clang['paths']['cc'] == str(clangdir.join('clang'))
    assert clang['paths']['cxx'] == str(clangdir.join('clang++'))


def test_compiler_find_path_order(
        no_compilers_yaml, working_env, clangdir):
    """Ensure that we find compilers that come first in the PATH first
    """

    with clangdir.as_cwd():
        os.mkdir('first_in_path')
        shutil.copy('gcc-8', 'first_in_path/gcc-8')
        shutil.copy('g++-8', 'first_in_path/g++-8')
        shutil.copy('gfortran-8', 'first_in_path/gfortran-8')

    # the first_in_path folder should be searched first
    os.environ['PATH'] = '{0}:{1}'.format(
        str(clangdir.join("first_in_path")),
        str(clangdir),
    )

    compiler('find', '--scope=site')

    config = spack.compilers.get_compiler_config('site', False)

    gcc = next(c['compiler'] for c in config
               if c['compiler']['spec'] == 'gcc@8.4.0')

    assert gcc['paths'] == {
        'cc': str(clangdir.join('first_in_path', 'gcc-8')),
        'cxx': str(clangdir.join('first_in_path', 'g++-8')),
        'f77': str(clangdir.join('first_in_path', 'gfortran-8')),
        'fc': str(clangdir.join('first_in_path', 'gfortran-8')),
    }


def test_compiler_list_empty(no_compilers_yaml, working_env, clangdir):
    # Spack should not automatically search for compilers when listing them and none
    # are available. And when stdout is not a tty like in tests, there should be no
    # output and no error exit code.
    os.environ['PATH'] = str(clangdir)
    out = compiler('list')
    assert not out
    assert compiler.returncode == 0
