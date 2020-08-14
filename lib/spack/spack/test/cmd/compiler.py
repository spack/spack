# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
def no_compilers_yaml(mutable_config):
    """Creates a temporary configuration without compilers.yaml"""

    for scope, local_config in mutable_config.scopes.items():
        compilers_yaml = os.path.join(
            local_config.path, scope, 'compilers.yaml'
        )
        if os.path.exists(compilers_yaml):
            os.remove(compilers_yaml)


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
def test_compiler_find_without_paths(
        no_compilers_yaml, working_env, mock_compiler_dir
):
    os.environ['PATH'] = mock_compiler_dir
    output = compiler('find', '--scope=site')
    assert 'gcc' in output


@pytest.mark.regression('17589')
def test_compiler_find_no_apple_gcc(
        no_compilers_yaml, mock_executable, monkeypatch
):
    gcc_exe = mock_executable('gcc', output="""\
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
    monkeypatch.setenv('PATH', os.path.dirname(gcc_exe), prepend=False)
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
    no_compilers_yaml, working_env, mock_compiler_dir, mock_compiler_version
):
    os.environ['PATH'] = mock_compiler_dir
    compiler('find', '--scope=site')

    # Ensure new compiler is in there
    compilers = set(spack.compilers.all_compiler_specs())
    expected_version = spack.version.Version(mock_compiler_version)
    assert any(c.version == expected_version for c in compilers)


@pytest.fixture
def clangdir(mock_executable):
    """Create a directory with some dummy compiler scripts in it.

    Scripts are:
      - clang
      - clang++
      - gcc
      - g++
      - gfortran-8

    """
    clang_path = mock_executable('clang', output="""\
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
    bindir = os.path.dirname(clang_path)
    shutil.copy(clang_path, os.path.join(bindir, 'clang++'))

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
    mock_executable('gcc-8', output=gcc_script.format('gcc', 'gcc-8'))
    mock_executable('g++-8', output=gcc_script.format('g++', 'g++-8'))
    mock_executable('gfortran-8', output=gcc_script.format(
        'GNU Fortran', 'gfortran-8'
    ))

    yield bindir


@pytest.mark.regression('17590')
def test_compiler_find_mixed_suffixes(
        no_compilers_yaml, monkeypatch, clangdir
):
    """Ensure that we'll mix compilers with different suffixes when necessary.
    """
    monkeypatch.setenv('PATH', str(clangdir))
    output = compiler('find', '--scope=site')

    assert 'clang@11.0.0' in output
    assert 'gcc@8.4.0' in output

    config = spack.compilers.get_compiler_config('site')
    clang = next(c['compiler'] for c in config
                 if c['compiler']['spec'] == 'clang@11.0.0')
    gcc = next(c['compiler'] for c in config
               if c['compiler']['spec'] == 'gcc@8.4.0')

    gfortran_path = os.path.join(clangdir, 'gfortran-8')
    assert clang['paths'] == {
        'cc': os.path.join(clangdir, 'clang'),
        'cxx': os.path.join(clangdir, 'clang++'),
        # we only auto-detect mixed clang on macos
        'f77': gfortran_path if sys.platform == 'darwin' else None,
        'fc': gfortran_path if sys.platform == 'darwin' else None,
    }

    assert gcc['paths'] == {
        'cc': os.path.join(clangdir, 'gcc-8'),
        'cxx': os.path.join(clangdir, 'g++-8'),
        'f77': gfortran_path,
        'fc': gfortran_path,
    }


@pytest.mark.regression('17590')
def test_compiler_find_prefer_no_suffix(
        no_compilers_yaml, monkeypatch, clangdir
):
    """Ensure that we'll pick 'clang' over 'clang-gpu' when there is a choice.
    """
    with llnl.util.filesystem.working_dir(clangdir):
        shutil.copy('clang', 'clang-gpu')
        shutil.copy('clang++', 'clang++-gpu')
        os.chmod('clang-gpu', 0o700)
        os.chmod('clang++-gpu', 0o700)

    monkeypatch.setenv('PATH', clangdir)
    output = compiler('find', '--scope=site')

    assert 'clang@11.0.0' in output
    assert 'gcc@8.4.0' in output

    config = spack.compilers.get_compiler_config('site')
    clang = next(c['compiler'] for c in config
                 if c['compiler']['spec'] == 'clang@11.0.0')

    assert clang['paths']['cc'] == os.path.join(clangdir, 'clang')
    assert clang['paths']['cxx'] == os.path.join(clangdir, 'clang++')


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
