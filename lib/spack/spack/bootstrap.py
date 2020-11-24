# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Bootstrap software needed by Spack"""
import os.path
import sys

import llnl.util.filesystem as fs
import llnl.util.tty as tty
import spack.environment
import spack.paths
import spack.tengine


def clingo():
    """Bootstrap clingo for the current interpreter, if not done before,
    modify sys.path and return the imported Python module.
    """
    # Base directory where to bootstrap software for this interpreter
    root_dir = spack.paths.bootstrap_path

    # Clingo will be installed with a Spack environment, so compute
    # base directory for the manifest file and associated view
    manifest_dir = os.path.join(root_dir, 'clingo')
    manifest_file = os.path.join(manifest_dir, 'spack.yaml')
    view_dir = os.path.join(root_dir, 'view')

    # Check if clingo with Python support is already present
    clingo_libs = fs.find_libraries(['libclingo'], view_dir, recursive=True)
    if clingo_libs:
        return _import_clingo_module(clingo_libs)

    # We need to build clingo, so ensure prerequisites are met first.
    msg = "CLINGO BOOTSTRAP: libclingo.so not found [view={0}]"
    tty.debug(msg.format(view_dir))
    _ensure_clingo_prereq()

    # Warn user that bootstrapping takes time and try to obtain
    # explicit permission
    if not _obtain_user_permission_to_proceed():
        tty.die("Operation aborted.")

    # Write a spack.yaml manifest with the software we need to bootstrap
    _write_clingo_spack_yaml(manifest_file, root_dir)

    with spack.environment.Environment(
            manifest_dir, init_file=manifest_file
    ) as env:
        with env.write_transaction():
            env.concretize()
            env.install_all()
            env.write()

    clingo_libs = fs.find_libraries(['libclingo'], view_dir, recursive=True)
    return _import_clingo_module(clingo_libs)


def _import_clingo_module(clingo_libs):
    python_extension_dir = _extract_extension_dir_from(clingo_libs)
    # Add the path to sys.path and import clingo
    sys.path.append(python_extension_dir)
    import clingo
    return clingo


def _extract_extension_dir_from(clingo_libs):
    msg = "Clingo libraries spread over multiple directories"
    assert len(clingo_libs.directories) == 1, msg
    python_extension_dir = fs.find(clingo_libs.directories[0], 'site-packages')
    msg = "Clingo built without python support"
    assert len(python_extension_dir) == 1, msg
    python_extension_dir = python_extension_dir[0]
    msg = "CLINGO BOOTSTRAP: extensions dir found [dir={0}]"
    tty.debug(msg.format(python_extension_dir))
    return python_extension_dir


def _ensure_clingo_prereq():
    # TODO: Check prerequisites are met, raise if not
    # TODO: 1. Compiler with support for C++14 (clingo)
    pass


def _write_clingo_spack_yaml(manifest_file, root_dir):
    manifest_dir = os.path.dirname(manifest_file)
    tenv = spack.tengine.make_environment()
    template = tenv.get_template('bootstrap/clingo.yaml')

    # Install clingo as an extension of the current interpreter
    interpreter_spec = 'python@{0}.{1}.{2}'.format(
        sys.version_info[0], sys.version_info[1], sys.version_info[2]
    )
    # Assume the interpreter is in a bin directory within the prefix
    interpreter_prefix = os.path.dirname(os.path.dirname(sys.executable))
    context = {
        'interpreter_spec': interpreter_spec,
        'interpreter_prefix': interpreter_prefix,
        'root': root_dir
    }
    text = template.render(**context)

    # Write the manifest file
    fs.mkdirp(manifest_dir)
    with open(manifest_file, 'w') as f:
        f.write(text)


def _obtain_user_permission_to_proceed():
    msg = ("Do you want Spack to bootstrap clingo? [The process will take"
           " several minutes]")
    return tty.get_yes_or_no(msg, default=True)
