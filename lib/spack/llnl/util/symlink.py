# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from os.path import exists, join, islink
import os
import tempfile
import shutil
import six
import sys

import llnl.util.filesystem as fs

__win32_can_symlink__ = None

def symlink(real_path, link_path):
    """
    Create a symbolic link.

    On Windows, use junctions if os.symlink fails.
    """
    if sys.platform != "win32" or _win32_can_symlink():
        os.symlink(real_path, link_path)
    else:
        # Use junctions
        _win32_junction(real_path, link_path)

# Based on https://github.com/Erotemic/ubelt/blob/master/ubelt/util_links.py
def _win32_junction(path, link):
    # junctions require absolute paths
    if not os.path.isabs(link):
        link = os.path.abspath(link)

    # os.symlink will fail if link exists, emulate the behavior here
    if exists(link):
        raise FileExistsError('File  exists: {} -> {}'.format(link, path))

    if not os.path.isabs(path):
        parent = os.path.join(link, os.pardir)
        path = os.path.join(parent, path)
        path = os.path.abspath(path)

    if os.path.isdir(path):
        # try using a junction (directory hard link)
        command = 'mklink /J "{}" "{}"'.format(link, path)
    else:
        # try using a hard link
        command = 'mklink /H "{}" "{}"'.format(link, path)

    _cmd(command)

def _win32_can_symlink():
    global __win32_can_symlink__
    if __win32_can_symlink__ is not None:
        return __win32_can_symlink__

    tempdir = tempfile.mkdtemp()

    dpath = join(tempdir, 'dpath')
    fpath = join(tempdir, 'fpath.txt')

    dlink = join(tempdir, 'dlink')
    flink = join(tempdir, 'flink.txt')

    fs.touchp(fpath)

    try:
        os.symlink(dpath, dlink)
        can_symlink_directories = os.path.islink(dlink)
    except OSError:
        can_symlink_directories = False

    try:
        os.symlink(fpath, flink)
        can_symlink_files = os.path.islink(flink)
    except OSError:
        can_symlink_files = False

    # Cleanup the test directory
    shutil.rmtree(tempdir)

    __win32_can_symlink__ = can_symlink_directories and can_symlink_files

    return __win32_can_symlink__

# Based on https://github.com/Erotemic/ubelt/blob/master/ubelt/util_cmd.py
def _cmd(command):
    import subprocess
    # Create a new process to execute the command
    def make_proc():
        # delay the creation of the process until we validate all args
        proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True,
                                universal_newlines=True, cwd=None, env=None)
        return proc

    proc = make_proc()
    (out, err) = proc.communicate()
    if proc.wait() != 0 :
        raise OSError(str(info))
